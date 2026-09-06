import config

from api_tester import run_api_test
from history import show_history
from profiles import profiles_menu
from settings import show_settings

HISTORY_FILE = "api_history.csv"


def main():
    """Run the API Watchdog main menu."""
    config.load_settings()

    while True:
        print("API Watchdog")
        print()
        print("1. Test an API")
        print("2. View test history")
        print("3. API profiles")
        print("4. Settings")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_api_test(HISTORY_FILE)

        elif choice == "2":
            show_history(HISTORY_FILE)

        elif choice == "3":
            profiles_menu()

        elif choice == "4":
            show_settings()

        elif choice == "5":
            print("Goodbye!")
            return

        else:
            print("Please choose an option from the menu.")


if __name__ == "__main__":
    main()