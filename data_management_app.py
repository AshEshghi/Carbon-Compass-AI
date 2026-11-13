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
        start_date = request.args.get("start_date", "2016-01-01")
        end_date = request.args.get("end_date", "2016-12-31")

        records = database.fetch_records(
            start_date=start_date,
            end_date=end_date
        )

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