from ai_service import AIService

# Create AIService object
ai = AIService()

# Build prompt
prompt = ai.build_prompt(
    consumption=1500,
    emissions=650
)

# Get AI response
response = ai.generate_response(prompt)

# Print response
print(response)