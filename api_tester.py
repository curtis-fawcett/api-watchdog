from datetime import datetime

import requests

import config
from history import save_result
from profiles import load_profiles


def test_api(url, field_name):
    """Test an API URL and return the result, status code, and response time."""
    url = url.strip()

    if not url:
        print("URL cannot be empty")
        return None, None, None, False, False

    try:
        response = requests.get(url, timeout=5)

    except requests.exceptions.ConnectionError:
        print("Connection failed")
        return None, None, None, False, False

    except requests.exceptions.Timeout:
        print("Connection timed out")
        return None, None, None, False, False

    except requests.exceptions.MissingSchema:
        print("Invalid URL. Include http:// or https://")
        return None, None, None, False, False

    except requests.exceptions.RequestException:
        print("Request failed")
        return None, None, None, False, False

    response_time = int(response.elapsed.total_seconds() * 1000)

    response_valid = validate_response(response)

    if response_valid:
        field_valid = check_json_field(response, field_name)
    else:
        field_valid = False

    result = (
        "PASS"
        if 200 <= response.status_code < 300
           and response_valid
           and field_valid
        else "FAIL"
    )

    return result, response.status_code, response_time, response_valid, field_valid


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

    for profile_name, profile_data in profiles_data.items():
        total_tests += 1

        url = profile_data["url"]
        field_name = profile_data["field"]

        test_result, status_code, response_time, response_valid, field_valid = test_api(
            url,
            field_name
        )

        if response_time is not None:
            total_response_time += response_time
            successful_tests += 1

        if test_result == "PASS":
            passed_tests += 1
        elif test_result == "FAIL":
            failed_tests += 1

        if test_result is None:
            failed_tests += 1

        if test_result is not None and not response_valid:
            invalid_responses += 1

        if test_result is not None:
            save_test_result(
                history_file,
                url,
                test_result,
                status_code,
                response_time,
                response_valid,
                field_name,
                field_valid
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


def print_test_result(
    test_result,
    status_code,
    response_time,
    response_valid,
    field_valid
):
    """Display the results of a single API test."""
    if test_result is None:
        print("Test could not be completed")
        return

    print("Result:", test_result)
    print("Status Code:", status_code)
    print("Response Time:", response_time, "ms")
    print("Response Validation:", "PASS" if response_valid else "FAIL")
    print("Field Validation:", "PASS" if field_valid else "FAIL")

    if response_time > config.slow_response_threshold:
        print("Warning: Slow response")


def save_test_result(
    history_file,
    url,
    test_result,
    status_code,
    response_time,
    response_valid,
    field_name,
    field_valid
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
        response_valid,
        field_name,
        field_valid
    )


def run_single_test(history_file, url, field_name):
    """Run one API test, save the result, and display the outcome."""
    test_result, status_code, response_time, response_valid, field_valid = test_api(url, field_name)

    if test_result is not None:
        save_test_result(
            history_file,
            url,
            test_result,
            status_code,
            response_time,
            response_valid,
            field_name,
            field_valid
        )

    print_test_result(
        test_result,
        status_code,
        response_time,
        response_valid,
        field_valid
    )


def run_api_test(history_file):
    """Display the API test menu and run the selected test."""
    while True:
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
                continue

            for number, profile_name in enumerate(profiles_data, start=1):
                print(f"{number}. {profile_name}")

            profile_names = list(profiles_data.keys())

            while True:
                profile_selection = input(
                    "Enter profile number (or 0 to go back): "
                ).strip()

                try:
                    profile_number = int(profile_selection)

                    if profile_number == 0:
                        break

                    if profile_number < 1 or profile_number > len(profile_names):
                        print("Invalid profile number.")
                        continue

                    profile_name = profile_names[profile_number - 1]
                    profile_data = profiles_data[profile_name]
                    url = profile_data["url"]
                    field_name = profile_data["field"]
                    run_single_test(history_file, url, field_name)
                    break

                except ValueError:
                    print("Please enter a valid number.")

        elif test_choice == "2":
            url = input("Enter API URL (or 0 to go back): ").strip()

            if url == "0":
                continue

            while not url:
                print("URL cannot be empty.")
                url = input("Enter API URL (or 0 to go back): ").strip()

                if url == "0":
                    break

            if url == "0":
                continue

            while not url.startswith(("http://", "https://")):
                print("URL must start with http:// or https://")
                url = input("Enter API URL (or 0 to go back): ").strip()

                if url == "0":
                    break

            if url == "0":
                continue

            field_name = input("Enter JSON field to verify (optional, or 0 to go back): ").strip()

            if field_name == "0":
                continue

            run_single_test(history_file, url, field_name)

        elif test_choice == "3":
            test_all_profiles(history_file)

        elif test_choice == "4":
            return

        else:
            print("Invalid option.")


def check_json_field(response, field_name):
    if not field_name:
        return True

    json_data = response.json()

    if isinstance(json_data, list):
        if not json_data:
            return False
        return all(isinstance(user, dict) and field_name in user for user in json_data)

    if isinstance(json_data, dict):
        return field_name in json_data

    return False