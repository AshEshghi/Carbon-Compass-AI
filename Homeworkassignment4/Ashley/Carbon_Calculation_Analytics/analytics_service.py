from datetime import date
from math import isfinite
try:
    from .analytics_error import AnalyticsError
except ImportError:
    from analytics_error import AnalyticsError
class AnalyticsService:
    def __init__(self, emission_factor=0.4):
        try:
            if isinstance(emission_factor, bool):
                raise ValueError
            self.emission_factor = float(emission_factor)
        except (TypeError, ValueError):
            raise AnalyticsError("Invalid emission factor")
        if not isfinite(self.emission_factor) or self.emission_factor < 0:
            raise AnalyticsError("Invalid emission factor")
    def summarize(self, records, building_id=1):
        monthly = {}
        for record in records:
            try:
                kwh = record["electricity_kwh"]
                if isinstance(kwh, bool):
                    raise ValueError
                kwh = float(kwh)
                month = date.fromisoformat(str(record["timestamp"])[:10]).strftime("%Y-%m")
            except (KeyError, TypeError, ValueError, OverflowError):
                raise AnalyticsError("Invalid consumption record")

            if not isfinite(kwh) or kwh < 0:
                raise AnalyticsError("Electricity consumption must be non-negative")
            monthly[month] = monthly.get(month, 0) + kwh

        total_kwh = sum(monthly.values())
        total_kg = total_kwh * self.emission_factor
        return {
            "building_id": building_id,
            "record_count": len(records),
            "total_electricity_kwh": round(total_kwh, 4),
            "emissions_kg_co2e": round(total_kg, 4),
            "emissions_tonnes_co2e": round(total_kg / 1000, 6),
            "factor_kg_co2e_per_kwh": self.emission_factor,
            "factor_note": "Hypothetical example factor, not for official reporting",
            "monthly": [
                {
                    "month": month,
                    "electricity_kwh": round(monthly[month], 4),
                    "emissions_kg_co2e": round(monthly[month] * self.emission_factor, 4),
                }
                for month in sorted(monthly)
            ],
        }
