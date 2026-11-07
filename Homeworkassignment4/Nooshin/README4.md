# Carbon Compass AI – AI Sustainability Assistant

## 1. Project Overview

**Project Name:** Carbon Compass AI  
**Subsystem:** AI Sustainability Assistant  
**Student:** Nooshin Janizadeh  

The AI Sustainability Assistant is one subsystem of the Carbon Compass AI project. It communicates with the Data Management API to retrieve energy consumption records and provides an API for accessing this data.

The application is developed using Python and Flask.

## 2. Technologies Used

- Python
- Flask
- Requests
- MySQL
- MySQL Connector
- Pytest

## 3. Project Structure

```text
AI_Assistant/
│
├── ai_assistant_app.py
├── ai_assistant_error.py
├── context_provider.py
├── mysql_database_manager.py
├── test_ai_assistant_app.py
├── requirements.txt
└── README.md
```

## 4. Main Components

### ai_assistant_app.py
This file creates the Flask application and provides the following endpoints:

- `/` – Displays project information and API status.
- `/records` – Retrieves energy consumption records from the Data Management API.

It also handles custom and unexpected errors.

### ai_assistant_error.py
Defines the custom exception class `AIAssistantError` for handling errors related to the AI Assistant subsystem.

### context_provider.py
Communicates with the Data Management API and retrieves consumption records.

### mysql_database_manager.py
Provides database access functionality for retrieving energy consumption records from MySQL.

### test_ai_assistant_app.py
Contains 15 automated tests that check the application's endpoints, responses, and error-handling functionality.

## 5. Error Handling

The application uses a custom exception class:

`AIAssistantError`

Two types of errors are handled:

- **Custom errors:** Return HTTP status code `503` when the Data Management API is unavailable.
- **Unexpected errors:** Return HTTP status code `500` when an unexpected error occurs.

## 6. Running the Application

### Step 1: Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 2: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 3: Start the Data Management API

The Data Management API must be running on port `5050`.

### Step 4: Start the AI Assistant API

```powershell
python ai_assistant_app.py
```

The application runs at:

```text
http://127.0.0.1:5001
```

### Step 5: Test the endpoints

Open these URLs in your browser:

- Home: http://127.0.0.1:5001/
- Records: http://127.0.0.1:5001/records

## 7. Automated Testing

The project uses **pytest** for automated testing.

To run all 15 tests:

```powershell
python -m pytest test_ai_assistant_app.py -v
```

The tests cover:

1. Home page status code
2. Project name
3. Subsystem name
4. Student name
5. API status
6. Records endpoint status
7. JSON response
8. Empty records
9. First record
10. Second record
11. Connection error
12. Timeout error
13. HTTP error
14. Custom error handler
15. Unexpected error

**Test Result:** All 15 tests passed successfully.

## 8. Project Status

- Flask application created successfully.
- Communication with the Data Management API implemented.
- Custom error-handling class created.
- Error handlers implemented and tested.
- 15 automated tests implemented.
- All 15 tests passed successfully.

## 9. Author

**Nooshin Janizadeh**  
FH Dortmund – Digital Transformation  
Carbon Compass AI Project  
AI Sustainability Assistant Subsystem