import requests

def test_api(url):

    if url == "":
        print("URL cannot be empty")

    else:

        try:
            response = requests.get(url, timeout=5)

        except requests.exceptions.ConnectionError:
            print("Connection failed")
        except requests.exceptions.Timeout:
            print("Connection timed out")
        except requests.exceptions.MissingSchema:
            print("Invalid URL. Include http:// or https://")

        else:
            print("Status Code:", response.status_code)

            if response.status_code == 200:
                print("PASS")
            else:
                print("FAIL")

            response_time = int(response.elapsed.total_seconds() * 1000)

            print("Response Time:" , response_time, "ms")

url = input("Enter API URL: ").strip()

test_api(url)