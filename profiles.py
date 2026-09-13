import json

FILENAME = "profiles.json"


def profiles_menu():
    """Display the API profiles menu and handle profile actions."""
    while True:
        print("API profiles")
        print()
        print("1. View profiles")
        print("2. Add profile")
        print("3. Delete profile")
        print("4. Back")

        profile_choice = input("Choose an option: ").strip()

        if profile_choice == "1":
            profiles_data = load_profiles()

            if not profiles_data:
                print("No profiles found. Please create a profile first.")
            else:
                for number, (profile_name, profile_data) in enumerate(
                        profiles_data.items(), start=1
                ):
                    print(
                        f"{number}. {profile_name} - "
                        f"{profile_data['url']} - "
                        f"Field: {profile_data['field']}"
                    )

        elif profile_choice == "2":
            profiles_data = load_profiles()

            try:
                profile_name = input("Enter profile name: ").strip()

                if not profile_name:
                    print("Profile name cannot be empty.")
                    continue

                if profile_name in profiles_data:
                    print("A profile with that name already exists.")
                    continue

                api_url = input("Enter the API URL: ").strip()
                field_name = input("Enter JSON field to verify (optional): ").strip()

                if not api_url.startswith(("http://", "https://")):
                    print("URL must start with http:// or https://")
                    continue

                profiles_data[profile_name] = {
                    "url": api_url,
                    "field": field_name
                }

                with open(FILENAME, "w", encoding="utf-8") as file:
                    json.dump(profiles_data, file, indent=4)

                print(f"Profile '{profile_name}' added successfully.")
                print()

            except OSError as error:
                print(f"An error occurred while saving: {error}")

        elif profile_choice == "3":
            profiles_data = load_profiles()

            if not profiles_data:
                print("No profiles found.")
                continue

            profile_names = list(profiles_data.keys())

            for number, profile_name in enumerate(profile_names, start=1):
                print(f"{number}. {profile_name}")

            delete_choice = input("Enter profile number to delete: ").strip()

            try:
                delete_number = int(delete_choice)

                if delete_number < 1 or delete_number > len(profile_names):
                    print("Invalid profile number.")
                    continue

                profile_name = profile_names[delete_number - 1]
                del profiles_data[profile_name]

                with open(FILENAME, "w", encoding="utf-8") as file:
                    json.dump(profiles_data, file, indent=4)

                print(f"Profile '{profile_name}' deleted successfully.")
                print()

            except ValueError:
                print("Please enter a valid profile number.")

        elif profile_choice == "4":
            return

        else:
            print("Please choose an option from the profiles menu.")


def load_profiles():
    """Load saved API profiles from the JSON file."""
    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, dict):
                return data

            return {}

    except (FileNotFoundError, json.JSONDecodeError):
        return {}