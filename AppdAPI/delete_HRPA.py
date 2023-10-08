# delete_entities.py

import requests
import certifi

def get_entities(endpoint, CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN):
    url = f"{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/alerting/rest/v1/applications/{APPLICATION_ID}/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    try:
        response = requests.get(url, headers=headers, verify=certifi.where())
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch {endpoint}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the AppDynamics API: {e}")
        return None

def delete_entity(endpoint, entity_id, CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN):
    url = f"{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/alerting/rest/v1/applications/{APPLICATION_ID}/{endpoint}/{entity_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    try:
        response = requests.delete(url, headers=headers, verify=certifi.where())
        if response.status_code == 200 or response.status_code == 204:
            print(f"Successfully deleted {endpoint} with id {entity_id}")
        else:
            print(f"Failed to delete {endpoint}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the AppDynamics API: {e}")

def process_entities(endpoint, whitelist, CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN):
    entities = get_entities(endpoint, CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN)
    delete_list = []
    preserve_list = []

    if entities:
        for entity in entities:
            entity_id = str(entity['id'])
            if entity_id not in whitelist:
                delete_list.append(entity_id)
            else:
                preserve_list.append(entity_id)

    print(f"IDs to be deleted from {endpoint}: {delete_list}")
    print(f"IDs to be preserved in {endpoint}: {preserve_list}")

    delete_confirmation = input("Do you want to delete the listed items? (y/n): ")
    if delete_confirmation.lower() == 'y':
        for entity_id in delete_list:
            delete_entity(endpoint, entity_id, CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN)
    elif delete_confirmation.lower() == 'n':
        print(f"List of IDs preserved for {endpoint}: {preserve_list}")
    else:
        print("Invalid input. No action taken.")
    print('\n')


def delete_all_entities(CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN, WHITE_LIST_POLICIES=[],WHITE_LIST_ACTIONS=[],WHITE_LIST_HEALTH_RULES=[]):
    process_entities('policies', WHITE_LIST_POLICIES, CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN)
    process_entities('actions', WHITE_LIST_ACTIONS, CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN)
    process_entities('health-rules', WHITE_LIST_HEALTH_RULES, CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN)
