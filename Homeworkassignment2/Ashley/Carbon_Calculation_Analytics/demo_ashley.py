try:
    from .scope_filter import ScopeFilter
    from .emission_transformer import EmissionTransformer
except ImportError:
    from scope_filter import ScopeFilter
    from emission_transformer import EmissionTransformer


FACTOR_CONFIG = {
    "electricity": {
        "value": 0.4,
        "unit": "kWh",
        "scope": 2,
        "year": 2026,
        "source": "Hypothetical factor for demonstration only",
    }
}

FACTORS = FACTOR_CONFIG


def electricity_events(records):
    for record in records:
        event = record.copy()
        event["scope"] = 2
        yield event


def main():
    records = [
        {"record_id": 1, "building_id": 1, "timestamp": "2026-01-01", "electricity_kwh": 120},
        {"record_id": 2, "building_id": 1, "timestamp": "2026-01-02", "electricity_kwh": 150},
    ]

    scope_filter = ScopeFilter((2,))
    transformer = EmissionTransformer(FACTOR_CONFIG)

    for record in scope_filter.filter_stream(electricity_events(records)):
        result = transformer.process(record)
        print(f"Record {result['record_id']}: {result['emissions_tonnes_co2e']:.5f} t CO2e")


if __name__ == "__main__":
    main()
