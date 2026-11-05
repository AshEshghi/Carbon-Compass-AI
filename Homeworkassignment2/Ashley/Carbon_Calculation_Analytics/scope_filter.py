import re
from collections.abc import Iterable, Mapping
try:
    from .processor_base import CarbonProcessor
except ImportError:
    from processor_base import CarbonProcessor
def parse_scope(value):
    """Accept 1, 2, 3 or strings like 'Scope 2'."""
    if isinstance(value, bool):
        raise ValueError("A scope must be 1, 2 or 3")
    if isinstance(value, int) and value in (1, 2, 3):
        return value
    if isinstance(value, str):
        match = re.fullmatch(r"(?:scope\s*[-_:]?\s*)?([123])", value.strip(), re.I)
        if match:
            return int(match.group(1))
    raise ValueError("A scope must be 1, 2 or 3")
class ScopeFilter(CarbonProcessor):
    """Keep only events belonging to the configured GHG scopes."""

    def __init__(self, allowed_scopes=(2,)):
        self.initialize(allowed_scopes)

    def initialize(self, allowed_scopes=(2,)):
        self.set_allowed_scopes(allowed_scopes)

    def get_allowed_scopes(self):
        return frozenset(self._allowed_scopes)

    def set_allowed_scopes(self, scopes):
        if isinstance(scopes, (str, bytes)):
            scopes = (scopes,)
        try:
            selected = frozenset(parse_scope(scope) for scope in scopes)
        except TypeError as error:
            raise ValueError("allowed_scopes must be iterable") from error
        if not selected:
            raise ValueError("At least one scope must be selected")
        self._allowed_scopes = selected

    def process(self, record: Mapping) -> dict | None:
        if not isinstance(record, Mapping):
            raise TypeError("Each event must be a dictionary-like record")
        tag = record.get("scope", record.get("scope_tag"))
        if tag is None:
            raise ValueError("Missing scope tag; add scope=2 for purchased electricity")
        normalized_scope = parse_scope(tag)
        if normalized_scope not in self._allowed_scopes:
            return None
        result = dict(record)
        result["scope"] = normalized_scope
        return result

    def filter_stream(self, records: Iterable):
        """Generate accepted records one at a time (does not modify source data)."""
        for record in records:
            filtered = self.process(record)
            if filtered is not None:
                yield filtered