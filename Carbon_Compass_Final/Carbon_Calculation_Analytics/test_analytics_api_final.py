"""Mocked Flask endpoint tests; a running MySQL server is not needed."""
import unittest
from datetime import date
from unittest.mock import patch

try:
    from flask import Flask
    import mysql.connector
    from Carbon_Calculation_Analytics.api.analytics_api import analytics_bp
    HAS_API_PACKAGES = True
except ImportError:
    HAS_API_PACKAGES = False


@unittest.skipUnless(HAS_API_PACKAGES, "Install Flask and mysql-connector-python first")
class FinalAnalyticsApiTests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.update(TESTING=True, MYSQL_PASSWORD="fake-password")
        app.register_blueprint(analytics_bp)
        self.client = app.test_client()
        self.app = app

    @patch("mysql.connector.connect")
    def test_get_analytics_and_date_filter(self, mock_connect):
        cursor = mock_connect.return_value.cursor.return_value
        cursor.fetchall.return_value = [
            {"record_id": 1, "building_id": 1,
             "timestamp": date(2016, 1, 1), "electricity_kwh": 120},
            {"record_id": 2, "building_id": 1,
             "timestamp": date(2016, 2, 1), "electricity_kwh": 150},
        ]
        response = self.client.get("/analytics?building_id=1")
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertEqual(result["record_count"], 2)
        self.assertEqual(result["emissions_kg_co2e"], 108)
        self.assertEqual(len(result["monthly"]), 2)

        sql, params = cursor.execute.call_args.args
        self.assertIn("timestamp >= %s AND timestamp < %s", sql)
        self.assertEqual(params, (1, "2016-01-01", "2016-10-01"))
        cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    def test_invalid_building_id(self):
        response = self.client.get("/analytics?building_id=abc")
        self.assertEqual(response.status_code, 400)

    @patch("mysql.connector.connect")
    def test_rejects_other_building(self, mock_connect):
        cursor = mock_connect.return_value.cursor.return_value
        cursor.fetchall.return_value = [
            {"record_id": 3, "building_id": 2,
             "timestamp": date(2016, 1, 1), "electricity_kwh": 120}
        ]
        response = self.client.get("/analytics?building_id=1")
        self.assertEqual(response.status_code, 422)

    @patch("mysql.connector.connect")
    def test_database_connection_failure(self, mock_connect):
        mock_connect.side_effect = mysql.connector.Error("offline")
        response = self.client.get("/analytics?building_id=1")
        self.assertEqual(response.status_code, 503)

    @patch("mysql.connector.connect")
    def test_invalid_database_row(self, mock_connect):
        cursor = mock_connect.return_value.cursor.return_value
        cursor.fetchall.return_value = [
            {"record_id": 1, "building_id": 1,
             "timestamp": date(2016, 1, 1), "electricity_kwh": -3}
        ]
        response = self.client.get("/analytics?building_id=1")
        self.assertEqual(response.status_code, 422)

    @patch("mysql.connector.connect")
    def test_rejects_test_year_if_query_returns_it(self, mock_connect):
        cursor = mock_connect.return_value.cursor.return_value
        cursor.fetchall.return_value = [
            {"record_id": 1, "building_id": 1,
             "timestamp": date(2026, 1, 1), "electricity_kwh": 120}
        ]
        response = self.client.get("/analytics?building_id=1")
        self.assertEqual(response.status_code, 422)

    @patch("mysql.connector.connect")
    def test_empty_dataset(self, mock_connect):
        mock_connect.return_value.cursor.return_value.fetchall.return_value = []
        response = self.client.get("/analytics?building_id=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["record_count"], 0)


if __name__ == "__main__":
    unittest.main()
