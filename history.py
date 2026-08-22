import csv
import os
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
        print("3. Last 5 tests")
        print("4. Statistics")
        print("5. Search by URL")
        print("6. Back to main menu")

        history_choice = input("Choose an option: ").strip()
        rows = load_history(history_file)

        if history_choice == "1":
            if rows:
                for row in rows:
                    print_history_row(row)
            else:
                print("No History found")

        elif history_choice == "2":
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

        elif history_choice == "4":
            show_statistics(rows)

        elif history_choice == "5":
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

        elif history_choice == "6":
            return

        else:
            print("Please choose an option from the history menu")