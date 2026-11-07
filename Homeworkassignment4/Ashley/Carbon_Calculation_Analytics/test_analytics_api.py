import unittest
from datetime import date
from unittest.mock import patch
from flask import Flask
import mysql.connector
try:
    from .analytics_api import analytics_bp
except ImportError:
    from analytics_api import analytics_bp
class AnalyticsApiTests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.update(TESTING=True, MYSQL_PASSWORD="test-password")
        app.register_blueprint(analytics_bp)
        self.client = app.test_client()

    @patch("mysql.connector.connect")
    def test_get_analytics(self, mock_connect):
        cursor = mock_connect.return_value.cursor.return_value
        cursor.fetchall.return_value = [
            {"record_id": 1, "building_id": 1,
             "timestamp": date(2026, 1, 1), "electricity_kwh": 120}
        ]
        response = self.client.get("/analytics?building_id=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["emissions_kg_co2e"], 48)

    def test_invalid_building_id(self):
        response = self.client.get("/analytics?building_id=abc")
        self.assertEqual(response.status_code, 400)

    @patch("mysql.connector.connect", side_effect=mysql.connector.Error("offline"))
    def test_database_connection_error(self, mock_connect):
        response = self.client.get("/analytics?building_id=1")
        self.assertEqual(response.status_code, 503)
if __name__ == "__main__":
    unittest.main()
