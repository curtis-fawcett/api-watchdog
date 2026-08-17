import requests
import csv
import os
from datetime import datetime

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

def show_history(history_file):
    print("API Test History")
    print()
    print("1. All tests")
    print("2. Failed tests")
    print("3. Last 5 tests")
    print("4. Exit")

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
            for row in rows:
                if row[2] == "FAIL":
                    print_history_row(row)
        else:
            print("No History found")

    elif history_choice == "3":
        if rows:
            for row in rows[-5:]:
                print_history_row(row)
        else:
            print("No History found")

    elif history_choice == "4":
        return

def test_api(url):
    if url == "":
        print("URL cannot be empty")
        return None, None, None
    else:
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
        else:
            if response.status_code == 200:
                result = "PASS"
            else:
                result = "FAIL"
            response_time = int(response.elapsed.total_seconds() * 1000)
            return result, response.status_code, response_time

while True:
    print("API Watchdog")
    print()
    print("1. Test an API")
    print("2. View test history")
    print("3. Exit")

    choice = input("Choose an option: ").strip()
    if choice == "1":
        url = input("Enter API URL: ").strip()
        test_result, status_code, response_time = test_api(url)
        if test_result is not None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_exists = os.path.exists(history_file)

            with open(history_file, "a", newline="") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Time", "URL", "Test Result", "Status Code", "Response Time"])
                writer.writerow([timestamp, url, test_result, status_code, response_time])
            print("Result:", test_result)
            print("Status Code:", status_code)
            print("Response Time:", response_time, "ms")

    elif choice == "2":
        show_history(history_file)

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Please choose an option from the menu")