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

def search_by_json_field(rows):
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
    print("Search by Field Validation")

    field_validation = input("Enter PASS or FAIL: ").strip().upper()

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
    print("Search by Date")

    search_date = input("Enter a date: ").strip()

    found_date = False

    for row in rows:
        if row and row[0].split()[0] == search_date:
            print_history_row(row)
            found_date = True

    if not found_date:
        print("No records found for that date.")

def show_all_tests(rows):
    """Display all API test history."""
    print("All tests")

    if rows:
        for row in rows:
            print_history_row(row)
    else:
        print("No history found")

def show_failed_tests(rows):
    print("Failed tests")

    if rows:
        failed_found = False

        for row in rows:
            if row[2] != "PASS":
                failed_found = True
                print_history_row(row)

        if not failed_found:
            print("No failed tests found")
    else:
        print("No history found")

def show_passed_tests(rows):
    print("Passed tests")

    if rows:
        passed_found = False

        for row in rows:
            if row[2] == "PASS":
                passed_found = True
                print_history_row(row)

        if not passed_found:
            print("No passed tests found")
    else:
        print("No history found")

def last_5_tests(rows):
    print("Last 5 tests")

    if rows:
        for row in rows[-5:]:
            print_history_row(row)
    else:
        print("No history found")

def search_by_url(rows):
    print("Search by URL")

    search_term = input("Enter URL keyword: ").strip()

    if not search_term:
        print("Search cannot be empty")
    else:
        match_found = False

        for row in rows:
            if search_term.lower() in row[1].lower():
                match_found = True
                print_history_row(row)

        if not match_found:
            print("No matching URLs found")

def search_by_statuscode(rows):
    print("Search by Status Code")

    search_code = input("Enter Status Code: ").strip()

    if not search_code:
        print("Status code cannot be empty")
    else:
        code_match_found = False

        for row in rows:
            if search_code == row[3]:
                code_match_found = True
                print_history_row(row)

        if not code_match_found:
            print("No matching Status Code found")

def show_slow_responses(rows):
    print("Show Slow Responses")

    slow_response_found = False

    for row in rows:
        response_time = int(row[4])

        if response_time > config.slow_response_threshold:
            slow_response_found = True
            print_history_row(row)

    if not slow_response_found:
        print("No slow responses found")

def show_fastest_test(rows):
    print("Top 5 Fastest Tests")

    if rows:
        for row in sorted(rows, key=lambda row: int(row[4]))[:5]:
            print_history_row(row)
    else:
        print("No history found")

def show_slowest_test(rows):
    print("Top 5 Slowest Tests")

    if rows:
        for row in sorted(
                rows,
                key=lambda row: int(row[4]),
                reverse=True
        )[:5]:
            print_history_row(row)
    else:
        print("No history found")

def show_last_failed(rows):
    print("Last Failed Test")

    if rows:
        failed_found = False

        for row in reversed(rows):
            if row[2] != "PASS":
                failed_found = True
                print_history_row(row)
                break

        if not failed_found:
            print("No failed tests found")
    else:
        print("No history found")

def show_invalid_response(rows):
    print("Show Invalid Responses")

    invalid_response_found = False

    for row in rows:
        if len(row) > 5 and row[5] == "FAIL":
            invalid_response_found = True
            print_history_row(row)

    if not invalid_response_found:
        print("No invalid responses found")

def clear_history(history_file):
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

def show_statistics_history(rows):
    print("Statistics")

    if rows:
        show_statistics(rows)
    else:
        print("No history found")

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