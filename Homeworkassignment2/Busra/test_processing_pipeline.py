from Web_Interface.processing_pipeline import ProcessingPipeline
from Carbon_Calculation_Analytics.scope_filter import ScopeFilter
from Carbon_Calculation_Analytics.emission_transformer import EmissionTransformer
from Carbon_Calculation_Analytics.demo_ashley import FACTOR_CONFIG
from Data_Management.energy_stream import EnergyStream
from AI_Sustainability_Assistant.insight_processor import InsightProcessor

pipeline = (
    ProcessingPipeline()
    | ScopeFilter((2,))
    | EmissionTransformer(FACTOR_CONFIG)
)

record = {
    "record_id": 1,
    "building_id": 1,
    "timestamp": "2026-01-01",
    "electricity_kwh": 120,
    "scope": 2
}

result = pipeline.process(record)

print("Pipeline result:")
print(result)
print("Emissions:", result["emissions_tonnes_co2e"], "t CO2e")
filtered_record = {
    "record_id": 2,
    "building_id": 1,
    "timestamp": "2026-01-02",
    "electricity_kwh": 150,
    "scope": 1
}

filtered_result = pipeline.process(filtered_record)

print("Filtered result:", filtered_result)
records = [
    {
        "record_id": 3,
        "building_id": 1,
        "timestamp": "2026-01-03",
        "electricity_kwh": 200,
        "scope": 2
    },
    {
        "record_id": 4,
        "building_id": 1,
        "timestamp": "2026-01-04",
        "electricity_kwh": 100,
        "scope": 1
    }
]

stream = EnergyStream(records)

print("Stream results:")

for result in pipeline.process_stream(stream):
    print(
        "Record:", result["record_id"],
        "Emissions:", result["emissions_tonnes_co2e"], "t CO2e"
    )
    records = [
    {
        "record_id": 3,
        "building_id": 1,
        "timestamp": "2026-01-03",
        "electricity_kwh": 200,
        "scope": 2
    },
    {
        "record_id": 4,
        "building_id": 1,
        "timestamp": "2026-01-04",
        "electricity_kwh": 100,
        "scope": 1
    }
]

stream = EnergyStream(records)

print("Stream results:")

for result in pipeline.process_stream(stream):
    print(
        "Record:", result["record_id"],
        "Emissions:", result["emissions_tonnes_co2e"], "t CO2e"
    )
print("Four subsystem integration test:")

complete_pipeline = pipeline | InsightProcessor()

test_record = {
    "record_id": 5,
    "building_id": 1,
    "timestamp": "2026-01-05",
    "electricity_kwh": 120,
    "scope": 2
}

result = complete_pipeline.process(test_record)

print("Emissions:", result["emissions_tonnes_co2e"], "t CO2e")
print("AI Insight:", result["ai_insight"])