
from insight_processor import InsightProcessor
from pipeline import Pipeline


# Create two processors
processor1 = InsightProcessor()
processor2 = InsightProcessor()

# Combine processors using +
pipeline = processor1 + processor2

# Sample carbon data
record = {
    "timestamp": "2026-11-01",
    "electricity_kwh": 1500,
    "scope": 2,
    "emissions_kg_co2e": 600,
    "emissions_tonnes_co2e": 0.6
}

# Run the pipeline
result = pipeline.process(record)

print("Pipeline test successful!")
print("Carbon emissions:", result["emissions_kg_co2e"])
print("\nAI Insight:")
print(result["ai_insight"])
