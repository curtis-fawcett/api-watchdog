import requests
import csv
import os
from datetime import datetime

from Cython.Compiler.Parsing import p_assert_statement

history_file = "api_history.csv"

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

def show_statistics(rows):
    total_tests = len(rows)
    passed_tests = 0

    for row in rows:
        if row[2] == "PASS":
            passed_tests += 1

    failed_tests = total_tests - passed_tests

    if total_tests == 0:
        pass_rate = 0
    else:
        pass_rate = round(passed_tests / total_tests * 100, 1)

    print("API Statistics")
    print()
    print("Total Tests:", total_tests)
    print("Passed:", passed_tests)
    print("Failed:", failed_tests)
    print("Pass Rate:", pass_rate, "%")

def show_history(history_file):
    while True:
        print("API Test History")
        print()
        print("1. All tests")
        print("2. Failed tests")
        print("3. Last 5 tests")
        print("4. Statistics")
        print("5. Back to main menu")

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
            return

        else:
            print("Please choose an option from the history menu")

def test_api(url):
    if url == "":
        print("URL cannot be empty")
        return None, None, None

    try:
        response = requests.get(url, timeout=5)

    except requests.exceptions.ConnectionError:
        print("Connection failed")
        return None, None, None

    except requests.exceptions.Timeout:
        print("Connection timed out")
        return None, None, None

    except requests.exceptions.MissingSchema:
        print("Invalid URL. Include http:// or https://")
        return None, None, None

    if response.status_code == 200:
        result = "PASS"
    else:
        result = "FAIL"

    response_time = int(response.elapsed.total_seconds() * 1000)

    return result, response.status_code, response_time

def save_result(history_file, timestamp, url, test_result, status_code, response_time):
    file_exists = os.path.exists(history_file)

    with open(history_file, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Time", "URL", "Test Result", "Status Code", "Response Time"])

        writer.writerow([timestamp, url, test_result, status_code, response_time])

def print_test_result(test_result, status_code, response_time):
    print("Result:", test_result)
    print("Status Code:", status_code)
    print("Response Time:", response_time, "ms")

def run_api_test(history_file):
    url = input("Enter API URL: ").strip()
    test_result, status_code, response_time = test_api(url)

    if test_result is not None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_result(history_file, timestamp, url, test_result, status_code, response_time)
        print_test_result(test_result, status_code, response_time)

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