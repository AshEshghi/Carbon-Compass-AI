"""Unit tests and integration tests for the shared carbon analytics subsystem."""

import csv
import tempfile
import unittest
from abc import ABC
from io import StringIO
from pathlib import Path

from Data_Management.consumption_record import ConsumptionRecord
from Data_Management.database_manager import DatabaseManager
from Data_Management.csv_validation import validate_csv
from Carbon_Calculation_Analytics.emission_factor import EmissionFactor
from Carbon_Calculation_Analytics.emission_result import EmissionResult
from Carbon_Calculation_Analytics.carbon_calculator import CarbonCalculator, BaseCalculator
from Carbon_Calculation_Analytics.analytics_service import AnalyticsService


def factor(year=2026, value=0.4):
    return EmissionFactor(1, "DEMO", year, value, "Hypothetical test factor")


def make_record(day="2026-01-01", kwh=100, record_id=1):
    return ConsumptionRecord(record_id, 1, day, kwh)


def make_dict(day="2026-01-01", kwh=100, record_id=1):
    return {"record_id": record_id, "building_id": 1, "timestamp": day, "electricity_kwh": kwh}


def sample_results():
    rows = [make_dict("2026-01-15", 1200, 1), make_dict("2026-02-15", 1000, 2),
            make_dict("2026-03-15", 900, 3)]
    return [CarbonCalculator().calculate(row, factor()) for row in rows]


class SharedDataModelTests(unittest.TestCase):
    def test_01_shared_class_is_the_real_one(self):
        self.assertEqual(ConsumptionRecord.__module__, "Data_Management.consumption_record")

    def test_02_shared_class_has_four_fields(self):
        rec = make_record()
        self.assertEqual((rec.get_record_id(), rec.get_building_id(), rec.get_timestamp(), rec.get_electricity_kwh()),
                         (1, 1, "2026-01-01", 100))

    def test_03_new_record_can_have_no_id(self):
        self.assertIsNone(make_record(record_id=None).get_record_id())

    def test_04_sahra_getters_and_setters(self):
        rec = make_record(record_id=None)
        rec.set_record_id(9)
        rec.set_electricity_kwh(150)
        self.assertEqual((rec.get_record_id(), rec.get_electricity_kwh()), (9, 150))


class CalculationTests(unittest.TestCase):
    def test_05_abstract_interface(self):
        self.assertTrue(issubclass(BaseCalculator, ABC))
        with self.assertRaises(TypeError):
            BaseCalculator()
        self.assertIsInstance(CarbonCalculator(), BaseCalculator)

    def test_06_calculate_from_shared_object(self):
        res = CarbonCalculator().calculate(make_record(kwh=120), factor())
        self.assertAlmostEqual(res.get_kgco2e(), 48)

    def test_07_calculate_from_database_dictionary(self):
        res = CarbonCalculator().calculate(make_dict(kwh=120), factor())
        self.assertAlmostEqual(res.get_kgco2e(), 48)

    def test_08_preserves_database_generated_id(self):
        res = CarbonCalculator().calculate(make_dict(record_id=22), factor())
        self.assertEqual(res.get_record_id(), 22)

    def test_09_unsaved_record_keeps_none(self):
        res = CarbonCalculator().calculate(make_dict(record_id=None), factor())
        self.assertIsNone(res.get_record_id())

    def test_10_calculation_does_not_modify_dict(self):
        original = make_dict(kwh=120)
        snapshot = original.copy()
        CarbonCalculator().calculate(original, factor())
        self.assertEqual(original, snapshot)

    def test_11_calculation_does_not_modify_shared_object(self):
        rec = make_record(kwh=120)
        CarbonCalculator().calculate(rec, factor())
        self.assertEqual(rec.get_electricity_kwh(), 120)
        self.assertEqual(rec.get_record_id(), 1)

    def test_12_rejects_negative_quantity(self):
        with self.assertRaises(ValueError):
            CarbonCalculator().calculate(make_dict(kwh=-10), factor())

    def test_13_rejects_non_finite_quantities(self):
        for val in [float("inf"), float("nan")]:
            with self.subTest(val=val), self.assertRaises(ValueError):
                CarbonCalculator().calculate(make_dict(kwh=val), factor())

    def test_14_rejects_missing_columns(self):
        data = make_dict()
        data.pop("building_id")
        with self.assertRaisesRegex(ValueError, "building_id"):
            CarbonCalculator().calculate(data, factor())

    def test_15_rejects_invalid_timestamp(self):
        with self.assertRaises(ValueError):
            CarbonCalculator().calculate(make_dict(day="not-a-date"), factor())

    def test_16_rejects_invalid_record_id(self):
        with self.assertRaises(ValueError):
            CarbonCalculator().calculate(make_dict(record_id=0), factor())

    def test_17_rejects_invalid_building(self):
        data = make_dict()
        data["building_id"] = -1
        with self.assertRaises(ValueError):
            CarbonCalculator().calculate(data, factor())

    def test_18_rejects_wrong_factor_year(self):
        with self.assertRaisesRegex(ValueError, "year"):
            CarbonCalculator().calculate(make_dict(), factor(2025))

    def test_19_factor_getters_setters(self):
        f = factor()
        f.set_kgco2e_per_kwh(0.3)
        self.assertEqual(f.get_kgco2e_per_kwh(), 0.3)
        self.assertTrue(f.validate_factor())

    def test_20_rejects_nonfinite_factor(self):
        with self.assertRaises(ValueError):
            factor(value=float("inf"))

    def test_21_rejects_wrong_factor_type(self):
        with self.assertRaises(TypeError):
            CarbonCalculator().calculate(make_dict(), {"factor": 0.4})

    def test_22_converts_to_tonnes(self):
        self.assertEqual(CarbonCalculator().convert_to_tonnes(400), 0.4)

    def test_23_total(self):
        calc = CarbonCalculator()
        res = [calc.calculate(make_dict(kwh=100, record_id=1), factor()),
               calc.calculate(make_dict(kwh=200, record_id=2), factor())]
        self.assertEqual(calc.calculate_total(res), 120)
        self.assertEqual(calc.get_calculation_count(), 2)

    def test_24_rounding(self):
        calc = CarbonCalculator(precision=2)
        self.assertEqual(calc.rounded_for_display(1.236), 1.24)


