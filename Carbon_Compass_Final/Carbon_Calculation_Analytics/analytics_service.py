import csv
from io import StringIO
from Carbon_Calculation_Analytics.emission_result import EmissionResult
from Carbon_Calculation_Analytics.validation import valid_quantity
class AnalyticsService:
    """Make monthly and total summaries from calculated results."""
    def __init__(self, results=None):
        self.initialize(results)
    def initialize(self, results=None):
        self.set_results([] if results is None else results)
    def get_results(self):
        return tuple(self._results)
    def set_results(self, results):
        if not isinstance(results, (list, tuple)):
            raise TypeError("results must be a list or tuple")
        if not all(isinstance(item, EmissionResult) for item in results):
            raise TypeError("Expected EmissionResult objects")
        self._results = list(results)
    def add_result(self, result):
        if not isinstance(result, EmissionResult):
            raise TypeError("Expected an EmissionResult")
        self._results.append(result)
    def calculate_total(self):
        return sum(item.get_kgco2e() for item in self._results)
    def total_electricity_kwh(self):
        return sum(item.get_electricity_kwh() for item in self._results)
    def aggregate_monthly(self):
        totals = {}
        for item in self._results:
            month = item.get_timestamp().strftime("%Y-%m")
            totals[month] = totals.get(month, 0) + item.get_kgco2e()
        return dict(sorted(totals.items()))
    def aggregate_by_building(self):
        totals = {}
        for item in self._results:
            building = item.get_building_id()
            totals[building] = totals.get(building, 0) + item.get_kgco2e()
        return dict(sorted(totals.items()))
    def calculate_percentage_change(self, old_value, new_value):
        old = valid_quantity(old_value, "old_value")
        new = valid_quantity(new_value, "new_value")
        if old == 0:
            return None
        return (new - old) / old * 100
    def compare_periods(self, previous, current):
        totals = self.aggregate_monthly()
        if previous not in totals or current not in totals:
            raise ValueError("both months must exist")
        old = totals[previous]
        new = totals[current]
        return {
            "previous_period": previous,
            "current_period": current,
            "previous_kgco2e": old,
            "current_kgco2e": new,
            "difference_kgco2e": new - old,
            "percentage_change": self.calculate_percentage_change(old, new),
        }
    def prepare_chart_data(self):
        return [
            {"month": month, "emissions_kgco2e": total}
            for month, total in self.aggregate_monthly().items()
        ]
    def summary(self):
        buildings = {item.get_building_id() for item in self._results}
        return {
            "building_id": next(iter(buildings)) if len(buildings) == 1 else None,
            "record_count": len(self._results),
            "total_electricity_kwh": self.total_electricity_kwh(),
            "total_emissions_kgco2e": self.calculate_total(),
            "monthly_emissions": self.aggregate_monthly(),
        }
    def export_results_csv(self):
        output = StringIO()
        fields = ["record_id", "building_id", "timestamp", "electricity_kwh", "factor_id", "kgco2e"]
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for result in self._results:
            data = result.to_dict()
            writer.writerow({name: data[name] for name in fields})
        return output.getvalue()
