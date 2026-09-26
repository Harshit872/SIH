import sys
import os
import json
sys.path.append(os.path.abspath('SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("\n=== RISK SCORE ENGINE ===")
r_req = {
    "freight_rate_confidence_flag": "low_confidence_out_of_range",
    "deadline_buffer_days": 1,
    "port_cost_source": "estimated_fallback",
    "vessel_feasibility_mode": "deadfreight"
}
res = client.post("/api/v1/risk-score", json=r_req)
print("Request:", json.dumps(r_req))
print("Response:", json.dumps(res.json(), indent=2))

print("\n=== WHAT-IF / DECISION ENGINE ===")
# Set delivery date exactly 25 days from laycan start. 
# 6300nm at 13.5kn is ~19.4 days + 4.5 port days = ~24 days.
# Book Now (offset 0): 24 days (feasible, buffer 1)
# Wait 7 Days: 31 days (infeasible, buffer -6)
# Wait 14 Days: 38 days (infeasible, buffer -13)
w_req = {
    "origin_port": "Newcastle", "destination_port": "Paradip",
    "vessel_class": "Panamax", "cargo_type": "Coal",
    "quantity_mt": 75000, "route_distance_nm": 6300,
    "bunker_price_usd_per_mt": 850, "bdi_value": 1500,
    "port_turnaround_days": 4.5, "demurrage_rate": 20000,
    "laycan_start_date": "2026-10-01", "required_delivery_date": "2026-10-26"
}
res = client.post("/api/v1/what-if", json=w_req)
print("Request:", json.dumps(w_req))
print("Response:", json.dumps(res.json(), indent=2))
