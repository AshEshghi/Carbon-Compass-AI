try:
    from .processor_base import CarbonProcessor
except ImportError:
    from processor_base import CarbonProcessor


def parse_scope(value):
    if isinstance(value, str):
        value = value.strip().lower().replace("scope", "").replace("-", "").strip()
    if isinstance(value, bool) or str(value) not in ("1", "2", "3"):
        raise ValueError("Scope must be 1, 2, or 3")
    return int(value)


class ScopeFilter(CarbonProcessor):
    def __init__(self, allowed_scopes=(2,)):
        self.allowed_scopes = {parse_scope(value) for value in allowed_scopes}
        if not self.allowed_scopes:
            raise ValueError("Select at least one scope")

    def process(self, record):
        if not isinstance(record, dict):
            raise TypeError("Record must be a dictionary")

        scope = parse_scope(record.get("scope", record.get("scope_tag")))
        if scope not in self.allowed_scopes:
            return None
        result = record.copy()
        result["scope"] = scope
        return result
    def filter_stream(self, records):
        for record in records:
            result = self.process(record)
            if result is not None:
                yield result
