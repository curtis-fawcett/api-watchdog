# API Watchdog

API Watchdog is a Python command-line tool for testing API endpoints, tracking test results, managing saved API profiles, and monitoring response times.

## Features

* Test individual API endpoints
* Test all saved API profiles
* Detect successful and failed HTTP responses
* Measure API response times
* Log API test results to CSV
* Save and manage API profiles using JSON
* Search test history by URL
* Search test history by status code
* View passed and failed tests
* View the latest tests
* Find slow API responses
* View the fastest and slowest responses
* View API testing statistics
* Configure the slow-response threshold
* Automated unit testing with Python's `unittest` framework

## Technologies

* Python
* Requests
* CSV
* JSON
* unittest

## Project Structure

```text
api_watchdog/
├── tests/
│   ├── __init__.py
│   └── test_api_watchdog.py
├── README.md
├── api_history.csv
├── api_tester.py
├── config.py
├── history.py
├── main.py
├── profiles.py
├── profiles.json
├── settings.py
├── settings.json
└── statistics.py
```

## Requirements

* Python 3.x
* Requests library

Install Requests with:

```bash
pip install requests
```

## Running the Application

From the project directory:

```bash
python main.py
```

The application provides options for:

1. Testing an API
2. Viewing test history
3. Managing API profiles
4. Configuring settings
5. Exiting the application

## Running Tests

Run the automated test suite from the project directory:

```bash
python -m unittest discover
```

## API Profiles

API Watchdog allows API endpoints to be saved as profiles so they can be tested without entering the URL each time.

Profiles are stored in:

```text
profiles.json
```

## Test History

Completed API tests are recorded in:

```text
api_history.csv
```

History can be viewed through the application and filtered by:

* Test result
* URL
* Status code
* Response time

## Configuration

API Watchdog includes a configurable slow-response threshold.

The setting is stored in:

```text
settings.json
```

Responses exceeding the configured threshold are identified as slow responses.

## Example

```text
API Watchdog

1. Test an API
2. View test history
3. API profiles
4. Settings
5. Exit
```

## Project Status

API Watchdog is an actively developed project. Current development focuses on improving automated testing, code quality, and additional API monitoring functionality.

## Future Improvements

Potential future improvements include:

* Expanded automated test coverage
* Support for additional HTTP methods
* API response validation
* Scheduled API monitoring
* Additional reporting features
* Notification and alerting capabilities
