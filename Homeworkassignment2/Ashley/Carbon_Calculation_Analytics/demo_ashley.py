try:
    from .scope_filter import ScopeFilter
    from .emission_transformer import EmissionTransformer
except ImportError:
    from scope_filter import ScopeFilter
    from emission_transformer import EmissionTransformer
FACTOR_CONFIG = {
    # Hypothetical figures
    "electricity": {
        "value": 0.4,       
        "unit": "kWh",
        "year": 2026,
        "scope": 2,
        "source": "Illustrative test factor (not an official inventory factor)",
    }
}
def electricity_events(records):
    for record in records:
        tagged = dict(record)
        tagged["scope"] = 2
        yield tagged


def main():
    raw_records = [
        {"record_id": 1, "building_id": 1, "timestamp": "2026-01-01", "electricity_kwh": 120.0},
        {"record_id": 2, "building_id": 1, "timestamp": "2026-01-02", "electricity_kwh": 150.0},
    ]
    scope_filter = ScopeFilter((2,))
    transformer = EmissionTransformer(FACTOR_CONFIG)
    for record in scope_filter.filter_stream(electricity_events(raw_records)):
        result = transformer.process(record)
        print(f"Record {result['record_id']}: {result['emissions_tonnes_co2e']:.5f} t CO2e")
if __name__ == "__main__":
    main()