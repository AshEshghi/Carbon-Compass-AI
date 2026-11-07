
import unittest
from unittest.mock import patch, MagicMock

from Web_Interface.flask_app import app


class TestWebInterface(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # Test 1: Dashboard displays electricity data
    @patch("Web_Interface.flask_app.get_connection")
    def test_home_page(self, mock_connection):
        cursor = MagicMock()
        cursor.fetchall.return_value = [{
            "record_date": "2026-01-01",
            "electricity_kwh": 120
        }]
        mock_connection.return_value.cursor.return_value = cursor

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Energy Consumption Dashboard", response.data)
        self.assertIn(b"120", response.data)

    # Test 2: Data Management records appear in the interface
    @patch("Web_Interface.flask_app.json.load")
    @patch("Web_Interface.flask_app.urlopen")
    def test_sahra_records_page(self, mock_urlopen, mock_json):
        mock_json.return_value = [{
            "record_id": 1,
            "building_id": 1,
            "timestamp": "2026-01-01",
            "electricity_kwh": 150
        }]

        response = self.client.get("/sahra-records")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Data Management Records", response.data)
        self.assertIn(b"150", response.data)

    # Test 3: Analytics results appear in the interface
    @patch("Web_Interface.flask_app.json.load")
    @patch("Web_Interface.flask_app.urlopen")
    def test_analytics_page(self, mock_urlopen, mock_json):
        mock_json.return_value = {
            "building_id": 1,
            "total_electricity_kwh": 270,
            "emissions_kg_co2e": 108,
            "emissions_tonnes_co2e": 0.108
        }

        response = self.client.get("/analytics")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Carbon Analytics", response.data)
        self.assertIn(b"108", response.data)


if __name__ == "__main__":
    unittest.main()
