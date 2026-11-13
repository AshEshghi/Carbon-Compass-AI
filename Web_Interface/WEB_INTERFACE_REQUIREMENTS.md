# Carbon Compass AI — Web Interface Requirements

**Project:** Enterprise Carbon Footprint Tracker & AI Assistant  
**Group:** 29 — Topic 3  
**Subsystem:** Web Interface (Streamlit)  
**Responsible team member:** Büşra Aydın  
**Scope:** Educational MVP using sample electricity consumption and an illustrative emissions factor.

## 1. Functional Requirements (FR)

| ID | Requirement | Implementation evidence | Assessment |
|---|---|---|---|
| FR-01 | The interface shall provide navigation between Dashboard, Upload Data, Analytics, and AI Assistant pages. | `Web_Interface/app.py` (`st.sidebar.radio`), `app_controller.py` | Implemented |
| FR-02 | The interface shall allow the user to select and upload a CSV file. | `app.py` (`st.file_uploader`) | Implemented |
| FR-03 | The interface shall display a preview of the uploaded CSV data. | `app.py` (`st.dataframe(preview.head(10))`) | Implemented |
| FR-04 | The interface shall invoke CSV validation and display valid-record counts and validation errors. | `app.py`, `data_upload_page.py`, Data Management validation | Implemented; integration tested manually |
| FR-05 | The interface shall retrieve electricity-consumption records from the Data Management API backed by MySQL. | `data_api.py` (`GET /records`), `app.py` (Load Records from Database) | Implemented; integration tested manually |
| FR-06 | The Dashboard shall display total electricity consumption in kWh. | `app.py` (`st.metric`), `dashboard_page.py` | Implemented; displayed in manual test |
| FR-07 | The Dashboard shall display total estimated carbon emissions in kg CO2e. | `app.py` (`st.metric`), `dashboard_page.py` | Implemented; displayed in manual test |
| FR-08 | The Analytics page shall visualize monthly emissions in a chart. | `app.py` (Altair bar chart), `analytics_page.py` | Implemented; manually demonstrated |
| FR-09 | The Analytics page shall let the user select a reporting month and view its emissions value. | `app.py` (`st.selectbox`, `st.metric`) | Implemented |
| FR-10 | The AI Assistant page shall accept a user question and display an AI-generated response based on the calculated electricity and emissions summary. | `app.py`, `assistant_page.py`, `AI_Sustainability_Assistant/ai_service.py` | Implemented; live KI:connect response tested |

## 2. Non-Functional Requirements (NFR)

*The thresholds below are **proposed acceptance criteria**, not claims that performance or other quality tests have already passed.*

| ID | Requirement / acceptance criterion | Implementation evidence or verification approach | Assessment |
|---|---|---|---|
| NFR-01 | On a supported laptop browser, the four main pages shall be usable without horizontal scrolling at a viewport width of 1280 px. | Streamlit wide layout; verify at 1280 px | Not verified |
| NFR-02 | Navigation between pages shall complete within 2 seconds for at least 95% of local test interactions, excluding external API waits. | Time 20 navigation actions | Not verified |
| NFR-03 | Rendering Dashboard and Analytics from an already calculated 274-record summary shall take no more than 3 seconds on the target laptop. | Time UI rendering in local demo environment | Not verified |
| NFR-04 | The interface shall label electricity values in kWh and carbon emissions in kg CO2e consistently across KPI cards and charts. | `app.py` labels and Altair axis | Implemented; visual review recommended |
| NFR-05 | When the Data Management API is unavailable, the interface shall show an understandable warning instead of terminating the application. | `data_api.py` returns `None` on request errors; `app.py` warns | Implemented; failure test not yet recorded |
| NFR-06 | The interface shall prevent an empty question from being submitted to the AI service and provide a user-facing validation message. | `app.py` checks `question.strip()` | Implemented; manual test recommended |
| NFR-07 | API credentials shall not be hard-coded in Web Interface source files or committed to the repository. | KI:connect key loaded from `.env`; root `.gitignore` excludes `.env` | Implemented for current setup; recheck repository history and deployments |
| NFR-08 | The Web Interface shall keep page/controller logic separate from Data Management, calculation, and AI service implementations. | `app_controller.py`, page classes, imported subsystem interfaces | Partially implemented; `app.py` also contains some calculation logic |
| NFR-09 | The interface shall label emissions based on the 0.4 kg CO2e/kWh demonstration factor as illustrative, not official reporting values. | Analytics caption and demo factor metadata | Partially implemented; disclaimer should also appear on Dashboard and AI Assistant |
| NFR-10 | External Data Management requests shall time out within 10 seconds and yield a recoverable UI error when unreachable. | `data_api.py` uses `timeout=10` and catches `RequestException` | Implemented in code; timeout test not yet recorded |

## 3. Manual Verification Evidence

- Loaded Building 1 records for January–September 2016 through the database-backed interface.
- Displayed calculated electricity consumption of approximately **1,396,657.01 kWh** and estimated emissions of **558,662.80 kg CO2e** (illustrative factor **0.4 kg CO2e/kWh**).
- Successfully asked the AI Assistant about total consumption, emissions, and possible reduction measures; KI:connect returned an answer using the calculated values.
- These are **manual integration observations**. They do not substitute for automated unit tests or performance/security testing.

## 4. Outstanding Work Before Final Submission

- Run and document NFR acceptance checks, especially responsiveness, error handling, and timeout behavior.
- Display the illustrative emissions-factor disclaimer consistently on Dashboard and AI Assistant pages.
- Review error handling around CSV reading and AI failures so technical exception details are not exposed to end users.
- Add Web Interface unit tests where practicable and include the results in the final presentation.
- Ensure this document and the complete team-wide requirements are linked in the project's README.

**Reference implementation:** `Web_Interface/app.py`, `app_controller.py`, `analytics_page.py`, `assistant_page.py`, `dashboard_page.py`, `data_api.py`, and `data_upload_page.py`, branch `busra-final-integration`.
