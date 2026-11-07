
from flask import Flask, jsonify
from context_provider import ContextProvider
import requests

app = Flask(__name__)

context = ContextProvider(
    api_url="http://127.0.0.1:5050/records"
)


@app.route("/")
def home():
    return jsonify({
        "project": "Carbon Compass AI",
        "subsystem": "AI Sustainability Assistant",
        "student": "Nooshin Janizadeh",
        "status": "AI Assistant API is running"
    })


@app.route("/records")
def get_records():
    try:
        records = context.get_api_records()
        return jsonify(records)

    except requests.RequestException as error:
        return jsonify({
            "error": "Data Management API is unavailable",
            "details": str(error)
        }), 503


if __name__ == "__main__":
    app.run(port=5001, debug=False)
