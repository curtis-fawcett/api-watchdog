import csv
import os

import config
from statistics import show_statistics


def load_history(history_file):
    """Load API test history from the CSV file."""
    rows = []

    if not os.path.exists(history_file):
        return rows

    with open(history_file, "r", newline="") as file:
        reader = csv.reader(file)

        next(reader, None)

        for row in reader:
            rows.append(row)

    return rows


def print_history_row(row):
    """Display one API test history record."""
    response_validation = row[5] if len(row) > 5 else "N/A"

    print(
        "Time:", row[0],
        "| URL:", row[1],
        "| Result:", row[2],
        "| Status:", row[3],
        "| Response Time:", row[4], "ms",
        "| Response Validation:", response_validation
    )


def save_result(
    history_file,
    timestamp,
    url,
    test_result,
    status_code,
    response_time,
    response_valid
):
    """Save an API test result to the CSV history file."""
    file_exists = os.path.exists(history_file)

    with open(history_file, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Time",
                "URL",
                "Test Result",
                "Status Code",
                "Response Time",
                "Response Validation"
            ])

        writer.writerow([
            timestamp,
            url,
            test_result,
            status_code,
            response_time,
            "PASS" if response_valid else "FAIL"
        ])


def show_history(history_file):
    """Display the API test history menu and handle selections."""
    while True:
        print("API Test History")
        print()
        print("1. All tests")
        print("2. Failed tests")
        print("3. Passed tests")
        print("4. Last 5 tests")
        print("5. Statistics")
        print("6. Search by URL")
        print("7. Search by Status Code")
        print("8. Show Slow Responses")
        print("9. Top 5 Fastest Tests")
        print("10. Top 5 Slowest Tests")
        print("11. Clear Test History")
        print("12. Last Failed Test")
        print("13. Show Invalid Responses")
        print("14. Back to main menu")

        history_choice = input("Choose an option: ").strip()
        rows = load_history(history_file)
        print()

        if history_choice == "1":
            print("All tests")

            if rows:
                for row in rows:
                    print_history_row(row)
            else:
                print("No history found")

        elif history_choice == "2":
            print("Failed tests")

            if rows:
                failed_found = False
                for row in rows:
                    if row[2] != "PASS":
                        failed_found = True
                        print_history_row(row)
                if not failed_found:
                    print("No failed tests found")
            else:
                print("No history found")

        elif history_choice == "3":
            print("Passed tests")

            if rows:
                passed_found = False
                for row in rows:
                    if row[2] == "PASS":
                        passed_found = True
                        print_history_row(row)
                if not passed_found:
                    print("No passed tests found")

        elif history_choice == "4":
            print("Last 5 tests")

            if rows:
                for row in rows[-5:]:
                    print_history_row(row)

            else:
                print("No history found")

        elif history_choice == "5":
            show_statistics(rows)

        elif history_choice == "6":
            search_term = input("Enter URL keyword: ").strip()

            if not search_term:
                print("Search cannot be empty")
            else:
                match_found = False

                for row in rows:
                    if search_term.lower() in row[1].lower():
                        match_found = True
                        print_history_row(row)

                if not match_found:
                    print("No matching URLs found")

        elif history_choice == "7":
            search_code = input("Enter Status Code: ").strip()

            if not search_code:
                print("Status code cannot be empty")
            else:
                code_match_found = False

                for row in rows:
                    if search_code == row[3]:
                        code_match_found = True
                        print_history_row(row)
                if not code_match_found:
                    print("No matching Status Code found ")

        elif history_choice == "8":
            slow_response_found = False

            for row in rows:
                response_time = int(row[4])

                if response_time > config.slow_response_threshold:
                    slow_response_found = True
                    print_history_row(row)

            if not slow_response_found:
                print("No slow responses found")

        elif history_choice == "9":
            if rows:
                for row in sorted(rows, key=lambda row: int(row[4]))[:5]:
                    print_history_row(row)
            else:
                print("No history found")

        elif history_choice == "10":
            if rows:
                for row in sorted(rows, key=lambda row: int(row[4]), reverse=True)[:5]:
                    print_history_row(row)
            else:
                print("No history found")

        elif history_choice == "11":
            while True:
                user_input = input("Are you sure you want to clear all test history? (yes/no): ").strip().lower()

                if user_input == "yes":
                    with open(history_file, "w", newline="") as file:
                        writer = csv.writer(file)

                        writer.writerow(["Time", "URL", "Test Result", "Status Code", "Response Time"])
                        print("History has been cleared")
                        break

                elif user_input == "no":
                    break

                else:
                    print("Please enter yes or no")

        elif history_choice == "12":
            if rows:
                failed_found = False
                for row in reversed(rows):
                    if row[2] != "PASS":
                        failed_found = True
                        print_history_row(row)
                        break
                if not failed_found:
                    print("No failed tests found")
            else:
                print("No history found")

        elif history_choice == "13":
            print("Invalid Responses")

            invalid_response_found = False

            for row in rows:
                if len(row) > 5 and row[5] == "FAIL":
                    invalid_response_found = True
                    print_history_row(row)

            if not invalid_response_found:
                print("No invalid responses found")

        elif history_choice == "14":
            return

        else:
            print("Please choose an option from the history menu")