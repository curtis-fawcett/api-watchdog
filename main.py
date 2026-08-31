import config

from history import show_history
from api_tester import run_api_test
from profiles import profiles_menu

history_file = "api_history.csv"

def show_settings():
    print("Settings")
    print()

    print("Current slow response threshold:", config.slow_response_threshold, "ms")
    settings_choice = input("Enter new threshold in ms: ")

    if settings_choice == "":
        print("Threshold cannot be empty")
    else:
        try:
            new_threshold = int(settings_choice)

            if new_threshold <= 0:
                print("Threshold must be greater than 0")
            else:
                config.set_slow_response_threshold(new_threshold)
                print("Slow response threshold updated to", new_threshold, "ms")
        except ValueError:
            print("Threshold must be a whole number")

def main():
    config.load_settings()

    while True:
        print("API Watchdog")
        print()
        print("1. Test an API")
        print("2. View test history")
        print("3. API Profiles")
        print("4. Settings")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_api_test(history_file)

        elif choice == "2":
            show_history(history_file)

        elif choice == "3":
            profiles_menu()

        elif choice == "4":
            show_settings()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Please choose an option from the menu")

if __name__ == "__main__":
    main()