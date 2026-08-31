import json

FILENAME = "profiles.json"

def profiles_menu():
    while True:
        print("API Profiles")
        print()

        print("1. View Profiles")
        print("2. Add Profile")
        print("3. Delete Profile")
        print("4. Back")

        profile_choice = input("Choose an option: ").strip()

        if profile_choice == "1":
            profiles_data = load_profiles()

            if not profiles_data:
                print("No profiles found. Please create a profile first")
            else:
                for number, (profile_name, api_url) in enumerate(profiles_data.items(), start=1):
                    print(f"{number}. {profile_name}: {api_url}")

        elif profile_choice == "2":
            profiles_data = load_profiles()
            try:
                profile_name = input("Enter Profile name: ").strip()
                if not profile_name:
                    print("Profile name cannot be empty.")
                    continue

                if profile_name in profiles_data:
                    print("A profile with that name already exists.")
                    continue

                api_url = input("Enter the API URL: ").strip()

                if not api_url.startswith(("http://", "https://")):
                    print("URL must start with http:// or https://")
                    continue

                profiles_data[profile_name] = api_url

                with open(FILENAME, "w") as file:
                    json.dump(profiles_data, file, indent=4)
                print(f"Profile '{profile_name}' added successfully!")
                print()

            except OSError as e:
                print(f"An error occurred while saving: {e}")

        elif profile_choice == "3":
            profiles_data = load_profiles()

            if not profiles_data:
                print('No profiles found.')
            else:
                for number, (profile_name, api_url) in enumerate(profiles_data.items(), start=1):
                    print(f"{number}. {profile_name}")

                delete_choice = input("Enter profile number to delete: ")

                try:
                    delete_number = int(delete_choice)

                    if delete_number < 1 or delete_number > len(profiles_data):
                        print("Invalid profile number.")
                    else:
                        profile_name = list(profiles_data.keys())[delete_number - 1]

                        del profiles_data[profile_name]

                        with open(FILENAME, "w") as file:
                            json.dump(profiles_data, file, indent=4)

                        print(f"Profile '{profile_name}' deleted successfully.")
                        print()

                except ValueError:
                    print("Please enter a valid number.")

        elif profile_choice == "4":
            return

        else:
            print("Please choose an option from the menu")

def load_profiles():
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            return {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}