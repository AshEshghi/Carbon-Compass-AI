
from flask import Flask, jsonify, request
import mysql.connector
from getpass import getpass
from data_management_error import DataManagementError

app = Flask(__name__)
@app.errorhandler(DataManagementError)
def handle_data_error(error):
    return jsonify({"error": str(error)}), 400

password = getpass("MySQL password: ")


@app.route("/")
def home():
    return jsonify({
        "project": "Carbon Compass AI",
        "subsystem": "Data Management",
        "status": "API is running"
    })


@app.route("/records")
def get_records():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="carbon_compass"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM consumption_records")
    records = cursor.fetchall()

    cursor.close()
    connection.close()

    for record in records:
        record["timestamp"] = record["timestamp"].isoformat()

    return jsonify(records)


@app.route("/records", methods=["POST"])
def add_record():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON data is required"}), 400

    required = ["building_id", "timestamp", "electricity_kwh"]

    if any(field not in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        kwh = float(data["electricity_kwh"])
        if kwh < 0:
            raise DataManagementError("Electricity consumption cannot be negative")
    except (ValueError, TypeError):
        return jsonify({"error": "Electricity consumption must be a number"}), 400
    
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="carbon_compass"
    )

    cursor = connection.cursor()

    cursor.execute(
        """INSERT INTO consumption_records
        (building_id, timestamp, electricity_kwh)
        VALUES (%s, %s, %s)""",
        (data["building_id"], data["timestamp"], data["electricity_kwh"])
    )

    connection.commit()
    record_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Record added successfully",
        "record_id": record_id
    }), 201

if __name__ == "__main__":
    app.run(port=5050, debug=False)
