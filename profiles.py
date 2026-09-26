import json

FILENAME = "profiles.json"


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


def save_profiles(profiles_data):
    """Save API profiles to the JSON file."""
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(profiles_data, file, indent=4)


def get_profile_name(profiles_data):
    """Get a new profile name from the user."""
    while True:
        profile_name = input(
            "Enter profile name (or 0 to go back): "
        ).strip()

        if profile_name == "0":
            return None

        if not profile_name:
            print("Profile name cannot be empty.")
            continue

        if profile_name in profiles_data:
            print("A profile with that name already exists.")
            continue

        return profile_name


def get_api_url(prompt):
    """Get and validate an API URL from the user."""
    while True:
        api_url = input(prompt).strip()

        if api_url == "0":
            return None

        if api_url.startswith(("http://", "https://")):
            return api_url

        print("URL must start with http:// or https://")


def add_profile():
    """Add a new API profile."""
    profiles_data = load_profiles()

    profile_name = get_profile_name(profiles_data)

    if profile_name is None:
        return

    api_url = get_api_url(
        "Enter the API URL (or 0 to go back): "
    )

    if api_url is None:
        return

    field_name = input(
        "Enter JSON field to verify (optional, or 0 to go back): "
    ).strip()

    if field_name == "0":
        return

    profiles_data[profile_name] = {
        "url": api_url,
        "field": field_name
    }

    try:
        save_profiles(profiles_data)
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

    profile_name = select_profile(
        profiles_data,
        "Enter profile number to edit: "
    )

    if profile_name is None:
        return

    profile_data = profiles_data[profile_name]

    print()
    print(f"Editing profile: {profile_name}")
    print(f"Current URL: {profile_data['url']}")
    print(f"Current JSON field: {profile_data['field']}")

    new_url = input(
        "Enter new API URL (or 0 to go back): "
    ).strip()

    if new_url == "0":
        return

    if not new_url:
        new_url = profile_data["url"]

    while not new_url.startswith(("http://", "https://")):
        print("URL must start with http:// or https://")
        new_url = input(
            "Enter new API URL (or 0 to go back): "
        ).strip()

        if new_url == "0":
            return

    new_field = input(
        "Enter new JSON field (optional, or 0 to go back): "
    ).strip()

    if new_field == "0":
        return

    if not new_field:
        new_field = profile_data["field"]

    profiles_data[profile_name] = {
        "url": new_url,
        "field": new_field
    }

    try:
        save_profiles(profiles_data)
        print(f"Profile '{profile_name}' updated successfully.")
        print()

    except OSError as error:
        print(f"An error occurred while saving: {error}")


def select_profile(profiles_data, prompt):
    """Display profiles and return the selected profile name."""
    profile_names = list(profiles_data.keys())

    while True:
        print("Edit Profile")
        print()

        for number, profile_name in enumerate(profile_names, start=1):
            print(f"{number}. {profile_name}")

        print("0. Back")

        selection = input(prompt).strip()

        try:
            number = int(selection)

            if number == 0:
                return None

            if number < 1 or number > len(profile_names):
                print("Invalid profile number.")
                continue

            return profile_names[number - 1]

        except ValueError:
            print("Please enter a valid profile number.")


def delete_profile():
    """Delete a selected API profile."""
    profiles_data = load_profiles()

    if not profiles_data:
        print("No profiles found.")
        return

    profile_name = select_delete_profile(profiles_data)

    if profile_name is None:
        return

    del profiles_data[profile_name]

    try:
        save_profiles(profiles_data)
        print(f"Profile '{profile_name}' deleted successfully.")
        print()

    except OSError as error:
        print(f"An error occurred while saving: {error}")


def select_delete_profile(profiles_data):
    """Display profiles and return the profile selected for deletion."""
    profile_names = list(profiles_data.keys())

    while True:
        for number, profile_name in enumerate(profile_names, start=1):
            print(f"{number}. {profile_name}")

        print("0. Back")

        selection = input(
            "Enter profile number to delete: "
        ).strip()

        try:
            number = int(selection)

            if number == 0:
                return None

            if number < 1 or number > len(profile_names):
                print("Invalid profile number.")
                continue

            return profile_names[number - 1]

        except ValueError:
            print("Please enter a valid profile number.")


def view_profiles():
    """Display all saved API profiles."""
    profiles_data = load_profiles()

    if not profiles_data:
        print("No profiles found. Please create a profile first.")
        return

    for number, (profile_name, profile_data) in enumerate(
        profiles_data.items(),
        start=1
    ):
        print(
            f"{number}. {profile_name} - "
            f"{profile_data['url']} - "
            f"Field: {profile_data['field']}"
        )


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
            view_profiles()

        elif profile_choice == "2":
            add_profile()

        elif profile_choice == "3":
            delete_profile()

        elif profile_choice == "4":
            edit_profile()

        elif profile_choice == "5":
            return

        else:
            print("Please choose an option from the profiles menu.")