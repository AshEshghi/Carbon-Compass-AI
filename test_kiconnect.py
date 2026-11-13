
from ai_service import AIService

ai = AIService()

print("Model:", ai.get_model())

prompt = "Say hello in one short sentence."

response = ai.generate_response(prompt)

print("\nAI Response:")
print(response)
