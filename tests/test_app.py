"""Basic route tests for the DeployLite Flask application."""

import app as deploylite_app


def test_homepage_renders_dashboard():
    client = deploylite_app.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"DeployLite" in response.data
    assert b"Application status" in response.data


def test_health_endpoint_reports_healthy():
    client = deploylite_app.app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy",
        "application": "DeployLite",
        "version": deploylite_app.VERSION,
    }
