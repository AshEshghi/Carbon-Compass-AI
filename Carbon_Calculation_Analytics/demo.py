"""Demonstration of carbon analytics using the shared Data Management model."""

from Data_Management.consumption_record import ConsumptionRecord
from Carbon_Calculation_Analytics.analytics_service import AnalyticsService
from Carbon_Calculation_Analytics.carbon_calculator import CarbonCalculator
from Carbon_Calculation_Analytics.emission_factor import EmissionFactor


def main():
    # Sample values are for demonstrating the software, not official accounting.
    sample_rows = [
        {"record_id": 1, "building_id": 1, "timestamp": "2026-01-15", "electricity_kwh": 1200.0},
        {"record_id": 2, "building_id": 1, "timestamp": "2026-02-15", "electricity_kwh": 1000.0},
        {"record_id": 3, "building_id": 1, "timestamp": "2026-03-15", "electricity_kwh": 900.0},
    ]
    # Sahra's model is also supported, not just the database dictionaries.
    shared_record = ConsumptionRecord(None, 1, "2026-03-16", 50.0)
    sample_rows.append(shared_record)

    factor = EmissionFactor(1, "DEMO", 2026, 0.4, "Hypothetical example factor")
    calculator = CarbonCalculator()
    results = [calculator.calculate(row, factor) for row in sample_rows]
    analytics = AnalyticsService(results)

    print("Factor source:", factor.get_source())
    print("Monthly emissions (kg CO2e):", analytics.aggregate_monthly())
    print("Total electricity (kWh):", analytics.total_electricity_kwh())
    print("Total emissions (kg CO2e):", analytics.calculate_total())
    print("Building totals:", analytics.aggregate_by_building())
    print("February to March:", analytics.compare_periods("2026-02", "2026-03"))
    print("Chart data:", analytics.prepare_chart_data())
    print("Calculated records:", calculator.get_calculation_count())


if __name__ == "__main__":
    main()
