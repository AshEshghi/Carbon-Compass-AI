from abc import ABC, abstractmethod
from collections.abc import Mapping
from Data_Management.consumption_record import ConsumptionRecord
from Carbon_Calculation_Analytics.emission_factor import EmissionFactor
from Carbon_Calculation_Analytics.emission_result import EmissionResult
from Carbon_Calculation_Analytics.validation import valid_id, valid_quantity, valid_timestamp
class BaseCalculator(ABC):
    """Common interface for calculators."""
    def __init__(self, precision=6):
        self.initialize(precision)
    def initialize(self, precision=6):
        self.set_precision(precision)
    def get_precision(self):
        return self._precision
    def set_precision(self, value):
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 12:
            raise ValueError("precision must be an integer from 0 to 12")
        self._precision = value

    @abstractmethod
    def calculate(self, record, factor):
        pass
    
class CarbonCalculator(BaseCalculator):
    """Convert electricity consumption into estimated emissions."""
    def __init__(self, precision=6):
        super().__init__(precision)
    def initialize(self, precision=6):
        super().initialize(precision)
        self._calculation_count = 0
    def get_calculation_count(self):
        return self._calculation_count
    def set_calculation_count(self, value):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("count must be a non-negative integer")
        self._calculation_count = value
    def _record_values(self, record):
        if isinstance(record, ConsumptionRecord):
            data = {
                "record_id": record.get_record_id(),
                "building_id": record.get_building_id(),
                "timestamp": record.get_timestamp(),
                "electricity_kwh": record.get_electricity_kwh(),
            }
        elif isinstance(record, Mapping):
            data = record
        else:
            raise TypeError("Expected a ConsumptionRecord or dictionary")

        fields = ("record_id", "building_id", "timestamp", "electricity_kwh")
        for field in fields:
            if field not in data:
                raise ValueError(f"Missing field: {field}")
        return {
            "record_id": valid_id(data["record_id"], "record_id", allow_none=True),
            "building_id": valid_id(data["building_id"], "building_id"),
            "timestamp": valid_timestamp(data["timestamp"]),
            "electricity_kwh": valid_quantity(data["electricity_kwh"], "electricity_kwh"),
        }
    def calculate(self, record, factor):
        if not isinstance(factor, EmissionFactor):
            raise TypeError("factor must be an EmissionFactor")
        data = self._record_values(record)
        if data["timestamp"].year != factor.get_year():
            raise ValueError("record year does not match factor year")
        if not factor.validate_factor():
            raise ValueError("invalid emission factor")
        emissions = data["electricity_kwh"] * factor.get_kgco2e_per_kwh()
        result = EmissionResult(
            data["record_id"], data["building_id"], data["timestamp"],
            data["electricity_kwh"], factor.get_factor_id(), emissions,
        )
        self._calculation_count += 1
        return result
    def calculate_total(self, results):
        results = list(results)
        if not all(isinstance(item, EmissionResult) for item in results):
            raise TypeError("Expected EmissionResult objects")
        return sum(item.get_kgco2e() for item in results)
    def convert_to_tonnes(self, kgco2e):
        return valid_quantity(kgco2e, "kgco2e") / 1000
    def rounded_for_display(self, kgco2e):
        return round(valid_quantity(kgco2e, "kgco2e"), self._precision)
