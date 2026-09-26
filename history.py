import csv
import os

import config
from statistics import show_statistics


def load_history(history_file):
    """Load API test history from the CSV file."""
    rows = []

    if not os.path.exists(history_file):
        return rows

    with open(history_file, "r", newline="") as file:
        reader = csv.reader(file)

        next(reader, None)

        for row in reader:
            rows.append(row)

    return rows


def save_result(
    history_file,
    timestamp,
    url,
    test_result,
    status_code,
    response_time,
    response_valid,
    field_name,
    field_valid
):
    """Save an API test result to the CSV history file."""
    file_exists = os.path.exists(history_file)

    with open(history_file, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date & Time",
                "URL",
                "Test Result",
                "Status Code",
                "Response Time",
                "Response Validation",
                "JSON Field",
                "Field Validation"
            ])

        writer.writerow([
            timestamp,
            url,
            test_result,
            status_code,
            response_time,
            "PASS" if response_valid else "FAIL",
            field_name,
            "PASS" if field_valid else "FAIL"
        ])


def print_history_row(row):
    """Display one API test history record."""
    response_validation = row[5] if len(row) > 5 else "N/A"
    json_field = row[6] if len(row) > 6 else "N/A"
    field_validation = row[7] if len(row) > 7 else "N/A"

    print(
        f"Date & Time: {row[0]} | "
        f"URL: {row[1]} | "
        f"Result: {row[2]} | "
        f"Status: {row[3]} | "
        f"Response Time: {row[4]} ms | "
        f"Response Validation: {response_validation} | "
        f"JSON Field: {json_field} | "
        f"Field Validation: {field_validation}"
    )


def show_all_tests(rows):
    """Display all API test history."""
    print("All tests")

    if rows:
        for row in rows:
            print_history_row(row)
    else:
        print("No history found")


def show_failed_tests(rows):
    """Display failed API tests."""
    print("Failed tests")

    matching_rows = [
        row for row in rows
        if len(row) > 2 and row[2] != "PASS"
    ]

    if not matching_rows:
        print("No failed tests found.")
        return

    for row in matching_rows:
        print_history_row(row)


def show_passed_tests(rows):
    """Display passed API tests."""
    print("Passed tests")

    matching_rows = [
        row for row in rows
        if len(row) > 2 and row[2] == "PASS"
    ]

    if not matching_rows:
        print("No passed tests found.")
        return

    for row in matching_rows:
        print_history_row(row)


def last_5_tests(rows):
    """Display the five most recent API tests."""
    print("Last 5 tests")

    if not rows:
        print("No history found")
        return

    for row in rows[-5:]:
        print_history_row(row)


def search_by_url(rows):
    """Search API history by URL keyword."""
    print("Search by URL")

    search_term = input("Enter URL keyword: ").strip()

    if not search_term:
        print("Search cannot be empty.")
        return

    matching_rows = [
        row for row in rows
        if len(row) > 1 and search_term.lower() in row[1].lower()
    ]

    if not matching_rows:
        print("No matching URLs found.")
        return

    for row in matching_rows:
        print_history_row(row)


def search_by_statuscode(rows):
    """Search API history by status code."""
    print("Search by Status Code")

    search_code = input("Enter Status Code: ").strip()

    if not search_code:
        print("Status code cannot be empty.")
        return

    matching_rows = [
        row for row in rows
        if len(row) > 3 and row[3] == search_code
    ]

    if not matching_rows:
        print("No matching Status Code found.")
        return

    for row in matching_rows:
        print_history_row(row)


def search_by_json_field(rows):
    """Search API history by JSON field."""
    print("Search by JSON Field")

    field_name = input("Enter JSON field: ").strip()

    matching_rows = [
        row for row in rows
        if len(row) > 6 and row[6] == field_name
    ]

    if not matching_rows:
        print("No matching tests found.")
        return

    for row in matching_rows:
        print_history_row(row)


def search_by_field(rows):
    """Search API history by field validation result."""
    print("Search by Field Validation")

    field_validation = input(
        "Enter PASS or FAIL: "
    ).strip().upper()

    if field_validation not in ("PASS", "FAIL"):
        print("Please enter PASS or FAIL.")
        return

    matching_rows = [
        row for row in rows
        if len(row) > 7 and row[7] == field_validation
    ]

    if not matching_rows:
        print("No matching validation found.")
        return

    for row in matching_rows:
        print_history_row(row)


