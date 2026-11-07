# Hometask 1 — Web Interface (Büsra Aydın)

## Contribution

This subsystem provides the Streamlit user interface for **Carbon Compass AI — Enterprise Carbon Footprint Tracker & AI Assistant**.

## Python Classes

- `AppController`: Tracks the selected page and delegates calls to services.
- `DashboardPage`: Holds dashboard labels and electricity/emissions totals.
- `DataUploadPage`: Holds the selected file name and validation results.
- `AnalyticsPage`: Holds the reporting period and emissions series.
- `AssistantPage`: Stores an AI question and response attributes.

Each page/controller class demonstrates object initialization and accessor methods. The interface connects to the team's Data Management, Carbon Calculation & Analytics, and AI Assistant modules through `app.py`.

## User Workflow

1. Open **Upload Data** and select a CSV containing timestamps and `electricity_kwh`.
2. Review the preview, valid-record count, and validation messages.
3. Open **Dashboard** to see calculated electricity and emissions totals.
4. Open **Analytics** to see monthly emissions and choose a reporting month.
5. Open **AI Assistant** to ask a question using the calculated totals. This requires Ollama and the `llama3.2:1b` model to be running locally.

## Run from the Project Root

```bash
python3 -m pip install streamlit pandas altair
ollama pull llama3.2:1b
python3 -m streamlit run Web_Interface/app.py
```

Ollama must be installed and its local service available on `http://localhost:11434` for AI answers. Other dependencies are part of the Python standard library.

## UML

- [Editable Web Interface UML](Web_Interface_UML.drawio)
- [Web Interface UML image](Web_Interface_UML.drawio.png)

## Notes

The application uses an **illustrative** emission factor of 0.4 kg CO2e/kWh for its example calculation, not an official inventory factor.

The uploaded sample contains a duplicate row that is rejected during validation.

This is an educational prototype, not a production emissions reporting application.

## Team Submission

The team-level README at the repository root lists subsystem owners, UML locations, and the video-link placeholder.

The five-minute team video must be recorded and linked before submission.
