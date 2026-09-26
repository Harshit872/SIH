import sys
import os
import json
sys.path.append(os.path.abspath('SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

user_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
password = "TestPassword123!"

client.post("/api/v1/auth/signup", json={
    "email": user_email,
    "password": password,
    "first_name": "Charter",
    "last_name": "Pro",
    "company": "Test Co",
    "role": "charterer"
})

login_res = client.post("/api/v1/auth/login", json={
    "email": user_email,
    "password": password
})
token = login_res.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

vd = {
    "origin_port": "Newcastle", "destination_port": "Paradip",
    "vessel_class": "Panamax", "cargo_type": "Coal",
    "quantity_mt": 75000, "route_distance_nm": 6300,
    "bunker_price_usd_per_mt": 850, "bdi_value": 1500,
    "port_turnaround_days": 4.5, "demurrage_rate": 20000,
    "laycan_start_date": "2026-10-01", "required_delivery_date": "2026-10-26"
}

wi_res = client.post("/api/v1/what-if", json=vd).json()

# 1. Approve Plan (Book Now)
print("--- APPROVE PLAN ---")
app_res = client.post("/api/v1/plan/approve", headers=headers, json={
    "user_decision": "approve",
    "voyage_details": vd,
    "what_if_response": wi_res
})
plan_id_1 = app_res.json().get("plan_id")

if plan_id_1:
    get_res = client.get(f"/api/v1/plan/{plan_id_1}", headers=headers)
    print("Get Response (Approved):", json.dumps(get_res.json(), indent=2))
else:
    print("Approve Failed:", app_res.text)

# 2. Modify Plan (Wait 7 Days)
print("\n--- MODIFY PLAN ---")
mod_res = client.post("/api/v1/plan/approve", headers=headers, json={
    "user_decision": "modify",
    "voyage_details": vd,
    "what_if_response": wi_res,
    "modified_scenario": "Wait 7 Days"
})
plan_id_2 = mod_res.json().get("plan_id")

if plan_id_2:
    get_res2 = client.get(f"/api/v1/plan/{plan_id_2}", headers=headers)
    print("Get Response (Modified):", json.dumps(get_res2.json(), indent=2))
else:
    print("Modify Failed:", mod_res.text)

