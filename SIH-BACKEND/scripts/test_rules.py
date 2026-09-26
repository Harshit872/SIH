import sys
import os
import json
sys.path.append(os.path.abspath('SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("=== 1. Vessel Feasibility ===")
v_req1 = {"cargo_quantity_mt": 75000, "origin_port": "Gladstone", "destination_port": "Paradip"}
v_req2 = {"cargo_quantity_mt": 150000, "origin_port": "Port Hedland", "destination_port": "Vizag"}
for i, req in enumerate([v_req1, v_req2], 1):
    res = client.post("/api/v1/vessel-feasibility", json=req)
    print(f"\nRequest {i}:", json.dumps(req))
    print(f"Response {i}:", json.dumps(res.json(), indent=2))

print("\n=== 2. Voyage Cost ===")
c_req1 = {
    "freight_rate_usd_per_mt": 15.5, "quantity_mt": 75000, "bunker_price_usd_per_mt": 850,
    "route_distance_nm": 6300, "vessel_class": "Panamax", "port_turnaround_days": 4.5, "demurrage_rate": 20000
}
c_req2 = {
    "freight_rate_usd_per_mt": 8.5, "quantity_mt": 150000, "bunker_price_usd_per_mt": 700,
    "route_distance_nm": 5300, "vessel_class": "Capesize", "port_turnaround_days": 3.0, "demurrage_rate": 20000
}
for i, req in enumerate([c_req1, c_req2], 1):
    res = client.post("/api/v1/voyage-cost", json=req)
    print(f"\nRequest {i}:", json.dumps(req))
    print(f"Response {i}:", json.dumps(res.json(), indent=2))
    
print("\n=== 3. Deadline Check ===")
d_req1 = {
    "route_distance_nm": 6300, "vessel_speed_knots": 13.5, "port_turnaround_days": 4.5,
    "laycan_start_date": "2026-10-01", "required_delivery_date": "2026-10-25"
}
d_req2 = {
    "route_distance_nm": 6300, "vessel_speed_knots": 13.5, "port_turnaround_days": 4.5,
    "laycan_start_date": "2026-10-01", "required_delivery_date": "2026-10-15"
}
for i, req in enumerate([d_req1, d_req2], 1):
    res = client.post("/api/v1/deadline-check", json=req)
    print(f"\nRequest {i}:", json.dumps(req))
    print(f"Response {i}:", json.dumps(res.json(), indent=2))
