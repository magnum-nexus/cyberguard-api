import pytest
from app import create_app, db
from app.config import Config
from app.models.cyber_models import User, Asset

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    API_KEY = "test-api-key"

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Buat 1 user & 1 asset awal untuk relasi pengujian
            user = User(username="tester", email="tester@local.test", role="analyst")
            db.session.add(user)
            db.session.commit()

            asset = Asset(
                owner_id=user.id,
                asset_name="Test Server",
                asset_type="Web Server",
                ip_address="10.0.0.1",
                criticality="High"
            )
            db.session.add(asset)
            db.session.commit()
        yield client

def test_health_check(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_create_incident_success(client):
    headers = {"X-API-Key": "test-api-key"}
    payload = {
        "asset_id": 1,
        "reporter_id": 1,
        "title": "Percobaan SQL Injection pada Form Pencarian",
        "incident_type": "SQL Injection",
        "severity": "Critical",
        "description": "Payload UNION SELECT terdeteksi oleh WAF."
    }
    res = client.post("/api/v1/incidents", json=payload, headers=headers)
    data = res.get_json()
    assert res.status_code == 201
    assert data["status"] == "success"
    assert data["data"]["title"] == payload["title"]

def test_create_incident_validation_error(client):
    headers = {"X-API-Key": "test-api-key"}
    # Sengaja mengosongkan field wajib dan mengisi severity tidak valid
    payload = {
        "asset_id": 1,
        "reporter_id": 1,
        "severity": "SuperUrgent"
    }
    res = client.post("/api/v1/incidents", json=payload, headers=headers)
    data = res.get_json()
    assert res.status_code == 400
    assert data["status"] == "error"
    assert "title" in data["errors"]
    assert "severity" in data["errors"]

def test_create_asset_unauthorized_without_api_key(client):
    payload = {
        "owner_id": 1,
        "asset_name": "Unauthorized Server",
        "asset_type": "API",
        "ip_address": "10.0.0.99"
    }
    res = client.post("/api/v1/assets", json=payload)
    assert res.status_code == 401
    assert res.get_json()["status"] == "error"

def test_get_nonexistent_incident(client):
    res = client.get("/api/v1/incidents/999")
    assert res.status_code == 404
    assert res.get_json()["status"] == "error"