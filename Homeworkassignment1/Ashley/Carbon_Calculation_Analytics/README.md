# Carbon Calculation & Analytics — HA1

Part of Carbon Compass AI. This subsystem takes validated electricity consumption records from Data Management, applies an emission factor, and generates monthly and building-level summaries. It does not create or modify database tables.

## Requirements

All analytics classes have constructors, initialization routines, getters and setters where applicable, and input validation. `CarbonCalculator` inherits from the abstract `BaseCalculator` and implements the `calculate()` method (inheritance and polymorphism).

Analytics-specific classes:

- `EmissionFactor` — factor value, reference year, region, source.
- `CarbonCalculator` — validates records/factors and calculates emissions.
- `EmissionResult` — keeps the calculated value and original record ID.
- `AnalyticsService` — monthly totals, comparisons, summaries and CSV export.
- `BaseCalculator` — shared abstract calculator interface.

`ConsumptionRecord` belongs to Sahra's `Data_Management` subsystem and is imported directly. No duplicate version is included here.

## Expected shared project layout

```text
Carbon_Compass_AI/
  Data_Management/
    consumption_record.py
    database_manager.py
    csv_validation.py
    csv_importer.py
    data_validator.py
    electricity.csv
  Carbon_Calculation_Analytics/
    carbon_calculator.py
    emission_factor.py
    emission_result.py
    analytics_service.py
    validation.py
    demo.py
    test_carbon_analytics.py
  run_analytics_demo.py
  docs/
    ANALYTICS_UML.md
    INTEGRATION_NOTES.md
  .gitignore
```

## Run with VS Code / terminal

Open `Carbon_Compass_AI` (the parent folder with both subsystem folders) in VS Code, and run `run_analytics_demo.py` with the Play button, or use the terminal:

```bash
python run_analytics_demo.py
python -m unittest discover -s Carbon_Calculation_Analytics -p "test_*.py" -v
```

No third-party packages are required for these HA1 analytics files. Python 3.10+ is recommended. `__init__.py` is optional for these namespace packages; `__init__()` class constructors are still present.

## Test-data disclaimer

The example factor of 0.4 kg CO2e/kWh is a hypothetical programming value, not an official or verified emissions factor. A geographically and methodologically appropriate factor must be selected for the final capstone.

## Team integration

See `docs/INTEGRATION_NOTES.md` and the UML in `docs/ANALYTICS_UML.md`. In the complete HA1 team submission, use the `Homeassignment1` branch and include the team overview, all four UML diagrams, and a 3–5-minute group video link in the root README.
