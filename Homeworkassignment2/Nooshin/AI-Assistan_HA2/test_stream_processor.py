
from stream_processor import EventStream, event_generator

records = [
    {
        "timestamp": "2026-11-01",
        "electricity_kwh": 1500,
        "emissions_kg_co2e": 600
    },
    {
        "timestamp": "2026-11-02",
        "electricity_kwh": 2000,
        "emissions_kg_co2e": 800
    },
    {
        "timestamp": "2026-11-03",
        "electricity_kwh": 1200,
        "emissions_kg_co2e": 480
    }
]

# Generate events one by one
generated_events = event_generator(records)

# Create an event stream
stream = EventStream(generated_events)

# Consume events
for event in stream:
    print("New event received:")
    print(event)
    print("--------------------")
