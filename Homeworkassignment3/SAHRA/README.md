# Hometask 3 – Data Management

**Project:** Carbon Compass AI  
**Student:** Sahra Özçelik  
**Subsystem:** Data Management

## Overview

This subsystem uses Flask and MySQL to store and retrieve electricity consumption records through a REST API.

## Technologies

- Python
- Flask
- MySQL
- mysql-connector-python

## Features

- Connect to a MySQL database
- Retrieve electricity consumption records using a GET request
- Add electricity consumption records using a POST request
- Return data in JSON format

## Database Setup

Create a MySQL database named `carbon_compass`.

Run the following SQL statements:

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

## How to Run

1. Make sure the MySQL server is running.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Run the application using `python app.py`.
4. Enter your local MySQL password when prompted.
5. Open `http://127.0.0.1:5050/records` to view consumption records.

## API Endpoints

**GET /records**

Retrieves electricity consumption records from MySQL.

**POST /records**

Adds a new electricity consumption record.

Example JSON request:

```json
{
  "building_id": 1,
  "timestamp": "2026-01-02",
  "electricity_kwh": 150.0
}
```

## Testing

The API was tested locally with sample electricity consumption records. GET and POST requests were successfully executed against the MySQL database.

Sample data is used for demonstration purposes.

## Project Scope

This contribution focuses on Data Management. Carbon Calculation and Analytics, AI Sustainability Assistant, and Web Interface are handled by the other team members.