import unittest

import config

import requests

from api_tester import test_api, validate_response, test_all_profiles, check_json_field
from profiles import load_profiles
from history import load_history, save_result
from statistics import show_statistics
from io import StringIO
from unittest.mock import patch

class TestApiWatchdog(unittest.TestCase):
    def test_api_success(self):
        result, status_code, response_time, response_valid, field_valid = test_api(
            "https://jsonplaceholder.typicode.com/users", ""
        )

        self.assertEqual(result, "PASS")
        self.assertEqual(status_code, 200)
        self.assertIsNotNone(response_time)

    def test_api_invalid_url(self):
        result, status_code, response_time = test_api(
            "not-a-valid-url", ""
        )

        self.assertIsNone(result)
        self.assertIsNone(status_code)
        self.assertIsNone(response_time)

    def test_api_empty_url(self):
        result, status_code, response_time = test_api("", "")

        self.assertIsNone(result)
        self.assertIsNone(status_code)
        self.assertIsNone(response_time)

    def test_api_not_found(self):
        result, status_code, response_time, response_valid, field_valid = test_api(
            "https://jsonplaceholder.typicode.com/invalid-endpoint", ""
        )

        self.assertEqual(result, "FAIL")
        self.assertEqual(status_code, 404)
        self.assertIsNotNone(response_time)

    def test_api_server_error(self):
        result, status_code, response_time, response_valid, field_valid = test_api(
            "https://httpbin.org/status/500", ""
        )

        self.assertEqual(result, "FAIL")
        self.assertEqual(status_code, 500)
        self.assertIsNotNone(response_time)

    def test_load_profiles(self):
        profiles = load_profiles()

        self.assertIsInstance(profiles, dict)
        self.assertIn("JSONPlaceholder Users", profiles)
        self.assertIn("JSONPlaceholder Posts", profiles)

    def test_save_result(self):
        import os
        import tempfile

        history_file = os.path.join(
            tempfile.gettempdir(),
            "test_api_history.csv"
        )

        if os.path.exists(history_file):
            os.remove(history_file)

        save_result(
            history_file,
            "2026-09-06 19:00:00",
            "https://example.com",
            "PASS",
            200,
            100,
            True,
            "",
            True
        )

        rows = load_history(history_file)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "https://example.com")
        self.assertEqual(rows[0][2], "PASS")
        self.assertEqual(rows[0][3], "200")
        self.assertEqual(rows[0][4], "100")

        os.remove(history_file)

    def test_load_empty_history(self):
        import os
        import tempfile

        history_file = os.path.join(
            tempfile.gettempdir(),
            "empty_api_history.csv"
        )

        if os.path.exists(history_file):
            os.remove(history_file)

        rows = load_history(history_file)

        self.assertEqual(rows, [])

    def test_empty_statistics(self):
        rows = []

        show_statistics(rows)

        self.assertEqual(len(rows), 0)

    def test_statistics_with_data(self):
        rows = [
            [
                "2026-09-06 19:00:00",
                "https://example.com",
                "PASS",
                "200",
                "100",
                "PASS"
            ],
            [
                "2026-09-06 19:01:00",
                "https://example.com",
                "FAIL",
                "500",
                "300",
                "FAIL"
            ]
        ]

        with patch("sys.stdout", new=StringIO()) as output:
            show_statistics(rows)

        self.assertIn("Invalid Responses: 1", output.getvalue())

    def test_profile_urls(self):
        profiles = load_profiles()

        self.assertEqual(
            profiles["JSONPlaceholder Users"],
            "https://jsonplaceholder.typicode.com/users"
        )

        self.assertEqual(
            profiles["JSONPlaceholder Posts"],
            "https://jsonplaceholder.typicode.com/posts"
        )

    def test_set_slow_response_threshold(self):
        original_threshold = config.slow_response_threshold

        config.set_slow_response_threshold(300)

        self.assertEqual(config.slow_response_threshold, 300)

        config.set_slow_response_threshold(original_threshold)

    def test_load_settings(self):
        config.set_slow_response_threshold(300)

        config.slow_response_threshold = 500

        config.load_settings()

        self.assertEqual(config.slow_response_threshold, 300)

    def test_slow_response_threshold(self):
        original_threshold = config.slow_response_threshold

        config.set_slow_response_threshold(200)

        rows = [
            [
                "2026-09-06 19:00:00",
                "https://example.com",
                "PASS",
                "200",
                "300"
            ]
        ]

        self.assertGreater(
            int(rows[0][4]),
            config.slow_response_threshold
        )

        config.set_slow_response_threshold(original_threshold)

    def test_validate_response(self):
        response = requests.get(
            "https://jsonplaceholder.typicode.com/users"
        )

        self.assertTrue(validate_response(response))

    def test_validate_invalid_response(self):
        response = requests.get(
            "https://example.com"
        )

        self.assertFalse(validate_response(response))

    def test_check_json_field_list_valid(self):
        response = unittest.mock.Mock()
        response.json.return_value = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Jane"}
        ]

        self.assertTrue(check_json_field(response, "id"))

    def test_check_json_field_list_missing(self):
        response = unittest.mock.Mock()
        response.json.return_value = [
            {"id": 1, "name": "John"},
            {"name": "Jane"}
        ]

        self.assertFalse(check_json_field(response, "id"))

    def test_check_json_field_empty_list(self):
        response = unittest.mock.Mock()
        response.json.return_value = []

        self.assertFalse(check_json_field(response, "id"))

    def test_check_json_field_dict_valid(self):
        response = unittest.mock.Mock()
        response.json.return_value = {
            "id": 1,
            "name": "John"
        }

        self.assertTrue(check_json_field(response, "id"))

    def test_check_json_field_dict_missing(self):
        response = unittest.mock.Mock()
        response.json.return_value = {
            "name": "John"
        }

        self.assertFalse(check_json_field(response, "id"))

    def test_check_json_field_unexpected_type(self):
        response = unittest.mock.Mock()
        response.json.return_value = "not a dictionary or list"

        self.assertFalse(check_json_field(response, "id"))

    def test_check_json_field_empty_field(self):
        response = unittest.mock.Mock()

        self.assertTrue(check_json_field(response, ""))

    def test_api_field_valid(self):
        result, status_code, response_time, response_valid, field_valid = test_api(
            "https://jsonplaceholder.typicode.com/users",
            "id"
        )

        self.assertEqual(result, "PASS")
        self.assertTrue(response_valid)
        self.assertTrue(field_valid)

    def test_api_field_invalid(self):
        result, status_code, response_time, response_valid, field_valid = test_api(
            "https://jsonplaceholder.typicode.com/users",
            "foobar"
        )

        self.assertEqual(result, "FAIL")
        self.assertTrue(response_valid)
        self.assertFalse(field_valid)

    def test_all_profiles(self):
        import os
        import tempfile

        history_file = os.path.join(
            tempfile.gettempdir(),
            "test_all_profiles_history.csv"
        )

        if os.path.exists(history_file):
            os.remove(history_file)

        test_all_profiles(history_file)

        rows = load_history(history_file)

        self.assertEqual(len(rows), 2)

        os.remove(history_file)

    def test_invalid_response_filter(self):
        rows = [
            [
                "2026-09-06 17:33:33",
                "https://example.com",
                "FAIL",
                "200",
                "111",
                "FAIL"
            ],
            [
                "2026-09-06 17:26:53",
                "https://jsonplaceholder.typicode.com/users",
                "PASS",
                "200",
                "112",
                "PASS"
            ]
        ]

        invalid_rows = [
            row for row in rows
            if len(row) > 5 and row[5] == "FAIL"
        ]

        self.assertEqual(len(invalid_rows), 1)
        self.assertEqual(invalid_rows[0][1], "https://example.com")