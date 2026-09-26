import sys
import os
import json
sys.path.append(os.path.abspath('../SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

req = {
    "origin_port": "Newcastle", "destination_port": "Visakhapatnam",
    "vessel_class": "Handysize", "cargo_type": "Coal",
    "quantity_mt": 35400, "route_distance_nm": 6500,
    "bunker_price_usd_per_mt": 850, "bdi_value": 1500,
    "port_turnaround_days": 4.5, "demurrage_rate": 20000,
    "laycan_start_date": "2026-10-01", "required_delivery_date": "2026-10-25"
}

r = client.post("/api/v1/forecast/freight-rate", json=req).json()
print("Raw API Output:")
print(r['predicted_freight_rate_usd_per_mt'])

