"""Calculated emissions associated with an electricity-consumption record."""

from Carbon_Calculation_Analytics.validation import valid_id, valid_quantity, valid_timestamp


class EmissionResult:
    """A calculation result, retaining the source record ID when available."""

    def __init__(self, record_id, building_id, timestamp,
                 electricity_kwh, factor_id, kgco2e, result_id=None):
        self.initialize(record_id, building_id, timestamp,
                        electricity_kwh, factor_id, kgco2e, result_id)

    def initialize(self, record_id, building_id, timestamp,
                   electricity_kwh, factor_id, kgco2e, result_id=None):
        self.set_record_id(record_id)
        self.set_building_id(building_id)
        self.set_timestamp(timestamp)
        self.set_electricity_kwh(electricity_kwh)
        self.set_factor_id(factor_id)
        self.set_kgco2e(kgco2e)
        self.set_result_id(result_id)

    def get_record_id(self):
        return self._record_id

    def set_record_id(self, value):
        self._record_id = valid_id(value, "record_id", allow_none=True)

    def get_result_id(self):
        return self._result_id

    def set_result_id(self, value):
        self._result_id = valid_id(value, "result_id", allow_none=True)

    def get_building_id(self):
        return self._building_id

    def set_building_id(self, value):
        self._building_id = valid_id(value, "building_id")

    def get_factor_id(self):
        return self._factor_id

    def set_factor_id(self, value):
        self._factor_id = valid_id(value, "factor_id")

    def get_timestamp(self):
        return self._timestamp

    def set_timestamp(self, value):
        self._timestamp = valid_timestamp(value)

    def get_electricity_kwh(self):
        return self._electricity_kwh

    def set_electricity_kwh(self, value):
        self._electricity_kwh = valid_quantity(value, "electricity_kwh")

    def get_kgco2e(self):
        return self._kgco2e

    def set_kgco2e(self, value):
        self._kgco2e = valid_quantity(value, "kgco2e")

    def to_dict(self):
        return {
            "result_id": self._result_id,
            "record_id": self._record_id,
            "building_id": self._building_id,
            "timestamp": self._timestamp.isoformat(),
            "electricity_kwh": self._electricity_kwh,
            "factor_id": self._factor_id,
            "kgco2e": self._kgco2e,
        }
