from datetime import date
from math import fsum, isfinite
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
        except (TypeError, ValueError, OverflowError):
            raise AnalyticsError("Invalid emission factor")
        if not isfinite(self.emission_factor) or self.emission_factor < 0:
            raise AnalyticsError("Invalid emission factor")
    def summarize(self, records, building_id=1):
        monthly = {}
        record_count = 0
        for record in records:
            try:
                kwh = record["electricity_kwh"]
                if isinstance(kwh, bool):
                    raise ValueError
                kwh = float(kwh)
                record_date = date.fromisoformat(str(record["timestamp"])[:10])
                month = record_date.strftime("%Y-%m")
            except (KeyError, TypeError, ValueError, OverflowError):
                raise AnalyticsError("Invalid consumption record")

            if not isfinite(kwh) or kwh < 0:
                raise AnalyticsError("Electricity consumption must be non-negative")
            if not date(2016, 1, 1) <= record_date < date(2016, 10, 1):
                raise AnalyticsError("Analytics only accepts January–September 2016 records")
            if "building_id" in record and record["building_id"] != building_id:
                raise AnalyticsError("Unexpected building ID")
            monthly.setdefault(month, []).append(kwh)
            record_count += 1

        try:
            total_kwh = fsum(fsum(values) for values in monthly.values())
            total_kg = total_kwh * self.emission_factor
        except OverflowError as exc:
            raise AnalyticsError("Analytics result is too large") from exc
        if not isfinite(total_kg):
            raise AnalyticsError("Analytics result is too large")
        return {
            "building_id": building_id,
            "record_count": record_count,
            "total_electricity_kwh": round(total_kwh, 4),
            "emissions_kg_co2e": round(total_kg, 4),
            "emissions_tonnes_co2e": round(total_kg / 1000, 6),
            "factor_kg_co2e_per_kwh": self.emission_factor,
            "factor_note": "Hypothetical example factor, not for official reporting",
            "monthly": [
                {
                    "month": month,
                    "electricity_kwh": round(fsum(monthly[month]), 4),
                    "emissions_kg_co2e": round(fsum(monthly[month]) * self.emission_factor, 4),
                }
                for month in sorted(monthly)
            ],
        }
