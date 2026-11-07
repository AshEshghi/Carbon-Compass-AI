# Hometask 4 – Carbon Calculation & Analytics

**Project:** Carbon Compass AI  
**Subsystem:** Carbon Calculation & Analytics  
**Contributor:** Ashley Eshghi

## Goal

Handle incorrect electricity and emissions data clearly, and test our existing Flask/MySQL analytics endpoint.

## Files

- `analytics_error.py` — the custom `AnalyticsError` exception.
- `analytics_service.py` — calculations and monthly summaries based on the HA3 design.
- `analytics_api.py` — Flask `/analytics` route with error handling (same table and endpoint as HA3).
- `test_analytics_service.py` — eight calculation and validation tests.
- `test_analytics_api.py` — three Flask endpoint tests using mocked database connections.

## Setup (Windows / VS Code)

Open this folder in VS Code. Then run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s Carbon_Calculation_Analytics -p "test_*.py" -v
```

The 11 tests here and Sahra's four Data Management tests provide **15 distinct group tests**, provided all pass when run together. No MySQL Server is required for these mocked tests.

## Optional: run Flask with a real database

A local or accessible MySQL Server is required only for real database operations. Create the `carbon_compass` database and Sahra's `consumption_records` table, then run:

```powershell
.\.venv\Scripts\python.exe Carbon_Calculation_Analytics\analytics_api.py
```

The example endpoint is `http://127.0.0.1:5051/analytics?building_id=1`.

In the integrated group application, Sahra's Flask app should register `analytics_bp` and provide `MYSQL_PASSWORD`. Keep a single `carbon_compass` database and a single shared Flask server.

**Note:** The default factor (`0.4 kg CO₂e/kWh`) is hypothetical test data, not an official emissions factor. Never commit database passwords or virtual environment folders.
