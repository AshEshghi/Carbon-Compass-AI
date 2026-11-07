from flask import Flask, jsonify, request
from getpass import getpass
from mysql_database_manager import MySQLDatabaseManager

app = Flask(__name__)

password = getpass("Enter MySQL root password: ")
database = MySQLDatabaseManager(password)


@app.route("/")
def home():
    return jsonify({
        "project": "Carbon Compass AI",
        "subsystem": "Data Management",
        "status": "API is running"
    })


@app.route("/records", methods=["GET"])
def get_records():
    try:
        records = database.fetch_records()

        result = [
            {
                "timestamp": str(record[0]),
                "electricity_kwh": record[1]
            }
            for record in records
        ]

        return jsonify(result)

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(port=5050, debug=False)