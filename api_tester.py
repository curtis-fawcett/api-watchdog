import requests
import config

from datetime import datetime
from history import save_result

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
    url = input("Enter API URL: ").strip()
    test_result, status_code, response_time = test_api(url)

    if test_result is not None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_result(history_file, timestamp, url, test_result, status_code, response_time)
        print_test_result(test_result, status_code, response_time)