from Carbon_Calculation_Analytics.integration import calculate_2016_records
import streamlit as st
from data_api import get_records
from dashboard_page import DashboardPage
from data_upload_page import DataUploadPage
from pathlib import Path
import sys
import pandas as pd
import tempfile
import altair as alt
from app_controller import AppController
from analytics_page import AnalyticsPage
from assistant_page import AssistantPage
project_folder = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_folder))
from AI_Sustainability_Assistant.ai_service import AIService

from Data_Management.csv_validation import validate_csv
from Carbon_Calculation_Analytics.carbon_calculator import CarbonCalculator
from Carbon_Calculation_Analytics.emission_factor import EmissionFactor
from Carbon_Calculation_Analytics.analytics_service import AnalyticsService
st.set_page_config(
    page_title="Carbon Compass AI",
    layout="wide"
)

st.title("Carbon Compass AI")

st.write("Enterprise Carbon Footprint Tracker & AI Assistant")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Upload Data", "Analytics", "AI Assistant"]
)
if "analytics_summary" not in st.session_state:
    st.session_state.analytics_summary = None
if "monthly_emissions" not in st.session_state:
    st.session_state.monthly_emissions = {}
controller = AppController(page)
page = controller.route_page()





if page == "Dashboard":
    st.header("Dashboard")

    summary = st.session_state.analytics_summary

    if summary is not None:
        dashboard = DashboardPage(
            "Carbon Compass AI",
            summary["total_electricity_kwh"],
            summary["total_emissions_kgco2e"]
        )

        st.info(
    f"Calculated from {st.session_state.get('data_source', 'uploaded CSV data')}"
)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Electricity Consumption",
                f"{dashboard.get_total_kwh():,.2f} kWh"
            )

        with col2:
            st.metric(
                "Total Carbon Emissions",
                f"{dashboard.get_total_co2():,.2f} kg CO2e"
            )

    else:
        st.info("Upload a CSV file to see your results.")




        
elif page == "Upload Data":
    st.header("Upload Data")

    st.subheader("MySQL Database Records (2016)")

    
    if st.button("Load Records from Database"):
        # Clear previous results before loading new database data
        st.session_state.pop("analytics_summary", None)
        st.session_state.pop("monthly_emissions", None)
        st.session_state.pop("data_source", None)

        records = get_records()

        if records is None:
            st.warning(
                "Data Management API is not available. "
                "Please start the API on port 5050."
            )

        elif records:
            st.success(f"Loaded {len(records)} records from MySQL.")
            st.dataframe(pd.DataFrame(records))

            # Use only Building 1, January–September 2016
            records_2016 = [
                record for record in records
                if str(record["timestamp"])[:7] >= "2016-01"
                and str(record["timestamp"])[:7] <= "2016-09"
                and record.get("building_id") == 1
            ]

            if records_2016:
                try:
                    summary, monthly = calculate_2016_records(
                        records_2016, building_id=1
                    )

                    st.session_state.analytics_summary = summary
                    st.session_state.monthly_emissions = monthly
                    st.session_state.data_source = "MySQL Database"

                    st.success(
                        "Dashboard and Analytics updated from MySQL records."
                    )

                except (ValueError, TypeError, KeyError) as error:
                    st.error(f"Analytics calculation failed: {error}")

            else:
                st.warning("No valid 2016 records found for Building 1.")

        else:
            st.info("No database records found.")


    uploaded_file = st.file_uploader(
        "Upload your CSV file",
        type=["csv"]
)

    if uploaded_file is not None:
        upload_page = DataUploadPage(uploaded_file.name)

        st.write("File name:", upload_page.get_file_name())

        st.subheader("Data Preview")

        uploaded_file.seek(0)
        preview = pd.read_csv(uploaded_file)

        st.dataframe(preview.head(10))


        with tempfile.TemporaryDirectory() as folder:
            file_path = Path(folder) / "uploaded.csv"
            file_path.write_bytes(uploaded_file.getvalue())

            result = controller.call_service(validate_csv, file_path)

        

        valid_records = result["valid_records"]
        # Clear previous results before processing a new CSV
        st.session_state.pop("analytics_summary", None)
        st.session_state.pop("monthly_emissions", None)
        st.session_state.pop("data_source", None)

        if valid_records:
            factor = EmissionFactor(
                1, "DEMO", 2016, 0.4,
                "Hypothetical example factor"
            )

            calculator = CarbonCalculator()

            emission_results = [
                calculator.calculate(record, factor)
                for record in valid_records
            ]

            analytics_service = AnalyticsService(emission_results)

            st.session_state.analytics_summary = analytics_service.summary()
            st.session_state.monthly_emissions = analytics_service.aggregate_monthly()
            st.session_state.data_source = "uploaded CSV data"

        upload_page.set_validation_result(result)

        validation = upload_page.render_validation()

        st.write("Valid records:", validation["valid_count"])
        st.write("Errors:", validation["error_count"])

        if validation["errors"]:
            for error in validation["errors"]:
                st.error(str(error))
        else:
            st.success("CSV validation completed successfully!")