def search_by_date(rows):
    """Search API history by date."""
    print("Search by Date")

    search_date = input("Enter a date: ").strip()

    if not search_date:
        print("Date cannot be empty.")
        return

    matching_rows = [
        row for row in rows
        if len(row) > 0 and row[0].split()[0] == search_date
    ]

    if not matching_rows:
        print("No records found for that date.")
        return

    for row in matching_rows:
        print_history_row(row)


def show_slow_responses(rows):
    """Display API tests that exceeded the slow response threshold."""
    print("Show Slow Responses")

    matching_rows = [
        row for row in rows
        if len(row) > 4
        and row[4]
        and int(row[4]) > config.slow_response_threshold
    ]

    if not matching_rows:
        print("No slow responses found.")
        return

    for row in matching_rows:
        print_history_row(row)


def show_fastest_test(rows):
    """Display the five fastest API tests."""
    print("Top 5 Fastest Tests")

    valid_rows = [
        row for row in rows
        if len(row) > 4 and row[4]
    ]

    if not valid_rows:
        print("No history found")
        return

    for row in sorted(valid_rows, key=lambda row: int(row[4]))[:5]:
        print_history_row(row)


def show_slowest_test(rows):
    """Display the five slowest API tests."""
    print("Top 5 Slowest Tests")

    valid_rows = [
        row for row in rows
        if len(row) > 4 and row[4]
    ]

    if not valid_rows:
        print("No history found")
        return

    for row in sorted(
        valid_rows,
        key=lambda row: int(row[4]),
        reverse=True
    )[:5]:
        print_history_row(row)


def show_last_failed(rows):
    """Display the most recent failed API test."""
    print("Last Failed Test")

    for row in reversed(rows):
        if len(row) > 2 and row[2] != "PASS":
            print_history_row(row)
            return

    print("No failed tests found.")


def show_invalid_response(rows):
    """Display API tests with invalid responses."""
    print("Show Invalid Responses")

    matching_rows = [
        row for row in rows
        if len(row) > 5 and row[5] == "FAIL"
    ]

    if not matching_rows:
        print("No invalid responses found.")
        return

    for row in matching_rows:
        print_history_row(row)


def show_statistics_history(rows):
    """Display API test statistics."""
    print("Statistics")

    if rows:
        show_statistics(rows)
    else:
        print("No history found")


def clear_history(history_file):
    """Clear all API test history."""
    print("Clear Test History")

    while True:
        user_input = input(
            "Are you sure you want to clear all test history? (yes/no): "
        ).strip().lower()

        if user_input == "yes":
            with open(history_file, "w", newline="") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "Date & Time",
                    "URL",
                    "Test Result",
                    "Status Code",
                    "Response Time",
                    "Response Validation",
                    "JSON Field",
                    "Field Validation"
                ])

            print("History has been cleared")
            break

        elif user_input == "no":
            break

        else:
            print("Please enter yes or no")


def show_history(history_file):
    """Display the API test history menu and handle selections."""
    while True:
        print("API Test History")
        print()
        print("1. All tests")
        print("2. Failed tests")
        print("3. Passed tests")
        print("4. Last 5 tests")
        print("5. Statistics")
        print("6. Search by URL")
        print("7. Search by Status Code")
        print("8. Show Slow Responses")
        print("9. Top 5 Fastest Tests")
        print("10. Top 5 Slowest Tests")
        print("11. Search by JSON Field")
        print("12. Search by Field Validation")
        print("13. Search by Date")
        print("14. Last Failed Test")
        print("15. Show Invalid Responses")
        print("16. Clear Test History")
        print("17. Back to main menu")

        history_choice = input("Choose an option: ").strip()
        rows = load_history(history_file)
        print()

        if history_choice == "1":
            show_all_tests(rows)

        elif history_choice == "2":
            show_failed_tests(rows)

        elif history_choice == "3":
            show_passed_tests(rows)

        elif history_choice == "4":
            last_5_tests(rows)

        elif history_choice == "5":
            show_statistics_history(rows)

        elif history_choice == "6":
            search_by_url(rows)

        elif history_choice == "7":
            search_by_statuscode(rows)

        elif history_choice == "8":
            show_slow_responses(rows)

        elif history_choice == "9":
            show_fastest_test(rows)

        elif history_choice == "10":
            show_slowest_test(rows)

        elif history_choice == "11":
            search_by_json_field(rows)

        elif history_choice == "12":
            search_by_field(rows)

        elif history_choice == "13":
            search_by_date(rows)

        elif history_choice == "14":
            show_last_failed(rows)

        elif history_choice == "15":
            show_invalid_response(rows)

        elif history_choice == "16":
            clear_history(history_file)

        elif history_choice == "17":
            return

        else:
            print("Please choose an option from the history menu")