import requests
import csv
import os
from datetime import datetime

history_file = "api_history.csv"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def show_history(history_file):

        file_exists = os.path.exists(history_file)

        if file_exists:

            with open(history_file, "r") as file:
                reader = csv.reader(file)

                next(reader)

                for row in reader:
                    print("Time:", row[0], "|", "URL:", row[1], "|", "Result:", row[2], "|", "Status:", row[3], "|", "Response Time:", row[4], "ms")
        else:
            print("No History found")

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
url = input("Enter API URL: ").strip()

test_result, status_code, response_time = test_api(url)

if test_result:
    file_exists = os.path.exists(history_file)

    with open(history_file, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Time", "URL", "Test Result", "Status Code", "Response Time"])
        writer.writerow([timestamp, url, test_result, status_code, response_time])
    print("Result:", test_result)
    print("Status Code:", status_code)
    print("Response Time:", response_time, "ms")

show_history(history_file)