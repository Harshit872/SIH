import sys
import os
sys.path.append(os.path.abspath('SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

print("--- SIGNUP ---")
user_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
password = "TestPassword123!"

signup_res = client.post("/api/v1/auth/signup", json={
    "email": user_email,
    "password": password,
    "first_name": "John",
    "last_name": "Doe",
    "company": "Test Co",
    "role": "charterer"
})
print("Signup Status:", signup_res.status_code)

print("\n--- LOGIN ---")
login_res = client.post("/api/v1/auth/login", json={
    "email": user_email,
    "password": password
})
print("Login Status:", login_res.status_code)
if login_res.status_code == 200:
    token = login_res.json().get("access_token")
    print("Token received:", bool(token))
else:
    token = None
    
print("\n--- PROTECTED ROUTE ---")
if token:
    headers = {"Authorization": f"Bearer {token}"}
    prot_res = client.post("/api/v1/voyage/submit", headers=headers, json={
        "origin": "Newcastle", "destination": "Paradip", "commodity": "Coal",
        "cargoMt": 75000, "deliveryDate": "2026-10-25", "contract": "Voyage Charter",
        "laycan": "01 Oct 2026 - 05 Oct 2026", "noOfVoyages": 2
    })
    print("Protected Status:", prot_res.status_code)
    print("Protected Response:", prot_res.text[:100])
