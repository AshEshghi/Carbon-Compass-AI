import unittest
from abc import ABC
from Data_Management.consumption_record import ConsumptionRecord
from Data_Management.csv_validation import validate_csv
from Carbon_Calculation_Analytics.analytics_service import AnalyticsService
from Carbon_Calculation_Analytics.carbon_calculator import BaseCalculator, CarbonCalculator
from Carbon_Calculation_Analytics.emission_factor import EmissionFactor
from pathlib import Path
def example_record(kwh=120, date="2026-01-01", record_id=1):
    return {"record_id": record_id, "building_id": 1,
            "timestamp": date, "electricity_kwh": kwh}
def example_factor():
    return EmissionFactor(1, "DEMO", 2026, 0.4, "Hypothetical test factor")
class CarbonAnalyticsTests(unittest.TestCase):
    def test_abstract_parent_class(self):
        self.assertTrue(issubclass(BaseCalculator, ABC))
        with self.assertRaises(TypeError):
            BaseCalculator()
    def test_calculates_from_dictionary(self):
        result = CarbonCalculator().calculate(example_record(), example_factor())
        self.assertEqual(result.get_kgco2e(), 48)
    def test_uses_sahras_shared_class(self):
        record = ConsumptionRecord(None, 1, "2026-01-01", 120)
        result = CarbonCalculator().calculate(record, example_factor())
        self.assertIsNone(result.get_record_id())
        self.assertEqual(result.get_kgco2e(), 48)
    def test_preserves_record_id(self):
        result = CarbonCalculator().calculate(example_record(record_id=7), example_factor())
        self.assertEqual(result.get_record_id(), 7)
    def test_rejects_negative_consumption(self):
        with self.assertRaises(ValueError):
            CarbonCalculator().calculate(example_record(kwh=-5), example_factor())
    def test_rejects_missing_field(self):
        record = example_record()
        del record["timestamp"]
        with self.assertRaises(ValueError):
            CarbonCalculator().calculate(record, example_factor())
    def test_rejects_invalid_factor_year(self):
        factor = example_factor()
        factor.set_year(2025)
        with self.assertRaises(ValueError):
            CarbonCalculator().calculate(example_record(), factor)
    def test_getters_and_setters(self):
        factor = example_factor()
        factor.set_kgco2e_per_kwh(0.5)
        self.assertEqual(factor.get_kgco2e_per_kwh(), 0.5)
    def test_aggregation_and_summary(self):
        calculator = CarbonCalculator()
        records = [example_record(1200, "2026-01-01", 1),
                   example_record(1000, "2026-02-01", 2),
                   example_record(900, "2026-03-01", 3)]
        results = [calculator.calculate(record, example_factor()) for record in records]
        service = AnalyticsService(results)
        self.assertEqual(service.calculate_total(), 1240)
        self.assertEqual(service.aggregate_monthly(),
                         {"2026-01": 480, "2026-02": 400, "2026-03": 360})
        self.assertEqual(service.summary()["total_electricity_kwh"], 3100)
        self.assertEqual(service.summary()["total_emissions_kgco2e"], 1240)
    def test_percentage_change(self):
        self.assertEqual(AnalyticsService().calculate_percentage_change(400, 360), -10)
        self.assertIsNone(AnalyticsService().calculate_percentage_change(0, 30))
    def test_convert_to_tonnes(self):
        self.assertEqual(CarbonCalculator().convert_to_tonnes(400), 0.4)
    def test_sahra_csv_to_analytics(self):
        csv_file = Path(__file__).resolve().parents[1] / "Data_Management" / "electricity.csv"
        records = validate_csv(csv_file)["valid_records"]
        results = [CarbonCalculator().calculate(record, example_factor()) for record in records]
        self.assertEqual(AnalyticsService(results).calculate_total(), 108)
if __name__ == "__main__":
    unittest.main()
