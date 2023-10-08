from tabulate import tabulate
from delete_HRPA import get_entities


def display_actions(data):
    if not data or not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        input("\n\nA nuke may have gone off! No actions data to display. \n\nPress Enter to continue")
        return

    headers = list(data[0].keys())
    actions_data = [list(action.values()) for action in data]
    table = tabulate(actions_data, headers=headers, tablefmt="grid")
    print(table)


def display_health_rules(data):
    if not data or not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        input("\n\nA nuke may have gone off! No actions data to display. \n\nPress Enter to continue")
        return
    headers = list(data[0].keys())
    health_rules_data = [list(hr.values()) for hr in data]
    table = tabulate(health_rules_data, headers=headers, tablefmt="grid")
    print(table)

def display_policies(data):
    if not data or not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        input("\n\nA nuke may have gone off! No actions data to display. \n\nPress Enter to continue")
        return
    headers = list(data[0].keys())
    table = tabulate(data, headers=headers, tablefmt="grid")
    print(table)


def fetch_and_display_actions(CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN):
    data = get_entities('actions', CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN)
    display_actions(data)

def fetch_and_display_health_rules(CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN):
    data = get_entities('health-rules', CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN)
    display_health_rules(data)

def fetch_and_display_policies(CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN):
    data = get_entities('policies', CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN)
    display_policies(data)
