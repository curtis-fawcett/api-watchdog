import json

FILENAME = "profiles.json"

def add_profile():
    profiles_data = load_profiles()

    try:

        profile_name = input(

            "Enter profile name (or 0 to go back): "

        ).strip()

        if profile_name == "0":
            return

        while not profile_name:

            print("Profile name cannot be empty.")

            profile_name = input(

                "Enter profile name (or 0 to go back): "

            ).strip()

            if profile_name == "0":
                break

        if profile_name == "0":
            return

        while profile_name in profiles_data:

            print("A profile with that name already exists.")

            profile_name = input(

                "Enter profile name (or 0 to go back): "

            ).strip()

            if profile_name == "0":
                break

        if profile_name == "0":
            return

        while True:
            api_url = input("Enter the API URL (or 0 to go back): ").strip()

            if api_url == "0":
                return

            if api_url.startswith(("http://", "https://")):
                break

            print("URL must start with http:// or https://")

        field_name = input("Enter JSON field to verify (optional, or 0 to go back): ").strip()

        if field_name == "0":
            return

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

def edit_profile():
    """Edit an existing API profile."""
    profiles_data = load_profiles()

    if not profiles_data:
        print("No profiles found.")
        return

    for number, profile_name in enumerate(profiles_data, start=1):
        print(f"{number}. {profile_name}")

    print("0. Back")

    while True:
        edit_choice = input("Enter profile number to edit: ").strip()

        try:
            edit_number = int(edit_choice)

            if edit_number == 0:
                return

            if edit_number < 1 or edit_number > len(profiles_data):
                print("Invalid profile number.")
                continue

            break

        except ValueError:
            print("Please enter a valid profile number.")

    profile_names = list(profiles_data.keys())
    profile_name = profile_names[edit_number - 1]
    profile_data = profiles_data[profile_name]

    print(f"Editing profile: {profile_name}")
    print(f"Current URL: {profile_data['url']}")
    print(f"Current JSON field: {profile_data['field']}")

    new_url = input("Enter new API URL: ").strip()

    if not new_url:
        new_url = profile_data["url"]

    if not new_url.startswith(("http://", "https://")):
        print("URL must start with http:// or https://")
        return

    new_field = input("Enter new JSON field: ").strip()

    if not new_field:
        new_field = profile_data["field"]

    profiles_data[profile_name] = {
        "url": new_url,
        "field": new_field
    }

    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(profiles_data, file, indent=4)

    print(f"Profile '{profile_name}' updated successfully.")

def profiles_menu():
    """Display the API profiles menu and handle profile actions."""
    while True:
        print("API profiles")
        print()
        print("1. View profiles")
        print("2. Add profile")
        print("3. Delete profile")
        print("4. Edit profile")
        print("5. Back")

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
            add_profile()

        elif profile_choice == "3":
            profiles_data = load_profiles()

            if not profiles_data:
                print("No profiles found.")
                continue

            profile_names = list(profiles_data.keys())

            while True:
                for number, profile_name in enumerate(profile_names, start=1):
                    print(f"{number}. {profile_name}")

                print("0. Back")

                delete_choice = input("Enter profile number to delete: ").strip()

                try:
                    delete_number = int(delete_choice)

                    if delete_number == 0:
                        break

                    if delete_number < 1 or delete_number > len(profile_names):
                        print("Invalid profile number.")
                        continue

                    profile_name = profile_names[delete_number - 1]
                    del profiles_data[profile_name]

                    with open(FILENAME, "w", encoding="utf-8") as file:
                        json.dump(profiles_data, file, indent=4)

                    print(f"Profile '{profile_name}' deleted successfully.")
                    print()
                    break

                except ValueError:
                    print("Please enter a valid profile number.")

        elif profile_choice == "4":
            edit_profile()

        elif profile_choice == "5":
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