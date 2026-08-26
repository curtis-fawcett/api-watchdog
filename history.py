import csv
import os
import config

from statistics import show_statistics

def load_history(history_file):
    rows = []
    file_exists = os.path.exists(history_file)

    if not file_exists:
        return rows
    with open(history_file, "r") as file:
        reader = csv.reader(file)

        next(reader)

        for row in reader:
            rows.append(row)

    return rows

def print_history_row(row):
    print("Time:", row[0], "|", "URL:", row[1], "|", "Result:", row[2], "|", "Status:", row[3], "|",
          "Response Time:", row[4], "ms")

def save_result(history_file, timestamp, url, test_result, status_code, response_time):
    file_exists = os.path.exists(history_file)

    with open(history_file, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Time", "URL", "Test Result", "Status Code", "Response Time"])

        writer.writerow([timestamp, url, test_result, status_code, response_time])

def show_history(history_file):
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
        print("12. Back to main menu")

        history_choice = input("Choose an option: ").strip()
        print()
        rows = load_history(history_file)

        if history_choice == "1":
            print("All tests")

            if rows:
                for row in rows:
                    print_history_row(row)
            else:
                print("No History found")

        elif history_choice == "2":
            print("Failed tests")

            if rows:
                failed_found = False
                for row in rows:
                    if row[2] == "FAIL":
                        failed_found = True
                        print_history_row(row)
                if not failed_found:
                    print("No failed tests found")
            else:
                print("No History found")

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
                history_count = len(rows)
                if history_count < 5:
                    if history_count == 1:
                        print("Only", history_count, "test found. Showing the available test.")
                    else:
                        print("Only", history_count, "tests found. Showing all available tests.")
                for row in rows[-5:]:
                    print_history_row(row)
            else:
                print("No History found")

        elif history_choice == "5":
            print("Statistics")

            show_statistics(rows)

        elif history_choice == "6":
            print("URL Search")

            search_term = input("Enter URL keyword: ").strip()

            if search_term == "":
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
            print("Status Code Search")

            search_code = input("Enter Status Code: ").strip()

            if search_code == "":
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
            print("Slow Responses")

            response_time_filter = False

            for row in rows:
                response_time = int(row[4])

                if response_time > config.slow_response_threshold:
                    response_time_filter = True
                    print_history_row(row)
            if not response_time_filter:
                print("No slow responses found")

        elif history_choice == "9":
            print("Top 5 Fastest tests")
            print()

            if rows:
                fastest_tests = rows.copy()
                fastest_tests.sort(key=lambda row: int(row[4]), reverse=False)

                for row in fastest_tests[:5]:
                    print_history_row(row)
            else:
                print("No history found")

        elif history_choice == "10":
            print("Top 5 Slowest tests")
            print()

            if rows:
                slowest_tests = rows.copy()
                slowest_tests.sort(key=lambda row: int(row[4]), reverse=True)

                for row in slowest_tests[:5]:
                    print_history_row(row)
            else:
                print("No History found")

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
            return

        else:
            print("Please choose an option from the history menu")