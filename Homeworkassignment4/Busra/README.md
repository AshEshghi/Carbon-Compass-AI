# Hometask 4 – Exception Handling and Unit Testing

**Student:** Büsra Aydın  
**Subsystem:** Web Interface  
**Project:** Carbon Compass AI

## Overview

This homework focuses on exception handling and automated testing for the Web Interface subsystem using Python and Flask.

The Web Interface connects to the Data Management and Carbon Calculation & Analytics subsystems and displays their results to users.

## Files

- `error_handler.py` – Custom exception class for Web Interface errors.
- `flask_app.py` – Flask application with error handling and three web routes.
- `test_flask_app.py` – Three automated tests for the Web Interface.
- `mysql_connection.py` – MySQL connection helper used by the dashboard.

## Exception Handling

The `WebInterfaceErrorHandler` class is used to handle errors in the Web Interface.

When the Data Management or Analytics API is unavailable, the application returns an understandable error message with HTTP status code 503.

## Automated Tests

Three different automated tests were implemented:

1. `test_home_page` – Verifies that the dashboard displays electricity consumption data correctly.
2. `test_sahra_records_page` – Verifies that Data Management records are displayed correctly in the Web Interface.
3. `test_analytics_page` – Verifies that carbon emissions results are displayed correctly on the Analytics page.

All three tests passed successfully.

## Running the Tests

From the project root, run:

```bash
python3 -m unittest Web_Interface.test_flask_app -v
```

Expected result:

```text
Ran 3 tests in ...s

OK
```

## Testing Approach

The tests use Python's `unittest` framework and `unittest.mock`.

Mocking allows the Web Interface to be tested without connecting to a real MySQL database or running

## Group Integration

The group has prepared 33 automated test functions across four subsystems:

- Data Management (Sahra): 4 tests
- Carbon Calculation & Analytics (Ashley): 11 tests
- AI Sustainability Assistant (Nooshin): 15 tests
- Web Interface (Büsra): 3 tests

All three Web Interface tests passed successfully.

The complete group test suite has not yet been tested together.

## Group Video

The group video link will be added to the final team README.
