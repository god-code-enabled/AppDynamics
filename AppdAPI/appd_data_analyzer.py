import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time
import certifi
import os
from postman_template import create_postman_json

os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# Replace with your AppDynamics controller info and API token
CONTROLLER_HOST = "controller host"
CONTROLLER_PORT = 443
API_TOKEN = "api token here"
ACCOUNT_NAME = "account name here"
CLIENT_ID = "client ID"
APPLICATION_ID = "app ID"  # Replace with your application ID
TIER_ID="Tier ID here"
DURATION_MIN = 0 # Duration in min
RULE_ID = "HR ID HERE" # replace with your health rule ID
sec = 3 # adjust delay between requests here

def get_metric_data(metric_path):
    # AppDynamics API endpoint to get metric data
    url = f"https://{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/rest/applications/{APPLICATION_ID}/metric-data"

    # API request headers with the API token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    # API request parameters
    params = {
        "metric-path": metric_path,
        "time-range-type": "BEFORE_NOW",
        "duration-in-mins": DURATION_MIN
    }

    try:
        # Send the GET request with the API token
        response = requests.get(url, headers=headers, params=params, verify=certifi.where())

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the XML response
            root = ET.fromstring(response.text)

            # Get the sum of the metric values
            sum = int(root.find('.//sum').text)

            return sum
        else:
            print(f"Failed to fetch metric data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the AppDynamics API: {e}")
        return None


def get_business_transactions_data():
    # AppDynamics API endpoint to get business transactions data
    url = f"https://{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/rest/applications/{APPLICATION_ID}/business-transactions"

    # API request headers with the API token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    # API request parameters
    params = {
        "time-range-type": "BEFORE_NOW",
        "duration-in-mins": DURATION_MIN
    }

    try:
        # Send the GET request with the API token
        response = requests.get(url, headers=headers, params=params, verify=certifi.where())

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the XML response
            root = ET.fromstring(response.text)

            # Create a list of dictionaries, each containing the data of a business transaction
            data = []
            for bt in root.findall('business-transaction'):
                bt_name = bt.find('name').text
                tier_name = bt.find('tierName').text

                # Get the total calls for this business transaction
                total_calls = get_metric_data(
                    f"Business Transaction Performance|Business Transactions|{tier_name}|{bt_name}|Calls per Minute")

                data.append({
                    'id': bt.find('id').text,
                    'name': bt_name,
                    'app': APPLICATION_ID,
                    'tier': tier_name,
                    'entryPointType': bt.find('entryPointType').text,
                    'Total Calls': total_calls
                })

            # Convert the list of dictionaries to a pandas Data Frame
            df = pd.DataFrame(data)

            # Save the DataFrame to a CSV file
            results_folder = os.path.expanduser("~/Desktop/appd_api_results")
            os.makedirs(results_folder, exist_ok=True)
            df.to_csv(os.path.join(results_folder, 'business_transactions.csv'), index=False)

            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(os.path.join(results_folder, 'business_transactions.csv'))

            # Write the DataFrame to an Excel file
            df.to_excel(os.path.join(results_folder, 'business_transactions.xlsx'), index=False)
            print(f"Saved {len(df)} business transactions to business_transactions.csv")
        else:
            print(f"Failed to fetch business transactions data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the AppDynamics API: {e}")

    # delay prior to next request
    time.sleep(sec)

    # Get the total number of calls and errors
    total_calls = get_metric_data("Overall Application Performance|Calls per Minute")
    total_errors = get_metric_data("Overall Application Performance|Errors per Minute")

    # Calculate the error rate
    if total_calls is not None and total_errors is not None:
        error_rate = (total_errors / total_calls) * 100
        error_rate = round(error_rate)
        print(f"Error rate: {error_rate}%")

        # Create a DataFrame with the results
        df = pd.DataFrame({
            'Total Calls': [total_calls],
            'Total Errors': [total_errors],
            'Error Rate (%)': [error_rate]
        })

        # Save the DataFrame to a CSV file
        df.to_csv(os.path.join(results_folder, 'error_rate.csv'), index=False)

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(results_folder, 'error_rate.csv'))

        # Write the DataFrame to an Excel file
        df.to_excel(os.path.join(results_folder, 'error_rate.xlsx'), index=False)
        print(f"Saved error rate to error_rate.csv")


if __name__ == "__main__":
    postman_collection = "y" #"n"
    #postman_collection = input("would you like to create a postman collection? enter y or n, json file will be created in ~/Desktop/appd_api_results/")
    if postman_collection == "y":
        create_postman_json(CONTROLLER_HOST, CONTROLLER_PORT, CLIENT_ID, ACCOUNT_NAME, API_TOKEN, APPLICATION_ID, DURATION_MIN)
        print ("postman collection and environment json files created, open postman and import both files")
    else:
        pass
    get_business_transactions_data()
