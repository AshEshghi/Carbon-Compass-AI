from flask import Flask
from Web_Interface.error_handler import WebInterfaceErrorHandler
from Web_Interface.mysql_connection import get_connection
import json
from urllib.request import urlopen

app = Flask(__name__)

@app.errorhandler(WebInterfaceErrorHandler)
def handle_web_interface_error(error):
    return str(error), 503



@app.route("/")
def home():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM electricity_records")
        records = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    html = """
    <h1>Carbon Compass AI</h1>
    <h2>Energy Consumption Dashboard</h2>
    <table border="1" cellpadding="10">
        <tr>
            <th>Date</th>
            <th>Electricity (kWh)</th>
        </tr>
    """

    for record in records:
        html += f"""
        <tr>
            <td>{record['record_date']}</td>
            <td>{record['electricity_kwh']}</td>
        </tr>
        """

    html += "</table>"
    return html

@app.route("/sahra-records")
def sahra_records():
    try:
        with urlopen("http://127.0.0.1:5050/records", timeout=5) as response:
            records = json.load(response)

        html = """
        <h1>Carbon Compass AI</h1>
        <h2>Data Management Records</h2>
        <table border="1" cellpadding="10">
            <tr>
                <th>Record ID</th>
                <th>Building ID</th>
                <th>Date</th>
                <th>Electricity (kWh)</th>
            </tr>
        """

        for record in records:
            html += f"""
            <tr>
                <td>{record['record_id']}</td>
                <td>{record['building_id']}</td>
                <td>{record['timestamp']}</td>
                <td>{record['electricity_kwh']}</td>
            </tr>
            """

        html += "</table>"
        return html
    except Exception as error:
        raise WebInterfaceErrorHandler(
            "Data Management API is not available."
        ) from error 

@app.route("/analytics")
def analytics():
    try:
        with urlopen(
            "http://127.0.0.1:5050/analytics?building_id=1",
            timeout=5
        ) as response:
            data = json.load(response)

        return f"""
        <h1>Carbon Compass AI</h1>
        <h2>Carbon Analytics</h2>
        <p>Building ID: {data['building_id']}</p>
        <p>Total Electricity: {data['total_electricity_kwh']} kWh</p>
        <p>Carbon Emissions: {data['emissions_kg_co2e']} kg CO2e</p>
        <p>Emissions in Tonnes: {data['emissions_tonnes_co2e']} t CO2e</p>
        <p><i>Illustrative emission factor – not for official reporting.</i></p>
        """

    except Exception as error:
        raise WebInterfaceErrorHandler(
            "Analytics API is not available."
        ) from error
if __name__ == "__main__":
    app.run(debug=True)