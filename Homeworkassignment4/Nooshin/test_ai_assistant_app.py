
import pytest
import requests
from unittest.mock import patch

from ai_assistant_app import app, context
from ai_assistant_error import AIAssistantError


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# 1. Home page status
def test_home_status_code(client):
    response = client.get("/")
    assert response.status_code == 200


# 2. Project name
def test_project_name(client):
    response = client.get("/")
    assert response.json["project"] == "Carbon Compass AI"


# 3. Subsystem name
def test_subsystem_name(client):
    response = client.get("/")
    assert response.json["subsystem"] == "AI Sustainability Assistant"


# 4. Student name
def test_student_name(client):
    response = client.get("/")
    assert response.json["student"] == "Nooshin Janizadeh"


# 5. API status
def test_api_status(client):
    response = client.get("/")
    assert response.json["status"] == "AI Assistant API is running"


# 6. Records endpoint status
@patch.object(context, "get_api_records", return_value=[])
def test_records_status(mock_api, client):
    response = client.get("/records")
    assert response.status_code == 200


# 7. JSON response
@patch.object(context, "get_api_records", return_value=[])
def test_records_json(mock_api, client):
    response = client.get("/records")
    assert response.is_json


# 8. Empty records
@patch.object(context, "get_api_records", return_value=[])
def test_empty_records(mock_api, client):
    response = client.get("/records")
    assert response.json == []


# 9. First record
@patch.object(
    context,
    "get_api_records",
    return_value=[{"timestamp": "2026-01-01", "electricity_kwh": 120.0}]
)
def test_first_record(mock_api, client):
    response = client.get("/records")
    assert response.json[0]["electricity_kwh"] == 120.0


# 10. Second record
@patch.object(
    context,
    "get_api_records",
    return_value=[{"timestamp": "2026-01-02", "electricity_kwh": 150.0}]
)
def test_second_record(mock_api, client):
    response = client.get("/records")
    assert response.json[0]["electricity_kwh"] == 150.0


# 11. Connection error
@patch.object(
    context,
    "get_api_records",
    side_effect=requests.ConnectionError("Connection failed")
)
def test_connection_error(mock_api, client):
    response = client.get("/records")
    assert response.status_code == 503
    assert response.json["error"] == "Data Management API is unavailable"


# 12. Timeout error
@patch.object(
    context,
    "get_api_records",
    side_effect=requests.Timeout("Request timed out")
)
def test_timeout_error(mock_api, client):
    response = client.get("/records")
    assert response.status_code == 503


# 13. HTTP error
@patch.object(
    context,
    "get_api_records",
    side_effect=requests.HTTPError("Server error")
)
def test_http_error(mock_api, client):
    response = client.get("/records")
    assert response.status_code == 503


# 14. Custom error handler
def test_custom_error_handler(client):
    with patch.object(
        context,
        "get_api_records",
        side_effect=AIAssistantError("Test error")
    ):
        response = client.get("/records")

    assert response.status_code == 503
    assert response.json["error"] == "Test error"


# 15. Unexpected error
@patch.object(
    context,
    "get_api_records",
    side_effect=RuntimeError("Unexpected error")
)
def test_unexpected_error(mock_api, client):
    response = client.get("/records")
    assert response.status_code == 500
