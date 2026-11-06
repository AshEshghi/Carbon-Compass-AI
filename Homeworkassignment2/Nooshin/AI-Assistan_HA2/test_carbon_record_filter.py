
from carbon_record_filter import CarbonRecordFilter

processor = CarbonRecordFilter()

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

for record in records:
    result = processor.process(record)

    if result is not None:
        print("Valid event:", result)
    else:
        print("Invalid event rejected.")
