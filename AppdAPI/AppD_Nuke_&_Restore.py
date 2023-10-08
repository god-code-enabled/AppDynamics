import requests
import certifi
import os
from delete_HRPA import delete_all_entities
from health_rules_module import export_health_rules, import_health_rules
from actions_module import export_actions, import_actions
from policies_module import export_policies, import_policies
import view

os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

CONTROLLER_PORT = 443
SECRET_KEY = ""  # ADD IF NOT USING API TOKEN
API_TOKEN = ""  # ADD IF NOT USING SECRET
ACCOUNT_NAME = "" # ADD ACCOUNT NAME
CONTROLLER_HOST = f"https://{ACCOUNT_NAME}.saas.appdynamics.com"
CLIENT_ID = F"clientname@{ACCOUNT_NAME}" #REPLACE "clientname" WITH ACTUAL ACCOUNT NAME
APPLICATION_ID = "" # ADD APPLICATION ID

# define exclusions here4
WHITE_LIST_POLICIES = []
WHITE_LIST_ACTIONS = []
WHITE_LIST_HEALTH_RULES = []


#clear output
def clear_screen():
    os_name = os.name
    if os_name == 'posix':
        os.system('clear')
    elif os_name == 'nt':
        os.system('cls')

# create a backup folder in the working directory for the exports
def ensure_backups_directory():
    if not os.path.exists('backups'):
        os.makedirs('backups')


def generate_token():
    global API_TOKEN
    token_endpoint = f"{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/api/oauth/access_token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": SECRET_KEY
    }
    response = requests.post(token_endpoint, data=payload)  # Use POST method here
    if response.status_code == 200:
        token_data = response.json()
        API_TOKEN = token_data.get("access_token")
    else:
        print(f"Failed to generate token. Status code: {response.status_code}")


# Generate a new token if Secret Key is not empty
if SECRET_KEY != "":
    generate_token()

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}


def main():
    while True:
        print("\n" + "=" * 40)
        print("AppDynamics REST Manager".center(40))
        print("=" * 40 + "\n")

        print("Choose an option:")
        print("1. Export entities")
        print("2. Delete entities")
        print("3. Import entities")
        print("4. View entities")
        print("5. Exit\n")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '1':
            print("\n" + "-" * 30)
            print("Exporting Entities".center(30))
            print("-" * 30 + "\n")
            export_health_rules(CONTROLLER_HOST, APPLICATION_ID, HEADERS, 'backups/health_rules.xml')
            export_actions(CONTROLLER_HOST, APPLICATION_ID, HEADERS, 'backups/actions.json')
            export_policies(CONTROLLER_HOST, APPLICATION_ID, HEADERS, 'backups/policies.json')
            input("\nOperation completed. Press Enter to continue...")

        elif choice == '2':
            print("\n" + "-" * 30)
            print("Deleting Entities".center(30))
            print("-" * 30 + "\n")
            delete_all_entities(CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN, WHITE_LIST_POLICIES,
                                WHITE_LIST_ACTIONS, WHITE_LIST_HEALTH_RULES)
            input("\nOperation completed. Press Enter to continue...")

        elif choice == '3':
            print("\n" + "-" * 30)
            print("Importing Entities".center(30))
            print("-" * 30 + "\n")
            overwrite_option = input("Do you want to overwrite existing entities if they have the same name? (y/n): ")
            overwrite = True if overwrite_option.lower() == 'y' else False
            import_health_rules(CONTROLLER_HOST, APPLICATION_ID, HEADERS, 'backups/health_rules.xml', overwrite)
            import_actions(CONTROLLER_HOST, APPLICATION_ID, HEADERS, 'backups/actions.json')
            import_policies(CONTROLLER_HOST, APPLICATION_ID, HEADERS, 'backups/policies.json', overwrite)
            input("\nOperation completed. Press Enter to continue...")

        elif choice == '4':  # New option to view entities
            print("Which entities would you like to view?")
            print("1. Health Rules")
            print("2. Policies")
            print("3. Actions")
            view_choice = input("Enter your choice (1/2/3): ")

            if view_choice == '1':
                view.fetch_and_display_health_rules(CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN)
            elif view_choice == '2':
                view.fetch_and_display_policies(CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN)
            elif view_choice == '3':
                view.fetch_and_display_actions(CONTROLLER_HOST, CONTROLLER_PORT, APPLICATION_ID, API_TOKEN)
            else:
                print("Invalid choice!")

        elif choice == '5':
            print("Exiting Program...\n")
            break

        else:
            print("\nInvalid choice! Please select a valid option.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
