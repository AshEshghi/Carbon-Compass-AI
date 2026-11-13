
from abc import ABC, abstractmethod
from collections.abc import Mapping

from ai_service import AIService


#class AssistantProcessor(ABC):
 #   """
  #  Abstract base class for AI assistant processors.
   # """

    #@abstractmethod
    #def process(self, record):
     #   pass

#############NEW Class AssistantProcessor########
class AssistantProcessor(ABC):

    @abstractmethod
    def process(self, record):
        pass

    def __add__(self, other):
        from pipeline import Pipeline

        if isinstance(other, Pipeline):
            return Pipeline([self] + other.processors)

        return Pipeline([self, other])

#################################################
class InsightProcessor(AssistantProcessor):
    """
    Receives calculated carbon data and generates
    an AI explanation using AIService.
    """

    def __init__(self, ai_service=None):
        self.ai_service = ai_service or AIService()

    def process(self, record):
        if not isinstance(record, Mapping):
            raise TypeError("Record must be a dictionary.")

        if "emissions_kg_co2e" not in record:
            raise ValueError("Missing emissions_kg_co2e.")

        consumption = record.get(
            "electricity_kwh",
            record.get("quantity")
        )

        if consumption is None:
            raise ValueError("Missing energy consumption data.")

        emissions = record["emissions_kg_co2e"]

        prompt = self.ai_service.build_prompt(
            consumption=consumption,
            emissions=emissions
        )

        response = self.ai_service.generate_response(prompt)

        result = dict(record)
        result["ai_insight"] = response

        return result