elif page == "Analytics":
    st.header("Analytics")

    monthly_data = st.session_state.monthly_emissions

    if monthly_data:
        selected_month = st.selectbox(
            "Select reporting period",
            list(monthly_data.keys())
        )

        analytics = AnalyticsPage(selected_month)
        analytics.set_emissions(list(monthly_data.values()))

        st.write("Selected period:", analytics.get_selected_period())

        st.subheader("Monthly Emission Trends")
        chart_data = pd.DataFrame(
            list(monthly_data.items()),
            columns=["Month", "Emissions (kg CO2e)"]
        )
        chart = alt.Chart(chart_data).mark_bar(size=45).encode(
            x=alt.X("Month:N", title="Month"),
            y=alt.Y("Emissions (kg CO2e):Q", title="kg CO2e")
        )

        st.altair_chart(chart, use_container_width=True)

      

        st.metric(
            "Selected Month Emissions",
            f"{monthly_data[selected_month]:,.2f} kg CO2e"
        )

        st.caption("Calculated using a hypothetical emission factor.")

    else:
        st.info("Upload a CSV file to view analytics results.")





elif page == "AI Assistant":
    st.header("AI Assistant")

    summary = st.session_state.analytics_summary

    if summary is not None:
        st.success("Energy data is available.")

        question = st.text_input(
            "Ask a sustainability question"
        )

        if st.button("Submit Question"):
            if question.strip():
                assistant = AssistantPage(question)

                ai_service = AIService()

                
                prompt = ai_service.build_prompt(
                summary["total_electricity_kwh"],
                summary["total_emissions_kgco2e"]
                )

                 

                
                prompt += f"""
                USER QUESTION:
                {assistant.get_question()}

                IMPORTANT INSTRUCTIONS:
                1. Start your answer with the verified electricity consumption
                   in kWh and carbon emissions in kg CO2e.
                2. Only use the data provided in this prompt.
                3. Do not describe consumption as high, low, good, or bad
                   unless comparison data is available.
                4. Do not invent comparisons, percentages, savings,
                   predictions, or additional numerical values.
                5. Clearly distinguish verified data from general recommendations.
                6. Explain that the emissions are calculated using a
                   hypothetical emission factor, not an official factor.
                7. Provide practical sustainability recommendations,
                   without claiming specific numerical savings.
                8. If the available data cannot answer a question,
                   clearly explain what information is missing.

                Answer the user's question clearly and concisely.
                """


                with st.spinner("Generating AI response..."):
                    response = ai_service.generate_response(prompt)

                
                st.subheader("Verified Building Data")

                st.metric(
                    "Total Electricity Consumption",
                    f"{summary['total_electricity_kwh']:,.2f} kWh"
                )

                st.metric(
                    "Total Carbon Emissions",
                    f"{summary['total_emissions_kgco2e']:,.2f} kg CO2e"
                )

                st.caption(
                    "Carbon emissions are calculated using a hypothetical "
                    "emission factor of 0.4 kg CO2e/kWh."
                )

                
                if response.startswith("AI service error:"):
                    st.error(
                        "The AI Assistant is temporarily unavailable. "
                        "Please try again later."
                    )
                else:
                    st.subheader("AI Recommendations")
                    st.write(response)



            else:
                st.error("Please enter a question.")

    else:
        st.info("Please upload a CSV file before using the AI Assistant.")
