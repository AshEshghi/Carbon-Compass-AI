# Carbon Compass AI
### Enterprise Carbon Footprint Tracker & AI Assistant

**Group 29 – Topic 3**

## 1. Project Overview

Carbon Compass AI is a Python-based application designed to track electricity consumption, calculate estimated carbon emissions, visualize energy data, and provide AI-powered sustainability recommendations.

The application integrates four subsystems and uses Streamlit, Flask, MySQL, and the KI:connect AI API.

## 2. Team Members and Responsibilities

| Team Member | Subsystem |
|---|---|
| Sahra Özcelik | Data Management |
| Ashley Eshghi | Carbon Calculation & Analytics |
| Nooshin Janizadeh | AI Sustainability Assistant |
| Büşra Aydın | Web Interface |

## 3. Main Features

- Upload and validate electricity consumption CSV files.
- Retrieve electricity records from a MySQL database.
- Display electricity consumption and carbon emission KPIs.
- Visualize monthly carbon emission trends.
- Select reporting periods.
- Ask sustainability questions using the AI Assistant.
- Display AI recommendations alongside calculated building data.

## 4. System Architecture

The application consists of four integrated subsystems.

**Data Management:** Handles electricity consumption records, CSV validation, database storage, and data retrieval through a Flask API.

**Carbon Calculation & Analytics:** Calculates estimated CO₂e emissions and prepares monthly analytics.

**AI Sustainability Assistant:** Uses KI:connect to generate sustainability recommendations based on the available data.

**Web Interface:** Uses Streamlit to connect the subsystems and provide a user-friendly application.

## 5. Technologies

- Python
- Streamlit
- Flask
- MySQL
- Pandas
- Altair
- OpenAI-compatible Python SDK
- KI:connect API
- Git and GitHub

## 6. Running the Application Locally

Install the required Python dependencies in a virtual environment, including Streamlit, Flask, Pandas, Altair, Requests, MySQL Connector, OpenAI SDK, and python-dotenv.

Configure a local `.env` file with the KI:connect API credentials and model settings. Never commit the `.env` file or API keys to GitHub.

Start the Data Management Flask API from the project root:

```bash
.venv/bin/python -m Data_Management.app
```

The Data Management API runs locally on port **5050** and requires a configured MySQL database.

Start the Streamlit Web Interface:

```bash
.venv/bin/python -m streamlit run Web_Interface/app.py
```

Open the local URL displayed by Streamlit in your browser.

The application provides four pages:

1. Dashboard
2. Upload Data
3. Analytics
4. AI Assistant

## 7. Example Dataset and Emission Factor

The integrated demonstration uses electricity consumption records for Building 1 from January to September 2016.

The carbon calculation currently uses a **hypothetical emission factor of 0.4 kg CO₂e/kWh**.

The calculated emissions are illustrative and must not be interpreted as an official or independently verified carbon inventory.

## 8. Requirements and UML Diagrams

The Web Interface subsystem includes:

- 10 Functional Requirements
- 10 Non-Functional Requirements
- Final UML Class Diagram

Files are available under:

`Web_Interface/WEB_INTERFACE_REQUIREMENTS.md`

`Web_Interface/UML/`

Each subsystem is responsible for maintaining its own requirements, diagrams, and implementation documentation.

## 9. Testing

The integrated application has been manually checked for CSV upload and validation, MySQL data retrieval, dashboard KPIs, monthly emission visualization, and KI:connect AI responses.

Additional automated test results and final validation evidence will be included as part of the team submission.

## 10. Project Status

The core integrated application has been demonstrated locally.

Final team deliverables, including Docker configuration verification, consolidated testing evidence, screencast, and presentation, are to be finalized before submission.

## 11. Academic Disclaimer

This application is an educational minimum viable product developed as part of the Medical Informatics Master's program at FH Dortmund.

It is not intended for certified