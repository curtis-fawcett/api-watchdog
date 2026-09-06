from datetime import datetime

import requests

import config
from history import save_result
from profiles import load_profiles


def test_api(url):
    """Test an API URL and return the result, status code, and response time."""
    url = url.strip()

    if not url:
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

    except requests.exceptions.RequestException:
        print("Request failed")
        return None, None, None

    response_time = int(response.elapsed.total_seconds() * 1000)

    response_valid = validate_response(response)

    result = (
        "PASS"
        if 200 <= response.status_code < 300 and response_valid
        else "FAIL"
    )

    return result, response.status_code, response_time, response_valid


def validate_response(response):
    """Check whether an API response contains valid JSON."""
    try:
        response.json()
    except ValueError:
        return False

    return True


def test_all_profiles(history_file):
    """Test all saved API profiles and display a summary."""
    profiles_data = load_profiles()

    if not profiles_data:
        print("No profiles found. Please create a profile first.")
        return

    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    total_response_time = 0
    successful_tests = 0
    invalid_responses = 0

    for profile_name, api_url in profiles_data.items():
        total_tests += 1

        test_result, status_code, response_time, response_valid = test_api(api_url)

        if response_time is not None:
            total_response_time += response_time
            successful_tests += 1

        if test_result == "PASS":
            passed_tests += 1
        else:
            failed_tests += 1

        if not response_valid:
            invalid_responses += 1

        if test_result is not None:
            save_test_result(
                history_file,
                api_url,
                test_result,
                status_code,
                response_time,
                response_valid
            )

        if test_result is None:
            print(f"{profile_name} ........ FAILED")
        else:
            print(
                f"{profile_name} ........ {test_result} "
                f"(Response Validation: {'PASS' if response_valid else 'FAIL'}, "
                f"{response_time} ms)"
            )

    # Calculate average response time
    average_response_time = (
        total_response_time / successful_tests
        if successful_tests > 0
        else 0
    )

    print()
    print(f"{total_tests} APIs tested")
    print(f"{passed_tests} Passed")
    print(f"{failed_tests} Failed")
    print(f"{successful_tests} Responses received")
    print(f"{invalid_responses} Invalid Responses")
    print(f"Average Response Time: {round(average_response_time, 1)} ms")


def print_test_result(test_result, status_code, response_time, response_valid):
    """Display the results of a single API test."""
    if test_result is None:
        print("Test could not be completed")
        return

    print("Result:", test_result)
    print("Status Code:", status_code)
    print("Response Time:", response_time, "ms")
    print("Response Validation:", "PASS" if response_valid else "FAIL")

    if response_time > config.slow_response_threshold:
        print("Warning: Slow response")


def save_test_result(
    history_file,
    url,
    test_result,
    status_code,
    response_time,
    response_valid
):
    """Save a completed API test result to the history file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_result(
        history_file,
        timestamp,
        url,
        test_result,
        status_code,
        response_time,
        response_valid
    )


def run_single_test(history_file, url):
    """Run one API test, save the result, and display the outcome."""
    test_result, status_code, response_time, response_valid = test_api(url)

    if test_result is not None:
        save_test_result(
            history_file,
            url,
            test_result,
            status_code,
            response_time,
            response_valid
        )

    print_test_result(
        test_result,
        status_code,
        response_time,
        response_valid
    )


def run_api_test(history_file):
    """Display the API test menu and run the selected test."""
    print("Test an API")
    print()
    print("1. Use a saved profile")
    print("2. Enter a custom URL")
    print("3. Test all profiles")
    print("4. Back")

    test_choice = input("Choose an option: ").strip()

    if test_choice == "1":
        profiles_data = load_profiles()
        if not profiles_data:
            print("No profiles found. Please create a profile first.")
            return

        for number, (profile_name, api_url) in enumerate(profiles_data.items(), start=1):
            print(f"{number}. {profile_name}")

        profile_selection = input("Enter profile number: ").strip()
        try:
            profile_number = int(profile_selection)

            profile_names = list(profiles_data.keys())

            if profile_number < 1 or profile_number > len(profile_names):
                print("Invalid profile number.")
                return

            profile_name = profile_names[profile_number - 1]
            url = profiles_data[profile_name]

        except ValueError:
            print("Please enter a valid number.")
            return

    elif test_choice == "2":
        url = input("Enter API URL: ").strip()

    elif test_choice == "3":
        test_all_profiles(history_file)
        return

    elif test_choice == "4":
        return

    else:
        print("Invalid option.")
        return

    run_single_test(history_file, url)