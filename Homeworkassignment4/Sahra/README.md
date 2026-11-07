# Hometask 4 – Exception Handling and Unit Tests

**Project:** Carbon Compass AI  
**Student:** Sahra Özçelik  
**Subsystem:** Data Management

## Overview
This homework focuses on error handling and automated testing for the Data Management subsystem using Python and Flask.

## Files
- `app.py` – Flask application with error handling.
- `data_management_error.py` – Custom exception class.
- `test_app.py` – Four automated unit tests.
- `requirements.txt` – Required Python packages.

## Error Handling
The `DataManagementError` class is used to handle invalid electricity consumption values. For example, negative electricity consumption is rejected with an HTTP 400 response and a clear error message.

## Automated Tests
Four tests were implemented:

1. `test_missing_fields` – Checks that missing required fields are rejected.
2. `test_negative_consumption` – Checks that negative electricity consumption is rejected.
3. `test_invalid_consumption` – Checks that non-numeric electricity consumption is rejected.
4. `test_get_records` – Checks that the API correctly returns consumption records.

All four tests passed successfully.

## Running the Tests
Install the required packages:

```bash
pip install -r requirements.txt
```

Run the tests from this folder:

```bash
python -m unittest test_app.py -v
```

## Notes
The tests use mocking to avoid modifying the real MySQL database.

This folder contains the Data Management contribution to Hometask 4. The complete group application requires 15 different automated tests across all subsystems.