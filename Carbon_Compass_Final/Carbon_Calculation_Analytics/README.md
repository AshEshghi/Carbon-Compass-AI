# Ashley — Final Carbon Calculation & Analytics

- `carbon_calculator.py`, `emission_factor.py`, `emission_result.py`, `analytics_service.py`, and `validation.py` preserve the HA1 classes that Büşra's Streamlit app imports.
- `integration.py` supplies `calculate_2016_records(records)` for records returned by Sahra's `/records` endpoint, producing `(summary, monthly_emissions)` in the **existing Streamlit session-state format**. Input must be one building's 2016 records; rejects mixed years.
- `api/analytics_api.py` supplies the HA4 Flask `analytics_bp` (`GET /analytics`) with **SQL restriction to Jan–Sep 2016**, using MySQL table `carbon_compass.consumption_records`. Import as `from Carbon_Calculation_Analytics.api.analytics_api import analytics_bp`.
- `api/analytics_service.py` and `api/analytics_error.py` preserve HA4 exception handling and JSON summary format, separate from the original HA1 analytics service. The two namespaced services intentionally provide distinct interfaces.
- No team member source files have been changed. Integration requires Büşra to invoke `calculate_2016_records` when loading database records (see `INTEGRATION_REPORT.md`) and Sahra to register the Blueprint and supply DB configuration. Those changes are NOT included in this delivery.
- `streaming/` preserves Ashley's HA2 abstract processors; `streaming_adapter.py` prepares 2016 Scope 2 events and matching factors. The team's existing ProcessingPipeline can compose these processors, but this is not automatically invoked by the Streamlit app.
- Factor 0.4 kg CO2e/kWh is **hypothetical**, not an official 2016 conversion factor.
- The final files are a proposed integration package, not an already-running complete application.

## Additional final-project checks

Use the sibling `Data_Management/` package and run from the shared final project root:

```powershell
python -m pip install Flask mysql-connector-python
python -m unittest discover -s Carbon_Calculation_Analytics -p "test_*.py" -v
```

`test_real_2016_csv.py` verifies the actual 274-row January–September 2016 source file without requiring MySQL. `test_analytics_api_final.py` mocks the database connector to check the Flask endpoint and its HTTP error statuses. The final API service now validates 2016 dates and expected building IDs after the existing SQL date filter.

**Note:** The seven new API tests are skipped if their Python packages are not installed. This folder is still a proposed package until Sahra registers its Blueprint and Büşra calls its Streamlit bridge. Refer to `ASHLEY_CHANGES_AND_TEAM_ACTIONS.md` for teammate-specific actions.
