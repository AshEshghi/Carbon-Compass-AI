
from insight_processor import AssistantProcessor, InsightProcessor
from carbon_record_filter import CarbonRecordFilter


# Create different processor objects
processors = [
    CarbonRecordFilter(),
    InsightProcessor()
]

# Sample valid event
record = {
    "timestamp": "2026-11-01",
    "electricity_kwh": 1500,
    "scope": 2,
    "emissions_kg_co2e": 600
}

# Check the common interface
for processor in processors:

    print("\nProcessor:", type(processor).__name__)

    print(
        "Is AssistantProcessor:",
        isinstance(processor, AssistantProcessor)
    )

    record = processor.process(record)

    if record is None:
        print("Event rejected.")
        break

    print("Process method executed successfully.")

print("\nPolymorphism test completed.")
######polymorphism