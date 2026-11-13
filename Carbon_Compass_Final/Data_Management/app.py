
from flask import Flask, jsonify, request
import mysql.connector
from getpass import getpass
from pathlib import Path
from tempfile import TemporaryDirectory
from Data_Management.csv_validation import validate_csv

app = Flask(__name__)

password = getpass("MySQL password: ")


@app.route("/")
def home():
    return jsonify({
        "project": "Carbon Compass AI",
        "subsystem": "Data Management",
        "status": "API is running"
    })


# GET records (with optional date filtering)
@app.route("/records")
def get_records():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="carbon_compass"
    )

    cursor = connection.cursor(dictionary=True)

    start_date = request.args.get("start_date", "1000-01-01")
    end_date = request.args.get("end_date", "9999-12-31")

    cursor.execute(
        """SELECT * FROM consumption_records
        WHERE timestamp BETWEEN %s AND %s""",
        (start_date, end_date)
    )

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    for record in records:
        record["timestamp"] = record["timestamp"].isoformat()

    return jsonify(records)


# POST a new record
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
            return jsonify({
                "error": "Electricity consumption cannot be negative"
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "error": "Electricity consumption must be a number"
        }), 400

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
        (data["building_id"], data["timestamp"], kwh)
    )

    connection.commit()
    record_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Record added successfully",
        "record_id": record_id
    }), 201


# Upload and validate CSV
@app.route("/upload-csv", methods=["POST"])
def upload_csv():
    file = request.files.get("file")

    if not file or not file.filename.endswith(".csv"):
        return jsonify({
            "error": "Please upload a CSV file"
        }), 400

    with TemporaryDirectory() as folder:
        path = Path(folder) / "electricity.csv"
        file.save(path)
        result = validate_csv(path)

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="carbon_compass"
    )

    cursor = connection.cursor()
    saved = 0

    try:
        for record in result["valid_records"]:
            values = (
                record["building_id"],
                record["timestamp"],
                record["electricity_kwh"]
            )

            cursor.execute(
                """SELECT 1 FROM consumption_records
                WHERE building_id = %s
                AND timestamp = %s
                AND electricity_kwh = %s
                LIMIT 1""",
                values
            )

            if cursor.fetchone():
                continue

            cursor.execute(
                """INSERT INTO consumption_records
                (building_id, timestamp, electricity_kwh)
                VALUES (%s, %s, %s)""",
                values
            )

            saved += 1

        connection.commit()

    except mysql.connector.Error:
        connection.rollback()
        return jsonify({
            "error": "Database operation failed"
        }), 500

    finally:
        cursor.close()
        connection.close()

    return jsonify({
        "saved_records": saved,
        "validation_errors": result["errors"]
    })


if __name__ == "__main__":
    app.run(port=5050, debug=False)
