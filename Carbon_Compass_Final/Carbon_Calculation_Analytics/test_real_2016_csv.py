"""Check the team's final 2016 CSV without connecting to MySQL."""
import csv
import unittest
from pathlib import Path

from Carbon_Calculation_Analytics.integration import calculate_2016_records
from Carbon_Calculation_Analytics.api.analytics_service import AnalyticsService as ApiAnalyticsService


class FinalCsvTests(unittest.TestCase):
    def test_real_csv_matches_expected_analytics(self):
        csv_path = (Path(__file__).absolute().parent.parent
                    / "Data_Management" / "carbon_compass_real_daily_building1.csv")
        if not csv_path.is_file():
            self.skipTest("Place Sahra's 2016 CSV in the sibling Data_Management folder")

        with csv_path.open(newline="", encoding="utf-8-sig") as source:
            records = [
                {"record_id": i, "building_id": 1, **row}
                for i, row in enumerate(csv.DictReader(source), start=1)
            ]

        dashboard, dashboard_months = calculate_2016_records(records)
        api = ApiAnalyticsService().summarize(records, building_id=1)

        self.assertEqual(len(records), 274)
        self.assertEqual(dashboard["record_count"], 274)
        self.assertEqual(api["record_count"], 274)
        self.assertEqual(len(dashboard_months), 9)
        self.assertEqual(len(api["monthly"]), 9)
        self.assertAlmostEqual(dashboard["total_electricity_kwh"], 1396657.011875, places=4)
        self.assertAlmostEqual(dashboard["total_emissions_kgco2e"], 558662.80475, places=4)
        self.assertAlmostEqual(api["emissions_kg_co2e"], 558662.80475, places=2)


if __name__ == "__main__":
    unittest.main()
