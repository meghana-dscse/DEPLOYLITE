"""Basic route tests for the DeploySphere Flask application."""

import app as deploysphere_app


def test_homepage_renders_dashboard():
    client = deploysphere_app.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"DeploySphere" in response.data
    assert b"Application status" in response.data


def test_health_endpoint_reports_healthy():
    client = deploysphere_app.app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy",
        "application": "DeploySphere",
        "version": deploysphere_app.VERSION,
    }
