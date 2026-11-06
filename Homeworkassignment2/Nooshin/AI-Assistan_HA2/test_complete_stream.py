
from stream_processor import EventStream, event_generator
from carbon_record_filter import CarbonRecordFilter
from insight_processor import InsightProcessor
from pipeline import Pipeline


# Sample incoming events
records = [
    {
        "timestamp": "2026-11-01",
        "electricity_kwh": 1500,
        "scope": 2,
        "emissions_kg_co2e": 600
    },
    {
        "timestamp": "2026-11-02",
        "electricity_kwh": -200,
        "scope": 2,
        "emissions_kg_co2e": 80
    },
    {
        "timestamp": "2026-11-03",
        "electricity_kwh": 1200,
        "scope": 4,
        "emissions_kg_co2e": 480
    }
]

# Create the stream
stream = EventStream(event_generator(records))

# Create processors
filter_processor = CarbonRecordFilter()
ai_processor = InsightProcessor()

# Compose the pipeline
pipeline = filter_processor + ai_processor

# Process events one by one
for event in stream:
    print("\nIncoming event:", event)

    result = pipeline.process(event)

    if result is not None:
        print("Event processed successfully!")
        print("AI Insight:")
        print(result["ai_insight"])
    else:
        print("Event rejected by the filter.")

    print("-" * 50)
