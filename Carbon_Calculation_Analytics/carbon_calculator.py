"""Object-oriented carbon calculator using Data Management's shared records."""

from abc import ABC, abstractmethod
from math import fsum
from collections.abc import Mapping

from Data_Management.consumption_record import ConsumptionRecord
from Carbon_Calculation_Analytics.emission_factor import EmissionFactor
from Carbon_Calculation_Analytics.emission_result import EmissionResult
from Carbon_Calculation_Analytics.validation import valid_id, valid_quantity, valid_timestamp


class BaseCalculator(ABC):
    """General interface for an activity-based emissions calculator."""

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
        """Return the emissions from one validated activity record."""


class CarbonCalculator(BaseCalculator):
    """Calculate electricity emissions from dictionaries or shared record objects."""

    def __init__(self, precision=6):
        super().__init__(precision)
        self._calculation_count = 0

    def initialize(self, precision=6):
        super().initialize(precision)
        self._calculation_count = 0

    def get_calculation_count(self):
        return self._calculation_count

    def set_calculation_count(self, count):
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ValueError("calculation count must be a non-negative integer")
        self._calculation_count = count

    @staticmethod
    def _record_values(record):
        """Read the shared model or four-field Data Management dictionary.

        The source record is never modified. Data validation here is independent
        of Data Management and protects numerical calculations from bad input.
        """
        if isinstance(record, ConsumptionRecord):
            values = {
                "record_id": record.get_record_id(),
                "building_id": record.get_building_id(),
                "timestamp": record.get_timestamp(),
                "electricity_kwh": record.get_electricity_kwh(),
            }
        elif isinstance(record, Mapping):
            required = {"record_id", "building_id", "timestamp", "electricity_kwh"}
            missing = required.difference(record.keys())
            if missing:
                raise ValueError(f"record is missing required fields: {', '.join(sorted(missing))}")
            values = {name: record[name] for name in required}
        else:
            raise TypeError("record must be a shared ConsumptionRecord or a four-field dictionary")

        return {
            "record_id": valid_id(values["record_id"], "record_id", allow_none=True),
            "building_id": valid_id(values["building_id"], "building_id"),
            "timestamp": valid_timestamp(values["timestamp"]),
            "electricity_kwh": valid_quantity(values["electricity_kwh"], "electricity_kwh"),
        }

    def calculate(self, record, factor):
        if not isinstance(factor, EmissionFactor):
            raise TypeError("factor must be an EmissionFactor")
        values = self._record_values(record)
        if values["timestamp"].year != factor.get_year():
            raise ValueError("record year does not match emission factor year")
        if not factor.validate_factor():
            raise ValueError("invalid emission factor")

        emissions = values["electricity_kwh"] * factor.get_kgco2e_per_kwh()
        result = EmissionResult(
            record_id=values["record_id"],
            building_id=values["building_id"],
            timestamp=values["timestamp"],
            electricity_kwh=values["electricity_kwh"],
            factor_id=factor.get_factor_id(),
            kgco2e=emissions,
        )
        self._calculation_count += 1
        return result

    def calculate_total(self, results):
        records = list(results)
        if not all(isinstance(item, EmissionResult) for item in records):
            raise TypeError("results must contain EmissionResult objects")
        return fsum(item.get_kgco2e() for item in records)

    def convert_to_tonnes(self, kgco2e):
        return valid_quantity(kgco2e, "kgco2e") / 1000

    def rounded_for_display(self, kgco2e):
        return round(valid_quantity(kgco2e, "kgco2e"), self._precision)
