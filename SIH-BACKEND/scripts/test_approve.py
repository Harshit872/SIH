import sys
import os
import json
sys.path.append(os.path.abspath('SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

wi_res = {
  "scenarios": [
    {
      "scenario_name": "Book Now",
      "total_cost_usd": 1328452.35,
      "risk_tier": "Low"
    },
    {
      "scenario_name": "Wait 7 Days",
      "total_cost_usd": 1300000.00,
      "risk_tier": "Medium"
    }
  ],
  "recommended_scenario": "Book Now"
}

vd = {"origin": "Newcastle"}

# 1. Approve Plan
print("--- APPROVE PLAN ---")
app_res = client.post("/api/v1/plan/approve", json={
    "user_decision": "approve",
    "voyage_details": vd,
    "what_if_response": wi_res
})
print("Approve Response:", json.dumps(app_res.json(), indent=2))
plan_id_1 = app_res.json().get("plan_id")

# 2. Get Plan
print("\n--- GET APPROVED PLAN ---")
if plan_id_1:
    get_res = client.get(f"/api/v1/plan/{plan_id_1}")
    print("Get Response:", json.dumps(get_res.json(), indent=2))

# 3. Modify Plan
print("\n--- MODIFY PLAN ---")
mod_res = client.post("/api/v1/plan/approve", json={
    "user_decision": "modify",
    "voyage_details": vd,
    "what_if_response": wi_res,
    "modified_scenario": "Wait 7 Days"
})
print("Modify Response:", json.dumps(mod_res.json(), indent=2))
plan_id_2 = mod_res.json().get("plan_id")

# 4. Get Modified Plan
print("\n--- GET MODIFIED PLAN ---")
if plan_id_2:
    get_res = client.get(f"/api/v1/plan/{plan_id_2}")
    print("Get Response:", json.dumps(get_res.json(), indent=2))

