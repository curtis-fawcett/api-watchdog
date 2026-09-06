import unittest

from api_tester import test_api


class TestApiWatchdog(unittest.TestCase):
    def test_api_success(self):
        result, status_code, response_time = test_api(
            "https://jsonplaceholder.typicode.com/users"
        )

        self.assertEqual(result, "PASS")
        self.assertEqual(status_code, 200)
        self.assertIsNotNone(response_time)