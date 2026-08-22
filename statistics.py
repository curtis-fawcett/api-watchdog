from config import slow_response_threshold

def show_statistics(rows):
    url_counts = {}
    fastest_url = None
    slowest_url = None
    most_tested_url = None
    times_tested = 0

    most_common_status = None
    highest_status_count = 0
    status_counts = {}

    total_tests = len(rows)
    passed_tests = 0

    total_response_time = 0
    fastest_response_time = None
    slowest_response_time = None
    slow_responses = 0

    for row in rows:
        response_time = int(row[4])

        if response_time > slow_response_threshold:
            slow_responses += 1

        url = row[1]
        status_code = row[3]

        if row[2] == "PASS":
            passed_tests += 1

        total_response_time += response_time

        if fastest_response_time is None or response_time < fastest_response_time:
            fastest_response_time = response_time
            fastest_url = url

        if slowest_response_time is None or response_time > slowest_response_time:
            slowest_response_time = response_time
            slowest_url = url

        if status_code in status_counts:
            status_counts[status_code] += 1
        else:
            status_counts[status_code] = 1

        if url in url_counts:
            url_counts[url] += 1
        else:
            url_counts[url] = 1

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
    print("Pass Rate:", pass_rate, "%")
    print("Average Response Time:", average_response_time, "ms")
    print("Slow Responses", "(>", slow_response_threshold, "ms):", slow_responses)
    print("Slow Response Rate:", slow_response_rate, "%")

    if total_tests == 0:
        print("No response time data available")
    else:
        print("Fastest Response Time:", fastest_response_time, "ms")
        print("Slowest Response Time:", slowest_response_time, "ms")
        print("Fastest URL:", fastest_url)
        print("Slowest URL:", slowest_url)
    print("Status Code Counts:")

    for status_code, count in status_counts.items():
        print(status_code, ":", count)

        if count > highest_status_count:
            highest_status_count = count
            most_common_status = status_code

    print("Most Common Status Code:", most_common_status)
    print("Occurrences:", highest_status_count)

    print("URL Test Counts:")

    for url, count in url_counts.items():
        print(url, ":", count)

        if count > times_tested:
            most_tested_url = url
            times_tested = count

    print("Most Tested URL:", most_tested_url)
    print("Times Tested:", times_tested)