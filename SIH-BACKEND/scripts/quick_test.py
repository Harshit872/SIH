import sys
import os
import json
sys.path.append(os.path.abspath('SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Journey 1
req1 = {
    "origin_port": "Newcastle", "destination_port": "Paradip", "vessel_class": "Panamax", "cargo_type": "Coal",
    "quantity_mt": 75000, "route_distance_nm": 6300, "bunker_price_usd_per_mt": 850, "bdi_value": 1500,
    "port_turnaround_days": 4.5, "demurrage_rate": 20000, "laycan_start_date": "2026-10-01", "required_delivery_date": "2026-10-25"
}

# Journey 2
req2 = {
    "origin_port": "Richards Bay", "destination_port": "Haldia", "vessel_class": "Handysize", "cargo_type": "Coal",
    "quantity_mt": 35000, "route_distance_nm": 4600, "bunker_price_usd_per_mt": 900, "bdi_value": 1500,
    "port_turnaround_days": 6.0, "demurrage_rate": 15000, "laycan_start_date": "2026-10-01", "required_delivery_date": "2026-10-25"
}

def print_results(req, name):
    fr = client.post("/api/v1/forecast/freight-rate", json=req).json()
    req["freight_rate_usd_per_mt"] = fr["predicted_freight_rate_usd_per_mt"]
    vc = client.post("/api/v1/voyage-cost", json=req).json()
    req["vessel_speed_knots"] = 13.5
    dl = client.post("/api/v1/deadline-check", json=req).json()
    rs = client.post("/api/v1/risk-score", json={
        "freight_rate_confidence_flag": fr["confidence_flag"],
        "deadline_buffer_days": dl["buffer_days"],
        "port_cost_source": vc["port_cost_source"],
        "vessel_feasibility_mode": "direct_feasible"
    }).json()
    print(f"--- {name} ---")
    print(f"Rate: /MT")
    print(f"Cost: ")
    print(f"Risk Tier: {rs['risk_tier']}")

print_results(req1, "Journey 1 (75k MT to Paradip)")
print_results(req2, "Journey 2 (35k MT to Haldia)")
