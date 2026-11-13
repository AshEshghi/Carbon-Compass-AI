
import unittest
from unittest.mock import patch
from datetime import date

with patch("getpass.getpass", return_value="test_password"):
    from Data_Management.app import app


class TestDataManagement(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_missing_fields(self):
        response = self.client.post("/records", json={
            "building_id": 1
        })
        self.assertEqual(response.status_code, 400)

    def test_negative_consumption(self):
        response = self.client.post("/records", json={
            "building_id": 1,
            "timestamp": "2026-01-01",
            "electricity_kwh": -50
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "Electricity consumption cannot be negative"
        )

    def test_invalid_consumption(self):
        response = self.client.post("/records", json={
            "building_id": 1,
            "timestamp": "2026-01-01",
            "electricity_kwh": "abc"
        })
        self.assertEqual(response.status_code, 400)

    @patch("Data_Management.app.mysql.connector.connect")
    def test_get_records(self, mock_connect):
        cursor = mock_connect.return_value.cursor.return_value
        cursor.fetchall.return_value = [{
            "record_id": 1,
            "building_id": 1,
            "timestamp": date(2026, 1, 1),
            "electricity_kwh": 120.0
        }]

        response = self.client.get("/records")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()[0]["electricity_kwh"],
            120.0
        )


if __name__ == "__main__":
    unittest.main()
