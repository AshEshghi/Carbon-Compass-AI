"""Carbon emissions calculations and a Flask endpoint for building electricity data."""

from collections import defaultdict
from datetime import date, datetime
from getpass import getpass
from math import fsum, isfinite

from flask import Blueprint, Flask, current_app, jsonify, request
import mysql.connector
class AnalyticsService:
    def __init__(self, emission_factor=0.4):
        self.emission_factor = float(emission_factor)
        if not isfinite(self.emission_factor) or self.emission_factor < 0:
            raise ValueError("Invalid emission factor")

    def summarize(self, records, building_id=1):
        monthly = defaultdict(list)

        for record in records:
            kwh = float(record["electricity_kwh"])
            if not isfinite(kwh) or kwh < 0:
                raise ValueError("Invalid electricity consumption")

            timestamp = record["timestamp"]
            if isinstance(timestamp, (date, datetime)):
                month = timestamp.strftime("%Y-%m")
            else:
                month = date.fromisoformat(str(timestamp)[:10]).strftime("%Y-%m")
            monthly[month].append(kwh)

        total_kwh = fsum(fsum(values) for values in monthly.values())
        total_kg = total_kwh * self.emission_factor
        return {
            "building_id": building_id,
            "record_count": sum(map(len, monthly.values())),
            "total_electricity_kwh": round(total_kwh, 4),
            "emissions_kg_co2e": round(total_kg, 4),
            "emissions_tonnes_co2e": round(total_kg / 1000, 6),
            "factor_kg_co2e_per_kwh": self.emission_factor,
            "factor_note": "Illustrative factor; not suitable for official carbon reporting",
            "monthly": [
                {
                    "month": month,
                    "electricity_kwh": round(fsum(monthly[month]), 4),
                    "emissions_kg_co2e": round(fsum(monthly[month]) * self.emission_factor, 4),
                }
                for month in sorted(monthly)
            ],
        }


analytics_bp = Blueprint("analytics", __name__)
@analytics_bp.get("/analytics")
def get_analytics():
    try:
        building_id = int(request.args.get("building_id", "1"))
        if building_id < 1:
            raise ValueError
    except ValueError:
        return jsonify({"error": "building_id must be a positive integer"}), 400

    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=current_app.config.get("MYSQL_HOST", "localhost"),
            user=current_app.config.get("MYSQL_USER", "root"),
            password=current_app.config["MYSQL_PASSWORD"],
            database="carbon_compass",
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT record_id, building_id, timestamp, electricity_kwh "
            "FROM consumption_records WHERE building_id = %s",
            (building_id,),
        )
        records = cursor.fetchall()
    except mysql.connector.Error:
        return jsonify({"error": "Database connection or query failed"}), 503
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

    try:
        result = AnalyticsService(
            current_app.config.get("EMISSION_FACTOR", 0.4)
        ).summarize(records, building_id)
    except (KeyError, ValueError, TypeError, OverflowError):
        return jsonify({"error": "Invalid consumption records"}), 422

    return jsonify(result)
if __name__ == "__main__":
    app = Flask(__name__)
    app.config["MYSQL_PASSWORD"] = getpass("MySQL password: ")
    app.register_blueprint(analytics_bp)
    app.run(port=5051, debug=False)
