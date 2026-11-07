from getpass import getpass
from flask import Blueprint, Flask, current_app, jsonify, request
import mysql.connector
try:
    from .analytics_error import AnalyticsError
    from .analytics_service import AnalyticsService
except ImportError:
    from analytics_error import AnalyticsError
    from analytics_service import AnalyticsService
analytics_bp = Blueprint("analytics", __name__)
@analytics_bp.errorhandler(AnalyticsError)
def handle_analytics_error(error):
    return jsonify({"error": str(error)}), error.status_code
@analytics_bp.get("/analytics")
def get_analytics():
    try:
        building_id = int(request.args.get("building_id", "1"))
        if building_id < 1:
            raise ValueError
    except ValueError:
        raise AnalyticsError("building_id must be a positive integer", 400)

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

    summary = AnalyticsService(
        current_app.config.get("EMISSION_FACTOR", 0.4)
    ).summarize(records, building_id)
    return jsonify(summary)
if __name__ == "__main__":
    app = Flask(__name__)
    app.config["MYSQL_PASSWORD"] = getpass("MySQL password: ")
    app.register_blueprint(analytics_bp)
    app.run(port=5051, debug=False)
