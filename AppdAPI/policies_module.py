import requests
import json
import os

def export_policies(controller_host, application_id, headers, filename):
    endpoint = f"{controller_host}/controller/policies/{application_id}"
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        try:
            with open(filename, 'w') as file:
                json.dump(response.json(), file)

            # Checking if the file is empty
            if os.path.getsize(filename) == 0:
                print(f"{filename} is empty.")
            else:
                print(f"Policies exported successfully to {filename}.")

        except IOError as e:
            print(f"Failed to write to {filename}. Error: {e}")
    else:
        print(f"Failed to export policies. Status code: {response.status_code}")


def import_policies(controller_host, application_id, headers, filename, overwrite=False):
    endpoint = f"{controller_host}/controller/policies/{application_id}"
    if overwrite:
        endpoint += "?overwrite=true"

    # Remove the Content-Type from headers as requests will set this automatically for multipart/form-data
    if "Content-Type" in headers:
        del headers["Content-Type"]

    # Check if the file exists and is not empty before proceeding
    if not os.path.exists(filename):
        print(f"{filename} does not exist.")
        return
    if os.path.getsize(filename) == 0:
        print(f"{filename} is empty. Aborting import.")
        return

    try:
        with open(filename, 'rb') as file:
            files = {'file': (filename, file)}
            response = requests.post(endpoint, headers=headers, files=files)

        if response.status_code == 200:
            print(f"Successfully imported policies from {filename}")
        else:
            print(f"Failed to import policies from {filename}. Status code: {response.status_code}")
            print(response.text)

    except IOError as e:
        print(f"Failed to read from {filename}. Error: {e}")
