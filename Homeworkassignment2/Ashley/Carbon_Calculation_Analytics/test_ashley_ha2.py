import unittest
try:
    from .scope_filter import ScopeFilter, parse_scope
    from .emission_transformer import EmissionTransformer
    from .demo_ashley import electricity_events, FACTOR_CONFIG
    from .processor_base import CarbonProcessor
except ImportError:
    from scope_filter import ScopeFilter, parse_scope
    from emission_transformer import EmissionTransformer
    from demo_ashley import electricity_events, FACTOR_CONFIG
    from processor_base import CarbonProcessor
class TestScopeFilter(unittest.TestCase):
    def test_inherits_abstract_interface(self):
        self.assertTrue(issubclass(ScopeFilter, CarbonProcessor))
        self.assertTrue(issubclass(EmissionTransformer, CarbonProcessor))

    def test_scope_parsing(self):
        self.assertEqual(parse_scope("Scope 2"), 2)
        self.assertEqual(parse_scope("scope-3"), 3)
        self.assertEqual(parse_scope(1), 1)

    def test_rejects_bad_scope(self):
        for bad in (0, 4, "scope 9", True, None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_scope(bad)

    def test_filters_out_scope_one(self):
        original = {"scope": 1, "activity_type": "natural_gas"}
        self.assertIsNone(ScopeFilter((2,)).process(original))

    def test_keeps_scope_two_without_mutation(self):
        original = {"scope": "Scope 2", "electricity_kwh": 120}
        selected = ScopeFilter((2,)).process(original)
        self.assertEqual(selected["scope"], 2)
        self.assertEqual(original["scope"], "Scope 2")

    def test_selects_multiple_scopes(self):
        filter_ = ScopeFilter((1, 3))
        self.assertIsNotNone(filter_.process({"scope": 3}))
        self.assertIsNone(filter_.process({"scope": 2}))

    def test_missing_scope_rejected(self):
        with self.assertRaises(ValueError):
            ScopeFilter().process({"electricity_kwh": 50})

    def test_generator_is_lazy(self):
        seen = []
        def source():
            for scope in (1, 2, 3):
                seen.append(scope)
                yield {"scope": scope}
        iterator = ScopeFilter((2,)).filter_stream(source())
        self.assertEqual(seen, [])
        self.assertEqual(next(iterator), {"scope": 2})
        self.assertEqual(seen, [1, 2])

    def test_invalid_config(self):
        with self.assertRaises(ValueError):
            ScopeFilter([])


class TestEmissionTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = EmissionTransformer(FACTOR_CONFIG)
        self.event = {"record_id": 1, "building_id": 1, "timestamp": "2026-01-01", "electricity_kwh": 1000, "scope": 2}

    def test_electricity_in_tonnes(self):
        result = self.transformer.process(self.event)
        self.assertAlmostEqual(result["emissions_kg_co2e"], 400)
        self.assertAlmostEqual(result["emissions_tonnes_co2e"], .4)

    def test_preserves_original_fields(self):
        result = self.transformer.process(self.event)
        self.assertEqual(result["record_id"], 1)
        self.assertEqual(result["building_id"], 1)
        self.assertNotIn("emissions_kg_co2e", self.event)

    def test_zero_quantity(self):
        self.event["electricity_kwh"] = 0
        self.assertEqual(self.transformer.process(self.event)["emissions_tonnes_co2e"], 0)

    def test_negative_and_nan(self):
        for amount in (-1, float("nan"), float("inf"), True):
            self.event["electricity_kwh"] = amount
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                self.transformer.process(self.event)

    def test_wrong_scope(self):
        self.event["scope"] = 1
        with self.assertRaises(ValueError):
            self.transformer.process(self.event)

    def test_missing_factor(self):
        self.event["activity_type"] = "flight"
        with self.assertRaises(ValueError):
            self.transformer.process(self.event)

    def test_timestamp_year_mismatch(self):
        self.event["timestamp"] = "2025-01-01"
        with self.assertRaises(ValueError):
            self.transformer.process(self.event)

    def test_no_mutation_of_config(self):
        snapshot = self.transformer.get_factors()
        snapshot["electricity"]["value"] = 99
        self.assertEqual(self.transformer.get_factors()["electricity"]["value"], .4)

    def test_invalid_factor_configuration(self):
        invalid = {"electricity": {**FACTOR_CONFIG["electricity"], "value": float("inf")}}
        with self.assertRaises(ValueError):
            EmissionTransformer(invalid)

    def test_other_scopes_with_explicit_factor(self):
        configs = {
            "natural_gas": {"value": 0.2, "unit": "kWh", "year": 2026, "scope": 1, "source": "Hypothetical test"},
            "flight": {"value": 0.15, "unit": "passenger_km", "year": 2026, "scope": 3, "source": "Hypothetical test"},
        }
        transformer = EmissionTransformer(configs)
        natural_gas = transformer.process({"scope": 1, "activity_type": "natural_gas", "quantity": 100, "unit": "kWh", "timestamp": "2026-02-01"})
        flight = transformer.process({"scope": 3, "activity_type": "flight", "quantity": 100, "unit": "passenger_km", "timestamp": "2026-02-01"})
        self.assertAlmostEqual(natural_gas["emissions_tonnes_co2e"], 0.02)
        self.assertAlmostEqual(flight["emissions_tonnes_co2e"], 0.015)

    def test_shared_protocol(self):
        steps = [ScopeFilter((2,)), self.transformer]
        event = dict(self.event)
        for processor in steps:
            event = processor.process(event)
        self.assertAlmostEqual(event["emissions_tonnes_co2e"], .4)


class TestStandaloneCompatibility(unittest.TestCase):
    def test_stream_of_dictionaries(self):
        # Works with Sahra's record format without importing her code.
        records = iter([
            {"record_id": 1, "building_id": 1, "timestamp": "2026-01-01", "electricity_kwh": 120},
            {"record_id": 2, "building_id": 1, "timestamp": "2026-01-02", "electricity_kwh": 150},
        ])
        filtered = ScopeFilter().filter_stream(electricity_events(records))
        transformer = EmissionTransformer(FACTOR_CONFIG)
        results = [transformer.process(record) for record in filtered]
        self.assertEqual(len(results), 2)
        self.assertAlmostEqual(sum(item["emissions_tonnes_co2e"] for item in results), 0.108)


if __name__ == "__main__":
    unittest.main()
