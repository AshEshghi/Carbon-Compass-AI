import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv


# Load environment variables from the project's .env file
load_dotenv(find_dotenv(), override=True)


class AIService:

    def __init__(self, model=None):
        self.model = model or os.getenv("KICONNECT_MODEL")

        self.client = OpenAI(
            api_key=os.getenv("KICONNECT_API_KEY"),
            base_url=os.getenv("KICONNECT_BASE_URL")
        )

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model

    def build_prompt(self, consumption, emissions):
        return f"""
You are an AI assistant for an Enterprise Carbon Footprint Tracker.

Your task is to analyze electricity consumption and carbon emissions
based ONLY on the verified data provided below.

Verified data:
- Electricity consumption: {consumption} kWh
- Carbon emissions: {emissions} kg CO2e

STRICT RULES:
1. Use only the numerical values provided above.
2. Do not invent, estimate, or assume any additional numerical data.
3. Do not create unsupported percentages, comparisons, or predictions.
4. If information is missing, clearly state that it is unavailable.
5. Explain the relationship between electricity consumption
   and carbon emissions in simple language.
6. Provide practical recommendations for reducing electricity
   consumption and carbon emissions.
7. Do not claim that a recommendation will produce a specific
   numerical reduction unless verified data supports it.
8. Clearly distinguish verified facts from general recommendations.

Write a clear and concise response.
"""

    def generate_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content

        except Exception as error:
            return f"AI service error: {error}"