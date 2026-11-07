# HA3 - Carbon Calculation & Analytics

**Project:** Carbon Compass AI  
**Subsystem:** Carbon Calculation & Analytics  
**Team role:** Ashley  

## Description

A Flask analytics endpoint reads validated electricity consumption data from the existing MySQL `carbon_compass` database and calculates simple monthly carbon emissions estimates. The `0.4 kg CO2e/kWh` factor is **hypothetical**, not an official emissions inventory factor.

## Files

- `Carbon_Calculation_Analytics/analytics_api.py`: calculation class and Flask route
- `Carbon_Calculation_Analytics/test_analytics.py`: unit and mocked endpoint tests
- `requirements.txt`: dependencies

## Database

Uses Sahra's existing MySQL table (does not create or modify it):

```sql
CREATE DATABASE IF NOT EXISTS carbon_compass;
USE carbon_compass;
CREATE TABLE IF NOT EXISTS consumption_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    building_id INT NOT NULL,
    timestamp DATE NOT NULL,
    electricity_kwh DOUBLE NOT NULL
);
```

## Install and run on Windows

Use MySQL Community Server locally and create the database/table from the SQL above. Install Python packages with:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the server from the project root:

```powershell
.\.venv\Scripts\python.exe Carbon_Calculation_Analytics\analytics_api.py
```

Enter **your own local MySQL root password**. Open:

`http://127.0.0.1:5051/analytics?building_id=1`

Run unit and mocked endpoint tests without a running MySQL server:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s Carbon_Calculation_Analytics -p "test_*.py" -v
```

## Team integration

Use a **single Flask application**. To add the analytics endpoint to Sahra's `app.py`, import `analytics_bp` from this file (with a correct project-root Python import path), then add two lines after her Flask app is created and password is collected:

```python
app.config["MYSQL_PASSWORD"] = password
app.register_blueprint(analytics_bp)
```

Then `http://127.0.0.1:5050/records` and `http://127.0.0.1:5050/analytics?building_id=1` will be served by the same Flask application. Do not run the separate analytics server once integrated.

No extra MySQL account, table, or SQLite file is required for the analytics module. Avoid committing MySQL passwords or `.venv`.
