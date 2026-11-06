from datetime import date
from math import isfinite
try:
    from .processor_base import CarbonProcessor
    from .scope_filter import parse_scope
except ImportError:
    from processor_base import CarbonProcessor
    from scope_filter import parse_scope


class EmissionTransformer(CarbonProcessor):
    def __init__(self, factors):
        if not factors:
            raise ValueError("Provide at least one emission factor")
        self.factors = factors

    def process(self, record):
        if not isinstance(record, dict):
            raise TypeError("Record must be a dictionary")

        activity = record.get("activity_type")
        if activity is None and "electricity_kwh" in record:
            activity = "electricity"
        if activity not in self.factors:
            raise ValueError("No emission factor for this activity")

        factor = self.factors[activity]
        activity_scope = parse_scope(record.get("scope", record.get("scope_tag")))
        factor_scope = parse_scope(factor["scope"])
        if activity_scope != factor_scope:
            raise ValueError("Activity and factor scopes do not match")

        if activity == "electricity" and "electricity_kwh" in record:
            quantity = record["electricity_kwh"]
            unit = "kWh"
        else:
            quantity = record.get("quantity")
            unit = record.get("unit")

        if unit != factor["unit"]:
            raise ValueError("Activity and factor units do not match")

        if isinstance(quantity, bool) or isinstance(factor["value"], bool):
            raise ValueError("Invalid quantity or factor")
        try:
            quantity = float(quantity)
            factor_value = float(factor["value"])
        except (TypeError, ValueError) as exc:
            raise ValueError("Quantity and factor must be numbers") from exc
        if not (isfinite(quantity) and isfinite(factor_value)) or min(quantity, factor_value) < 0:
            raise ValueError("Quantity and factor must be non-negative and finite")

        if record.get("timestamp") and factor.get("year") is not None:
            try:
                year = date.fromisoformat(str(record["timestamp"])[:10]).year
            except ValueError as exc:
                raise ValueError("Invalid timestamp") from exc
            if year != factor["year"]:
                raise ValueError("Factor year does not match activity year")

        kg = quantity * factor_value
        result = record.copy()
        result.update({
            "scope": factor_scope,
            "activity_type": activity,
            "emissions_kg_co2e": kg,
            "emissions_tonnes_co2e": kg / 1000,
            "emission_factor_source": factor.get("source", "Unspecified"),
            "emission_factor_year": factor.get("year"),
        })
        return result