class AnalyticsTests(unittest.TestCase):
    def test_25_monthly_aggregation(self):
        self.assertEqual(AnalyticsService(sample_results()).aggregate_monthly(),
                         {"2026-01": 480, "2026-02": 400, "2026-03": 360})

    def test_26_total(self):
        self.assertAlmostEqual(AnalyticsService(sample_results()).calculate_total(), 1240)

    def test_27_building_aggregation(self):
        self.assertEqual(AnalyticsService(sample_results()).aggregate_by_building(), {1: 1240})

    def test_28_period_comparison(self):
        r = AnalyticsService(sample_results()).compare_periods("2026-02", "2026-03")
        self.assertEqual(r["difference_kgco2e"], -40)
        self.assertAlmostEqual(r["percentage_change"], -10)

    def test_29_zero_baseline(self):
        self.assertIsNone(AnalyticsService().calculate_percentage_change(0, 20))

    def test_30_missing_period(self):
        with self.assertRaises(ValueError):
            AnalyticsService(sample_results()).compare_periods("2025-05", "2026-03")

    def test_31_empty_results(self):
        a = AnalyticsService()
        self.assertEqual(a.aggregate_monthly(), {})
        self.assertEqual(a.calculate_total(), 0)
        self.assertEqual(a.summary()["record_count"], 0)

    def test_32_reject_wrong_result_type(self):
        with self.assertRaises(TypeError):
            AnalyticsService(["something else"])

    def test_33_export_csv(self):
        table = list(csv.DictReader(StringIO(AnalyticsService(sample_results()).export_results_csv())))
        self.assertEqual(len(table), 3)
        self.assertEqual(table[0]["record_id"], "1")

    def test_34_summary(self):
        result = AnalyticsService(sample_results()).summary()
        self.assertEqual(result["total_emissions_kgco2e"], 1240)
        self.assertEqual(result["total_electricity_kwh"], 3100)
        self.assertEqual(result["building_id"], 1)

    def test_35_result_initialization(self):
        r = sample_results()[0]
        self.assertIsInstance(r, EmissionResult)
        r.set_kgco2e(15)
        self.assertEqual(r.get_kgco2e(), 15)


class IntegrationWithSahraTests(unittest.TestCase):
    def test_36_data_validation_from_real_csv(self):
        sample = Path(__file__).resolve().parents[1] / "Data_Management" / "electricity.csv"
        out = validate_csv(sample)
        self.assertEqual(len(out["valid_records"]), 2)
        self.assertEqual(len(out["errors"]), 1)  # duplicate third row
        self.assertEqual(set(out["valid_records"][0]),
                         {"record_id", "building_id", "timestamp", "electricity_kwh"})
        calc = CarbonCalculator()
        results = [calc.calculate(row, factor()) for row in out["valid_records"]]
        self.assertAlmostEqual(AnalyticsService(results).calculate_total(), 108)

    def test_37_database_auto_id_and_dictionary_fetch(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = DatabaseManager(Path(tmp) / "test.db")
            db.create_table()
            record_id = db.save_record(1, "2026-01-01", 120.0)
            self.assertEqual(record_id, 1)
            records = db.fetch_records()
            self.assertIsInstance(records[0], dict)
            self.assertEqual(records[0]["record_id"], 1)
            self.assertEqual(CarbonCalculator().calculate(records[0], factor()).get_kgco2e(), 48)

    def test_38_full_real_csv_to_db_to_analytics(self):
        sample = Path(__file__).resolve().parents[1] / "Data_Management" / "electricity.csv"
        validated = validate_csv(sample)["valid_records"]
        with tempfile.TemporaryDirectory() as tmp:
            db = DatabaseManager(Path(tmp) / "test.db")
            db.create_table()
            for item in validated:
                generated_id = db.save_record(item["building_id"], item["timestamp"], item["electricity_kwh"])
                self.assertIsInstance(generated_id, int)
            records = db.fetch_records()
            results = [CarbonCalculator().calculate(row, factor()) for row in records]
            self.assertAlmostEqual(AnalyticsService(results).calculate_total(), 108)
            self.assertTrue(all(x.get_record_id() is not None for x in results))


if __name__ == "__main__":
    unittest.main()
