import requests
from datetime import datetime
from config import slow_response_threshold
from history import load_history, print_history_row, save_result, show_history

history_file = "api_history.csv"

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

def print_test_result(test_result, status_code, response_time):
    print("Result:", test_result)
    print("Status Code:", status_code)
    print("Response Time:", response_time, "ms")

    if response_time > slow_response_threshold:
        print("Warning: Slow response")

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