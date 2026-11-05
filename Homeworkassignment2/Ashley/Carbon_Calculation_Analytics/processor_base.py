from abc import ABC, abstractmethod
from collections.abc import Mapping
class CarbonProcessor(ABC):
    """A single record enters and produces a dictionary or is filtered out"""
    @abstractmethod
    def process(self, record: Mapping) -> dict | None:
        """Process one event without changing the input object"""