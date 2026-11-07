# Hometask 3 – Data Management

**Project:** Carbon Compass AI  
**Student:** Sahra Ozcelik  
**Subsystem:** Data Management

## Overview

This subsystem uses Flask and MySQL to store and retrieve electricity consumption records through a REST API.

In Hometask 1 and 2, SQLite was used for data storage. For Hometask 3, MySQL is used to demonstrate database access through a Flask application.

## Technologies

- Python
- Flask
- MySQL
- mysql-connector-python
- SQLite (used in Hometask 1 and 2)

## Features

- Connect to a MySQL database
- Retrieve electricity consumption records using a GET request
- Add electricity consumption records using a POST request
- Return data in JSON format
- Support transferring existing SQLite records to MySQL
- Provide a MySQL database export for other team members

## Project Files

The `Data_Management` folder contains:

- `app.py` – Flask application with GET and POST endpoints
- `test_mysql.py` – Tests the MySQL database connection
- `migrate_sqlite_to_mysql.py` – Transfers records from SQLite to MySQL
- `carbon_compass_mysql.sql` – MySQL database structure and sample records

The `requirements.txt` file contains the required Python packages.

## Database Setup

### Option 1: Import the Existing MySQL Database (Recommended)

The `carbon_compass_mysql.sql` file contains the MySQL table structure and two sample electricity consumption records.

Team members can use this file to set up the same database on their own computers.

**Step 1:** Install MySQL and make sure the MySQL server is running.

**Step 2:** Download `carbon_compass_mysql.sql` from the GitHub repository.

**Step 3:** Open a terminal in the `Homeworkassignment3/SAHRA` folder and run:

```bash
mysql -u root -p < Data_Management/carbon_compass_mysql.sql
```

**Step 4:** Enter your own MySQL password when prompted.

The SQL file will create the `carbon_compass` database, the `consumption_records` table, and the two sample records.

This import is intended for a fresh database. If the table already exists, check it before importing to avoid conflicts.

Alternatively, team members can import the SQL file using MySQL Workbench.

### Option 2: Create an Empty Database Manually

If you prefer to start with an empty database, you can execute the following SQL statements in MySQL:

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

This creates the database and table without adding sample records.

**Note:** Choose either Option 1 or Option 2 when setting up a new database. You do not need to perform both.

## SQLite to MySQL Migration

In Hometask 1 and 2, electricity consumption records were stored in an SQLite database named `carbon_compass.db`.

For Hometask 3, the equivalent sample records were already present in MySQL. The migration script was used to check for existing records and prevent duplicates.

The file `migrate_sqlite_to_mysql.py` can be used to transfer missing SQLite records into MySQL.

To run this script, place the original `carbon_compass.db` file in the same folder as the migration script and execute:

```bash
python3 Data_Management/migrate_sqlite_to_mysql.py
```

The script checks whether records already exist in MySQL before inserting them.

**Important:** Team members who import `carbon_compass_mysql.sql` do not need the SQLite database or the migration script. The SQL file already contains the sample records.

## How to Run

### Step 1: Install Required Packages

Open a terminal in the `Homeworkassignment3/SAHRA` folder.

Run:

```bash
python3 -m pip install -r requirements.txt
```

### Step 2: Set Up MySQL

Make sure MySQL is installed and running.

Import `carbon_compass_mysql.sql` as described in the Database Setup section.

Use your own local MySQL username and password.

### Step 3: Start the Flask Application

From the `SAHRA` folder, run:

```bash
python3 Data_Management/app.py
```

Enter your local MySQL password if prompted.

### Step 4: Access the API

Open the following address in your browser:

`http://127.0.0.1:5050/records`

This endpoint retrieves electricity consumption records from the MySQL database.

## API Endpoints

### GET /records

Retrieves electricity consumption records from MySQL and returns them in JSON format.

**Example request:**

```http
GET http://127.0.0.1:5050/records
```

### POST /records

Adds a new electricity consumption record to the MySQL database.

**Example JSON request:**

```json
{
  "building_id": 1,
  "timestamp": "2026-01-02",
  "electricity_kwh": 150.0
}
```

POST requests can be tested using tools such as Postman.

## Testing

The API was tested locally with sample electricity consumption records.

- MySQL database connection was tested.
- GET requests successfully retrieved records.
- POST requests successfully added records.
- SQLite and MySQL records were compared.
- Existing records were not duplicated during the migration check.
- The MySQL database was exported to `carbon_compass_mysql.sql`.

The MySQL export contains two sample electricity consumption records.

All sample data is used for demonstration purposes.

## Notes for Team Members

To use this subsystem on another computer:

1. Download the project files from GitHub.
2. Install the Python packages from `requirements.txt`.
3. Install and start MySQL.
4. Import `carbon_compass_mysql.sql` into your local MySQL server.
5. Configure the MySQL connection in `app.py` using your own local credentials.
6. Run the Flask application.
7. Test the GET and POST endpoints.

Each team member uses their own local MySQL database. No shared MySQL password is required.

## Project Scope

This contribution focuses on the **Data Management** subsystem of Carbon Compass AI.

Other subsystems are developed by the remaining team members:

- Carbon Calculation and Analytics
- AI Sustainability Assistant
- Web Interface

The Data Management subsystem provides the database functionality needed to store and retrieve electricity consumption data for further processing.
