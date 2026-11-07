import unittest
try:
    from .analytics_error import AnalyticsError
    from .analytics_service import AnalyticsService
except ImportError:
    from analytics_error import AnalyticsError
    from analytics_service import AnalyticsService
class AnalyticsTests(unittest.TestCase):
    def test_total_emissions(self):
        records = [{"timestamp": "2026-01-01", "electricity_kwh": 120}]
        result = AnalyticsService().summarize(records)
        self.assertEqual(result["emissions_kg_co2e"], 48)
    def test_monthly_totals(self):
        records = [
            {"timestamp": "2026-01-01", "electricity_kwh": 120},
            {"timestamp": "2026-02-01", "electricity_kwh": 50},
        ]
        result = AnalyticsService().summarize(records)
        self.assertEqual(len(result["monthly"]), 2)
        self.assertEqual(result["monthly"][1]["emissions_kg_co2e"], 20)
    def test_empty_records(self):
        result = AnalyticsService().summarize([])
        self.assertEqual(result["record_count"], 0)
        self.assertEqual(result["monthly"], [])
    def test_zero_consumption(self):
        records = [{"timestamp": "2026-01-01", "electricity_kwh": 0}]
        self.assertEqual(AnalyticsService().summarize(records)["emissions_kg_co2e"], 0)
    def test_negative_consumption(self):
        records = [{"timestamp": "2026-01-01", "electricity_kwh": -10}]
        with self.assertRaises(AnalyticsError):
            AnalyticsService().summarize(records)
    def test_text_instead_of_consumption(self):
        records = [{"timestamp": "2026-01-01", "electricity_kwh": "abc"}]
        with self.assertRaises(AnalyticsError):
            AnalyticsService().summarize(records)
    def test_missing_consumption(self):
        records = [{"timestamp": "2026-01-01"}]
        with self.assertRaises(AnalyticsError):
            AnalyticsService().summarize(records)
    def test_negative_factor(self):
        with self.assertRaises(AnalyticsError):
            AnalyticsService(-0.1)
if __name__ == "__main__":
    unittest.main()
