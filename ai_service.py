
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class AIService:

    def __init__(self, model="llama3.2:1b"):
        self.model = model

    # Getter for model
    def get_model(self):
        return self.model

    # Setter for model
    def set_model(self, model):
        self.model = model

    # Build a prompt using project data
    def build_prompt(self, consumption, emissions):

        prompt = f"""
        You are an AI sustainability assistant.

        Here is the company's energy data:

        Electricity consumption: {consumption} kWh
        Carbon emissions: {emissions} kg CO2e

        Please explain these results and suggest
        practical ways to reduce energy consumption
        and carbon emissions.

        Only use the provided data.
        Do not invent numbers.
        """

        return prompt

    # Send prompt to Ollama and receive a response
    def generate_response(self, prompt):

        data = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }).encode("utf-8")

        request = Request(
            "http://localhost:11434/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urlopen(request, timeout=180) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

            return result.get("response", "")

        except (URLError, HTTPError, TimeoutError) as error:
            return f"AI service error: {error}"
