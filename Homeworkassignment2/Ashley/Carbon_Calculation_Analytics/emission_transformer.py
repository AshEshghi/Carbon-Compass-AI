from collections.abc import Mapping
from datetime import datetime, date
from math import isfinite
try:
    from .processor_base import CarbonProcessor
    from .scope_filter import parse_scope
except ImportError:
    from processor_base import CarbonProcessor
    from scope_filter import parse_scope
class EmissionTransformer(CarbonProcessor):

    def __init__(self, factors: Mapping):
        self.initialize(factors)

    def initialize(self, factors: Mapping):
        self.set_factors(factors)

    def set_factors(self, factors: Mapping):
        if not isinstance(factors, Mapping) or not factors:
            raise ValueError("factors must be a non-empty mapping")
        verified = {}
        for activity, raw_factor in factors.items():
            if not isinstance(activity, str) or not activity.strip():
                raise ValueError("Activity type must be a nonempty string")
            if not isinstance(raw_factor, Mapping):
                raise TypeError("Factor configuration must be a dictionary")
            required = {"value", "unit", "source", "year", "scope"}
            missing = required - raw_factor.keys()
            if missing:
                raise ValueError(f"Factor {activity!r} missing: {sorted(missing)}")
            value = raw_factor["value"]
            if isinstance(value, bool):
                raise ValueError("Factor must be a non-negative finite number")
            try:
                value = float(value)
            except (TypeError, ValueError, OverflowError) as error:
                raise ValueError("Factor must be numeric") from error
            if not isfinite(value) or value < 0:
                raise ValueError("Factor must be a non-negative finite number")
            unit = raw_factor["unit"]
            source = raw_factor["source"]
            year = raw_factor["year"]
            if not isinstance(unit, str) or not unit.strip():
                raise ValueError("Unit must be specified")
            if not isinstance(source, str) or not source.strip():
                raise ValueError("Factor source must be specified")
            if isinstance(year, bool) or not isinstance(year, int) or not 1900 <= year <= 2100:
                raise ValueError("Factor year must be a valid integer")
            verified[activity.strip().lower()] = {
                "value": value,
                "unit": unit.strip(),
                "source": source.strip(),
                "year": year,
                "scope": parse_scope(raw_factor["scope"]),
            }
        self._factors = verified

    def get_factors(self):
        return {name: dict(config) for name, config in self._factors.items()}

    @staticmethod
    def _read_quantity(record: Mapping, activity: str):
        if activity == "electricity" and "electricity_kwh" in record:
            return record["electricity_kwh"], "kWh"
        if "quantity" not in record or "unit" not in record:
            raise ValueError("This activity needs quantity and unit fields")
        return record["quantity"], record["unit"]

    def process(self, record: Mapping) -> dict:
        if not isinstance(record, Mapping):
            raise TypeError("Each event must be a dictionary-like record")

        # Sahra's electricity records have electricity_kwh but no activity_type.
        activity = record.get("activity_type")
        if activity is None and "electricity_kwh" in record:
            activity = "electricity"
        if not isinstance(activity, str) or not activity.strip():
            raise ValueError("Missing activity_type")
        activity = activity.strip().lower()
        if activity not in self._factors:
            raise ValueError(f"No emission factor for activity: {activity}")
        factor = self._factors[activity]

        scope = record.get("scope", record.get("scope_tag"))
        if scope is None:
            raise ValueError("Missing scope tag")
        if parse_scope(scope) != factor["scope"]:
            raise ValueError("Activity scope does not match selected factor")

        raw_quantity, unit = self._read_quantity(record, activity)
        if isinstance(raw_quantity, bool):
            raise ValueError("Quantity must be a non-negative finite number")
        try:
            quantity = float(raw_quantity)
        except (TypeError, ValueError, OverflowError) as error:
            raise ValueError("Quantity must be numeric") from error
        if not isfinite(quantity) or quantity < 0:
            raise ValueError("Quantity must be a non-negative finite number")
        if unit != factor["unit"]:
            raise ValueError(f"Unit mismatch: expected {factor['unit']}, got {unit}")

        if "timestamp" in record and record["timestamp"] is not None:
            stamp = record["timestamp"]
            if isinstance(stamp, str):
                try:
                    stamp_year = datetime.fromisoformat(stamp.strip()).year
                except ValueError as error:
                    raise ValueError("timestamp must be ISO-formatted") from error
            elif isinstance(stamp, (date, datetime)):
                stamp_year = stamp.year
            else:
                raise ValueError("timestamp must be a date or ISO date string")
            if stamp_year != factor["year"]:
                raise ValueError("Timestamp year does not match factor year")

        emissions_kg = quantity * factor["value"]
        if not isfinite(emissions_kg):
            raise ValueError("Computed emissions are not finite")
        result = dict(record)
        result.update({
            "scope": factor["scope"],
            "activity_type": activity,
            "quantity": quantity,
            "unit": factor["unit"],
            "emission_factor_value": factor["value"],
            "emission_factor_unit": f"kgCO2e/{factor['unit']}",
            "emission_factor_source": factor["source"],
            "emission_factor_year": factor["year"],
            "emissions_kg_co2e": emissions_kg,
            "emissions_tonnes_co2e": emissions_kg / 1000.0,
        })
        return result
