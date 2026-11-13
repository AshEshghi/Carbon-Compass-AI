
from insight_processor import InsightProcessor


# Create a sample record similar to Ashley's output
sample_record = {
    "timestamp": "2026-11-01",
    "electricity_kwh": 1500,
    "scope": 2,
    "emissions_kg_co2e": 600,
    "emissions_tonnes_co2e": 0.6
}


# Create the processor
processor = InsightProcessor()

# Process the record
result = processor.process(sample_record)

# Display the results
print("Carbon emissions:", result["emissions_kg_co2e"])
print("\nAI Insight:")
print(result["ai_insight"])
