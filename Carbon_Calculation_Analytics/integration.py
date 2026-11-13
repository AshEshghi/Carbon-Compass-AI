"""Bridge the final 2016 database records to the existing Streamlit calculator."""
from datetime import date, datetime
from Carbon_Calculation_Analytics.analytics_service import AnalyticsService
from Carbon_Calculation_Analytics.carbon_calculator import CarbonCalculator
from Carbon_Calculation_Analytics.emission_factor import EmissionFactor


def calculate_2016_records(records, building_id=1, factor_value=0.4):
    """Return (HA1 summary, monthly emission totals) for one 2016 building.

    Accepts the dictionaries returned by Sahra's GET /records.
    Invalid/mixed-year records are rejected rather than silently counted.
    """
    factor = EmissionFactor(1, "DEMO", 2016, factor_value,
                            "Hypothetical example factor; not for official reporting")
    calculator = CarbonCalculator()
    results = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Records must be dictionaries")
        if record.get("building_id") != building_id:
            raise ValueError("Unexpected building_id in analytics records")
        raw_date = record.get("timestamp")
        try:
            record_date = raw_date.date() if isinstance(raw_date, datetime) else raw_date
            if not isinstance(record_date, date):
                record_date = date.fromisoformat(str(raw_date)[:10])
        except (ValueError, TypeError) as exc:
            raise ValueError("Invalid record timestamp") from exc
        if not date(2016, 1, 1) <= record_date < date(2016, 10, 1):
            raise ValueError("Final analytics expects January–September 2016 records only")
        results.append(calculator.calculate(record, factor))
    service = AnalyticsService(results)
    return service.summary(), service.aggregate_monthly()
