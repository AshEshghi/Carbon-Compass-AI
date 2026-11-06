from abc import ABC, abstractmethod
class CarbonProcessor(ABC):

    @abstractmethod
    def process(self, record):
        pass
