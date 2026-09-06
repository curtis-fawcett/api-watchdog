import config


def show_statistics(rows):
    """Display statistics for the API test history."""
    total_tests = len(rows)
    passed_tests = 0
    slow_responses = 0
    total_response_time = 0
    invalid_responses = 0

    fastest_response_time = None
    slowest_response_time = None
    fastest_url = None
    slowest_url = None

    url_counts = {}
    status_counts = {}

    for row in rows:
        url = row[1]
        status_code = row[3]
        response_time = int(row[4])

        if row[2] == "PASS":
            passed_tests += 1

        if len(row) > 5 and row[5] == "FAIL":
            invalid_responses += 1

        total_response_time += response_time

        if response_time > config.slow_response_threshold:
            slow_responses += 1

        if fastest_response_time is None or response_time < fastest_response_time:
            fastest_response_time = response_time
            fastest_url = url

        if slowest_response_time is None or response_time > slowest_response_time:
            slowest_response_time = response_time
            slowest_url = url

        url_counts[url] = url_counts.get(url, 0) + 1
        status_counts[status_code] = status_counts.get(status_code, 0) + 1

    failed_tests = total_tests - passed_tests

    if total_tests == 0:
        pass_rate = 0
        average_response_time = 0
        slow_response_rate = 0
    else:
        pass_rate = round(passed_tests / total_tests * 100, 1)
        average_response_time = round(total_response_time / total_tests, 1)
        slow_response_rate = round(slow_responses / total_tests * 100, 1)

    print("Total Tests:", total_tests)
    print("Passed:", passed_tests)
    print("Failed:", failed_tests)
    print("Invalid Responses:", invalid_responses)
    print("Pass Rate:", pass_rate, "%")
    print("Average Response Time:", average_response_time, "ms")
    print(
        "Slow Responses",
        f"(> {config.slow_response_threshold} ms):",
        slow_responses,
    )
    print("Slow Response Rate:", slow_response_rate, "%")

    if total_tests == 0:
        print("No response time data available")
        print("No status code data available")
        print("No URL data available")
        return

    print("Fastest Response Time:", fastest_response_time, "ms")
    print("Slowest Response Time:", slowest_response_time, "ms")
    print("Fastest URL:", fastest_url)
    print("Slowest URL:", slowest_url)

    print("Status Code Counts:")
    for status_code, count in status_counts.items():
        print(status_code, ":", count)

    most_common_status = max(status_counts, key=status_counts.get)
    print("Most Common Status Code:", most_common_status)
    print("Occurrences:", status_counts[most_common_status])

    print("URL Test Counts:")
    for url, count in url_counts.items():
        print(url, ":", count)

    most_tested_url = max(url_counts, key=url_counts.get)
    print("Most Tested URL:", most_tested_url)
    print("Times Tested:", url_counts[most_tested_url])