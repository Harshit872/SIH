import pytest
from fastapi.testclient import TestClient
from app.main import app
app.dependency_overrides = {}

from app.main import app
app.dependency_overrides = {}

def test_signup():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "test@odyssey.app",
                "password": "securepassword",
                "first_name": "Test",
                "last_name": "User",
                "company": "Test Co"
            }
        )
        assert response.status_code in [201, 400] # 400 if already exists

def test_login():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@odyssey.app",
                "password": "securepassword"
            }
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

def test_protected_route_without_auth():
    app.dependency_overrides = {}
    with TestClient(app) as client:
        response = client.post("/api/v1/voyage/submit", json={})
        assert response.status_code == 401

def test_protected_route_with_auth():
    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@odyssey.app",
                "password": "securepassword"
            }
        )
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/v1/voyage/schedule",
            headers={"Authorization": f"Bearer {token}"},
            json={}
        )
        assert response.status_code == 422





