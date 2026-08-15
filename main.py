import requests

# Define the target URL
url = "https://jsonplaceholder.typicode.com/users"

try:
    # Send the GET request
    response = requests.get(url, timeout=5)

    # Automatically raise an exception for HTTP errors
    response.raise_for_status()

    # Process the data
    print(f"Status Code: {response.status_code}")

    # If the server response is JSON, parse it into a Python dictionary
    data = response.json()
    print("\nResponse Data:")
    print(data)

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.Timeout:
    print("The request timed out.")
except Exception as err:
    print(f"An unexpected error occurred: {err}")