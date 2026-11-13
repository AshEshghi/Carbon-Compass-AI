from flask import Flask, jsonify
from context_provider import ContextProvider
from ai_assistant_error import AIAssistantError
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


@app.errorhandler(AIAssistantError)
def handle_ai_error(error):
    return jsonify({
        "error": str(error)
    }), 503


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    return jsonify({
        "error": "An unexpected error occurred in the AI Assistant."
    }), 500


@app.route("/records")
def get_records():
    try:
        records = context.get_api_records()
        return jsonify(records)

    except requests.RequestException as error:
        raise AIAssistantError(
            "Data Management API is unavailable"
        ) from error


if __name__ == "__main__":
    app.run(port=5001, debug=False)