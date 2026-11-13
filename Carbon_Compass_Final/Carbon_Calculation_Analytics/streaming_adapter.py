"""Convert electricity records to HA2 processing events (optional stage)."""
from Carbon_Calculation_Analytics.streaming.scope_filter import ScopeFilter
from Carbon_Calculation_Analytics.streaming.emission_transformer import EmissionTransformer


def electricity_events(records):
    for row in records:
        event = dict(row)
        event["scope"] = 2  # purchased electricity is Scope 2
        yield event


def make_processors(factor_value=0.4):
    factor = {"electricity": {
        "value": factor_value, "unit": "kWh", "scope": 2, "year": 2016,
        "source": "Hypothetical example factor; not for official reporting",
    }}
    return ScopeFilter((2,)), EmissionTransformer(factor)
