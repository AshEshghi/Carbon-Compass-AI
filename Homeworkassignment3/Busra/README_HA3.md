# Hometask 3 – Flask & MySQL Web Interface

**Student:** Büşra Aydın  
**Project:** Carbon Compass AI  
**Subsystem:** Web Interface

## Overview

This project demonstrates a Flask web application connected to a MySQL database. The Web Interface retrieves electricity consumption records from MySQL and displays them in an HTML table.

It also integrates with the Data Management REST API developed by Sahra Özçelik.

## Technologies

- Python 3
- Flask
- MySQL
- MySQL Connector/Python
- HTML

## Web Interface Files

- `flask_app.py` – Creates the Flask application and displays electricity consumption records.
- `mysql_connection.py` – Establishes a MySQL connection using an environment variable for the password.
- `requirements.txt` – Lists the Python dependencies in the main project folder.

## MySQL Database

**Database:** `carbon_compass`

**Table:** `electricity_records`

The table stores:

- `id` – Record identifier
- `record_date` – Electricity consumption date
- `electricity_kwh` – Electricity consumption in kWh

## Data Management Integration

The Web Interface is integrated with Sahra's Data Management API.

Sahra's API uses the `consumption_records` table and provides:

- `GET /records` – Retrieves electricity consumption records.
- `POST /records` – Adds a new electricity consumption record.

The Data Management API runs on port `5050`.

The Web Interface runs on port `5000` and displays Sahra's records at:

`http://127.0.0.1:5000/sahra-records`

The integration was successfully tested using sample electricity consumption data.
## Carbon Analytics Integration

The Flask Web Interface is also integrated with Ashley's Carbon Analytics API.

The Analytics API reads electricity consumption records from MySQL
and calculates estimated carbon emissions.

The Web Interface displays the results at:

http://127.0.0.1:5000/analytics

This integration was successfully tested using sample data
and a hypothetical emission factor.

## How to Run

1. Install the dependencies from the project's `requirements.txt`.
2. Start the MySQL server and create the required database tables.
3. Configure the `MYSQL_PASSWORD` environment variable for the Web Interface.
4. Start Sahra's Data Management API on port `5050`.
5. Start the Web Interface with:

   `python Web_Interface/flask_app.py`

6. Open the following pages:

   - `http://127.0.0.1:5000/` – Electricity records from the Web Interface's MySQL table.
   - `http://127.0.0.1:5000/sahra-records` – Electricity records retrieved from Sahra's API.

## Testing

The following operations were successfully tested:

- Flask application startup.
- MySQL database connection.
- Retrieval and display of electricity consumption records.
- Data Management API GET and POST requests.
- Integration between the Data Management API and the Flask Web Interface.

The data used for testing is illustrative.

## GitHub Submission

This Web Interface module is part of the Carbon Compass AI group project. The final repository README should include the complete project information, group members, setup instructions and repository submission details.