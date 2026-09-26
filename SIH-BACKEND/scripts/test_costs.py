import sys
import os
import json
sys.path.append(os.path.abspath('SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("\n=== VOYAGE COST TESTS ===")
# 1. Paradip (real_reference)
c_req1 = {
    "origin_port": "Newcastle", "destination_port": "Paradip",
    "freight_rate_usd_per_mt": 15.5, "quantity_mt": 75000, "bunker_price_usd_per_mt": 850,
    "route_distance_nm": 6300, "vessel_class": "Panamax", "port_turnaround_days": 4.5, "demurrage_rate": 20000
}
res = client.post("/api/v1/voyage-cost", json=c_req1)
print(f"Request (Paradip):", json.dumps(c_req1))
print(f"Response:", json.dumps(res.json(), indent=2))

# 2. Visakhapatnam (estimated_fallback)
c_req2 = {
    "origin_port": "Port Hedland", "destination_port": "Visakhapatnam",
    "freight_rate_usd_per_mt": 15.5, "quantity_mt": 75000, "bunker_price_usd_per_mt": 850,
    "route_distance_nm": 6300, "vessel_class": "Panamax", "port_turnaround_days": 4.5, "demurrage_rate": 20000
}
res = client.post("/api/v1/voyage-cost", json=c_req2)
print(f"\nRequest (Visakhapatnam):", json.dumps(c_req2))
print(f"Response:", json.dumps(res.json(), indent=2))

# 3. Different route/combo
c_req3 = {
    "origin_port": "Richards Bay", "destination_port": "Haldia",
    "freight_rate_usd_per_mt": 25.5, "quantity_mt": 35000, "bunker_price_usd_per_mt": 900,
    "route_distance_nm": 4600, "vessel_class": "Handysize", "port_turnaround_days": 6.0, "demurrage_rate": 15000
}
res = client.post("/api/v1/voyage-cost", json=c_req3)
print(f"\nRequest (Handysize):", json.dumps(c_req3))
print(f"Response:", json.dumps(res.json(), indent=2))

print("\n=== VESSEL FEASIBILITY TESTS ===")
# Borderline (59,000 MT is right near the max of Supramax which is 59999, but > 95% of max might reject it)
v_req1 = {"cargo_quantity_mt": 58000, "origin_port": "Gladstone", "destination_port": "Paradip"}
res = client.post("/api/v1/vessel-feasibility", json=v_req1)
print(f"Request (Borderline 58k MT):", json.dumps(v_req1))
print(f"Response:", json.dumps(res.json(), indent=2))

