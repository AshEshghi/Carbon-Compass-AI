from Carbon_Calculation_Analytics.validation import valid_id, valid_quantity
class EmissionFactor:
    """Factor expressed in kg CO2e per kWh for a given region and year."""
    def __init__(self, factor_id, region, year, kgco2e_per_kwh, source):
        self.initialize(factor_id, region, year, kgco2e_per_kwh, source)
    def initialize(self, factor_id, region, year, kgco2e_per_kwh, source):
        self.set_factor_id(factor_id)
        self.set_region(region)
        self.set_year(year)
        self.set_kgco2e_per_kwh(kgco2e_per_kwh)
        self.set_source(source)
    def get_factor_id(self):
        return self._factor_id
    def set_factor_id(self, value):
        self._factor_id = valid_id(value, "factor_id")
    def get_region(self):
        return self._region
    def set_region(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("region must be non-empty text")
        self._region = value.strip()
    def get_year(self):
        return self._year
    def set_year(self, value):
        if isinstance(value, bool) or not isinstance(value, int) or not 1900 <= value <= 2100:
            raise ValueError("year must be an integer between 1900 and 2100")
        self._year = value
    def get_kgco2e_per_kwh(self):
        return self._kgco2e_per_kwh
    def set_kgco2e_per_kwh(self, value):
        self._kgco2e_per_kwh = valid_quantity(value, "kgco2e_per_kwh")
    def get_source(self):
        return self._source
    def set_source(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("source must be non-empty text")
        self._source = value.strip()
    def validate_factor(self):
        return self._kgco2e_per_kwh >= 0 and bool(self._source)
    def to_dict(self):
        return {
            "factor_id": self._factor_id,
            "region": self._region,
            "year": self._year,
            "kgco2e_per_kwh": self._kgco2e_per_kwh,
            "source": self._source,
            "unit": "kgCO2e/kWh",
        }
