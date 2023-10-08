import requests
import os
import xml.etree.ElementTree as ET


def export_health_rules(controller_host, application_id, headers, filename):
    endpoint = f"{controller_host}/controller/healthrules/{application_id}"
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        entities = ET.fromstring(response.text)

        try:
            with open(filename, 'w') as file:
                file.write(ET.tostring(entities, encoding='utf-8').decode('utf-8'))

            # Checking if the file is empty
            if os.path.getsize(filename) == 0:
                print(f"{filename} is empty.")
            else:
                print(f"Exported health rules successfully to {filename}.")

        except IOError as e:
            print(f"Failed to write to {filename}. Error: {e}")
    else:
        print(f"Failed to export health rules. Status code: {response.status_code}")


def import_health_rules(controller_host, application_id, headers, filename, overwrite=False):
    endpoint = f"{controller_host}/controller/healthrules/{application_id}"
    if overwrite:
        endpoint += "?overwrite=true"

    # Remove the "Content-Type" from headers as it will be set automatically by requests when sending files
    headers.pop("Content-Type", None)

    # Check if the file exists and is not empty before proceeding
    if not os.path.exists(filename):
        print(f"{filename} does not exist.")
        return
    if os.path.getsize(filename) == 0:
        print(f"{filename} is empty. Aborting import.")
        return

    try:
        with open(filename, 'rb') as file:
            files = {
                "file": (os.path.basename(filename), file, "application/xml")
            }
            response = requests.post(endpoint, headers=headers, files=files)

        if response.status_code == 200 or response.status_code == 201:
            print(f"Successfully imported health rules from {filename}")
        else:
            print(f"Failed to import health rules from {filename}. Status code: {response.status_code}")
            print(response.text)

    except IOError as e:
        print(f"Failed to read from {filename}. Error: {e}")