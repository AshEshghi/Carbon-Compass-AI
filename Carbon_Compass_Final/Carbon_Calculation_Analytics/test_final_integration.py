import csv
import unittest
from pathlib import Path
from Carbon_Calculation_Analytics.integration import calculate_2016_records
from Carbon_Calculation_Analytics.analytics_service import AnalyticsService
from Carbon_Calculation_Analytics.streaming_adapter import electricity_events, make_processors
from Carbon_Calculation_Analytics.api.analytics_service import AnalyticsService as ApiAnalyticsService


class FinalIntegrationTests(unittest.TestCase):
    def test_streaming_2016(self):
        rows = [{"record_id": 1, "building_id": 1, "timestamp": "2016-01-01", "electricity_kwh": 120}]
        event = next(electricity_events(rows))
        scope_filter, transformer = make_processors()
        output = transformer.process(scope_filter.process(event))
        self.assertEqual(output["emissions_kg_co2e"], 48)

    def test_2016_sample(self):
        rows = [{"record_id": 1, "building_id": 1, "timestamp": "2016-01-01", "electricity_kwh": 120}]
        summary, monthly = calculate_2016_records(rows)
        self.assertEqual(summary["total_emissions_kgco2e"], 48)
        self.assertEqual(monthly, {"2016-01": 48})

    def test_reject_2026_test_records(self):
        rows = [{"record_id": 1, "building_id": 1, "timestamp": "2026-01-01", "electricity_kwh": 120}]
        with self.assertRaises(ValueError):
            calculate_2016_records(rows)

    def test_reject_late_2016(self):
        rows = [{"record_id": 1, "building_id": 1, "timestamp": "2016-10-01", "electricity_kwh": 120}]
        with self.assertRaises(ValueError):
            calculate_2016_records(rows)

    def test_api_and_dashboard_calculations_agree(self):
        rows = [
            {"record_id": 1, "building_id": 1, "timestamp": "2016-01-01", "electricity_kwh": 120},
            {"record_id": 2, "building_id": 1, "timestamp": "2016-02-01", "electricity_kwh": 150},
        ]
        dashboard, months = calculate_2016_records(rows)
        api = ApiAnalyticsService().summarize(rows)
        self.assertEqual(api["emissions_kg_co2e"], dashboard["total_emissions_kgco2e"])
        self.assertEqual({m["month"]: m["emissions_kg_co2e"] for m in api["monthly"]}, months)

    def test_api_rejects_2026_record_without_sql_filter(self):
        rows = [{"timestamp": "2026-01-01", "electricity_kwh": 120}]
        with self.assertRaises(ValueError):
            ApiAnalyticsService().summarize(rows)

    def test_mismatched_building(self):
        rows = [{"record_id": 1, "building_id": 2, "timestamp": "2016-01-01", "electricity_kwh": 120}]
        with self.assertRaises(ValueError):
            calculate_2016_records(rows)
