# Hometask 3 – Web Interface

**Student:** Büsra Aydın  
**Subsystem:** Web Interface  
**Project:** Carbon Compass AI

## Overview

This homework focuses on developing a Flask web application with MySQL database access and API integration.

The Web Interface displays electricity consumption records and carbon emission results from the other subsystems.

## Files

- `flask_app.py` – Flask application containing the web pages and API connections.
- `mysql_connection.py` – MySQL database connection helper.

## Flask Routes

The Web Interface includes four routes:

1. `/` – Displays electricity consumption data from the MySQL database.
2. `/sahra-records` – Displays records retrieved from the Data Management API.
3. `/analytics` – Displays carbon emission results from the Analytics API.
4. `/ai-assistant` – Checks the connection to the AI Assistant API and displays the number of records received.

## Integration

The Web Interface connects to:

- **Data Management (Sahra):** Retrieves electricity consumption records.
- **Carbon Calculation & Analytics (Ashley):** Displays calculated carbon emissions.
- **AI Sustainability Assistant (Nooshin):** Connects to the AI Assistant API to retrieve records.

The application uses Flask, MySQL, and HTTP API requests.

## Running the Application

Start the required Data Management and AI Assistant APIs.

From the integrated project root, run:

```bash
python3 -m Web_Interface.flask_app
```

Open the application at:

`http://127.0.0.1:5000`

The other pages can be accessed through their respective routes.

## Testing

The following functionality was checked locally:

- Data Management API connectivity.
- Analytics API connectivity and emission results.
- AI Assistant API connectivity.
- Display of consumption records and analytics results in the Web Interface.

## Notes

The carbon emission factor used in the example calculations is illustrative and is not intended for official carbon reporting.

The `/ai-assistant` route currently demonstrates API connectivity. It does not yet provide an AI question-and-answer interface.

## Group Submission

The complete project requires the files from all four subsystems, along with the team documentation and video presentation link.
