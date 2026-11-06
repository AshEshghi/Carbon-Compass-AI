
from insight_processor import AssistantProcessor


class CarbonRecordFilter(AssistantProcessor):
    """
    Filters invalid carbon activity records.
    """

    def process(self, record):

        if not isinstance(record, dict):
            return None

        if record.get("scope") not in [1, 2, 3]:
            return None

        if "electricity_kwh" not in record:
            return None

        if record["electricity_kwh"] < 0:
            return None

        if "emissions_kg_co2e" not in record:
            return None

        if record["emissions_kg_co2e"] < 0:
            return None

        return record
