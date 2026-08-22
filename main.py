from history import show_history
from api_tester import run_api_test

history_file = "api_history.csv"

def main():
    while True:
        print("API Watchdog")
        print()
        print("1. Test an API")
        print("2. View test history")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_api_test(history_file)

        elif choice == "2":
            show_history(history_file)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Please choose an option from the menu")

if __name__ == "__main__":
    main()