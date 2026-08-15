import requests

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:
    print("PASS")
else:
    print("FAIL")

response_time = int(response.elapsed.total_seconds() * 1000)

print("Response Time:" , response_time, "ms")