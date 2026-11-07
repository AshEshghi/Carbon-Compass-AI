import unittest
from datetime import date
from unittest.mock import MagicMock, patch
from flask import Flask
from analytics_api import AnalyticsService, analytics_bp
class AnalyticsTests(unittest.TestCase):
    def test_emissions_and_monthly_totals(self):
        records = [
            {"timestamp": date(2026, 1, 1), "electricity_kwh": 120},
            {"timestamp": "2026-01-02", "electricity_kwh": 150},
            {"timestamp": "2026-02-01", "electricity_kwh": 100},
        ]
        result = AnalyticsService().summarize(records)
        self.assertEqual(result["total_electricity_kwh"], 370)
        self.assertEqual(result["emissions_kg_co2e"], 148)
        self.assertEqual(result["monthly"][0]["electricity_kwh"], 270)

    def test_empty_records(self):
        result = AnalyticsService().summarize([])
        self.assertEqual(result["total_electricity_kwh"], 0)
        self.assertEqual(result["monthly"], [])

    def test_invalid_consumption(self):
        with self.assertRaises(ValueError):
            AnalyticsService().summarize([{"timestamp": "2026-01-01", "electricity_kwh": -10}])

    def test_invalid_factor(self):
        with self.assertRaises(ValueError):
            AnalyticsService(-1)

    def test_flask_endpoint_with_mock_database(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["MYSQL_PASSWORD"] = "test-password"
        app.register_blueprint(analytics_bp)
        rows = [
            {"record_id": 1, "building_id": 1, "timestamp": date(2026, 1, 1), "electricity_kwh": 120},
        ]
        connection = MagicMock()
        connection.cursor.return_value.fetchall.return_value = rows
        with patch("analytics_api.mysql.connector.connect", return_value=connection):
            response = app.test_client().get("/analytics?building_id=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["emissions_kg_co2e"], 48)
        connection.cursor.return_value.execute.assert_called_once()

    def test_invalid_building_id(self):
        app = Flask(__name__)
        app.register_blueprint(analytics_bp)
        response = app.test_client().get("/analytics?building_id=abc")
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
