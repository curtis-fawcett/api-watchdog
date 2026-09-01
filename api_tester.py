import requests
import config

from datetime import datetime
from history import save_result
from profiles import load_profiles


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

    if response_time > config.slow_response_threshold:
        print("Warning: Slow response")

def run_api_test(history_file):
    print("Test an API")
    print()
    print("1. Use a saved profile")
    print("2. Enter a custom URL")
    print("3. Back")

    test_choice = input("Choose an option: ").strip()

    if test_choice == "1":
        profiles_data = load_profiles()
        if not profiles_data:
            print("No profiles found. Please create a profile first.")
            return
        else:
            for number, (profile_name, api_url) in enumerate(profiles_data.items(), start=1):
                print(f"{number}. {profile_name}")

            profile_selection = input("Enter profile number: ").strip()
            try:
                profile_number = int(profile_selection)

                if profile_number < 1 or profile_number > len(profiles_data):
                    print("Invalid profile number.")
                    return
                else:
                    profile_name = list(profiles_data.keys())[profile_number - 1]
                    url = profiles_data[profile_name]

            except ValueError:
                print("Please enter a valid number.")
                return

    elif test_choice == "2":
        url = input("Enter API URL: ").strip()

    elif test_choice == "3":
        return

    else:
        print("Invalid option.")
        return

    test_result, status_code, response_time = test_api(url)

    if test_result is not None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_result(history_file, timestamp, url, test_result, status_code, response_time)
        print_test_result(test_result, status_code, response_time)