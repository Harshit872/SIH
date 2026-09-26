import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Reference values
VESSELS = {
    'Handysize': {'dwt': (10000, 39999), 'speed': 13.5, 'consumption': 21, 'hire_range': (8000, 14000)},
    'Handymax / Supramax': {'dwt': (40000, 59999), 'speed': 13.5, 'consumption': 26, 'hire_range': (10000, 16000)},
    'Panamax': {'dwt': (60000, 99999), 'speed': 13.5, 'consumption': 30, 'hire_range': (12000, 20000)},
    'Capesize': {'dwt': (100000, 180000), 'speed': 14.5, 'consumption': 45, 'hire_range': (15000, 30000)}
}

ROUTES = [
    {'origin': 'Port Hedland, Australia', 'destination': 'Visakhapatnam, India', 'distance': 5300, 'cargo': 'Iron Ore'},
    {'origin': 'Gladstone, Australia', 'destination': 'Paradip, India', 'distance': 6300, 'cargo': 'Coal'},
    {'origin': 'Richards Bay, South Africa', 'destination': 'Visakhapatnam, India', 'distance': 4600, 'cargo': 'Coal'}
]

np.random.seed(42)
random.seed(42)

start_date = datetime(2025, 1, 1)
n_rows = 500

data = []
for _ in range(n_rows):
    date = start_date + timedelta(days=random.randint(0, 600))
    route = random.choice(ROUTES)
    vessel_class = random.choice(list(VESSELS.keys()))
    
    # Vessel specs
    v_spec = VESSELS[vessel_class]
    quantity_mt = random.randint(v_spec['dwt'][0], int(v_spec['dwt'][1]*0.95))
    
    # Bunker Price
    bunker_price_usd_per_mt = random.uniform(700, 1000)
    
    # BDI Synthetic
    bdi_value_synthetic = random.randint(500, 3000)
    
    # Hire Rate interpolation based on BDI
    bdi_ratio = (bdi_value_synthetic - 500) / 2500.0 # BDI range 500 to 3000
    hire_min, hire_max = v_spec['hire_range']
    daily_hire_rate = hire_min + (bdi_ratio * (hire_max - hire_min))
    
    # Cost Calculations
    sea_days = route['distance'] / (v_spec['speed'] * 24)
    hire_cost_usd = sea_days * daily_hire_rate
    bunker_cost_usd = sea_days * v_spec['consumption'] * bunker_price_usd_per_mt
    
    # Port Cost (derived from turnaround time 48 - 93 hrs * /hr + base )
    turnaround_hrs = random.uniform(48, 94)
    port_cost_usd = 30000 + (turnaround_hrs * 500)
    
    # Demurrage (cap 20k per SAIL reference)
    demurrage_days = random.uniform(0, 5)
    demurrage_rate = random.uniform(5000, 20000)
    demurrage_usd = demurrage_days * demurrage_rate if random.random() > 0.5 else 0
    
    # Freight Cost (Capital Hire + Bunker + Port + Demurrage)
    freight_cost_usd = hire_cost_usd + bunker_cost_usd + port_cost_usd + demurrage_usd
    freight_rate_usd_per_mt = freight_cost_usd / quantity_mt
    
    data.append({
        'date': date.strftime('%Y-%m-%d'),
        'origin_port': route['origin'],
        'destination_port': route['destination'],
        'vessel_class': vessel_class,
        'cargo_type': route['cargo'],
        'quantity_mt': quantity_mt,
        'route_distance_nm': route['distance'],
        'bunker_price_usd_per_mt': round(bunker_price_usd_per_mt, 2),
        'bunker_cost_usd': round(bunker_cost_usd, 2),
        'hire_cost_usd': round(hire_cost_usd, 2),
        'port_cost_usd': round(port_cost_usd, 2),
        'demurrage_usd': round(demurrage_usd, 2),
        'freight_cost_usd': round(freight_cost_usd, 2),
        'freight_rate_usd_per_mt': round(freight_rate_usd_per_mt, 2),
        'bdi_value_synthetic': bdi_value_synthetic,
        'is_synthetic': True
    })

df = pd.DataFrame(data)
df = df.sort_values('date')

os.makedirs('DATASETS/processed', exist_ok=True)
df.to_csv('DATASETS/processed/synthetic_voyages_v1.csv', index=False)

# README
readme = f"""# Data Dictionary: synthetic_voyages_v1.csv

**WARNING: All data in this file is SYNTHETIC (is_synthetic=True for all rows).**
This dataset was generated for training purposes using base assumptions grounded in the actual reference files provided in SIH26006_Freight_Chartering_Dataset.xlsx.

## References Used
1. **Vessel Specs** (5_Vessel_Class_Reference): 
   - Handysize (10-40k DWT, 13.5kn, 21 t/day, Hire: -14k/day)
   - Handymax / Supramax (40-60k DWT, 13.5kn, 26 t/day, Hire: -16k/day)
   - Panamax (60-100k DWT, 13.5kn, 30 t/day, Hire: -20k/day)
   - Capesize (100-180k DWT, 14.5kn, 45 t/day, Hire: -30k/day)
   *Hire rates are typical public ranges scaling linearly with the Baltic Dry Index.*
2. **Route Distances** (6_Route_Distances_Reference):
   - Port Hedland, Australia to Visakhapatnam, India: 5300 nm (Iron Ore)
   - Gladstone, Australia to Paradip, India: 6300 nm (Coal)
   - Richards Bay, South Africa to Visakhapatnam, India: 4600 nm (Coal)
3. **Bunker Prices**: Sampled randomly between  and ,000 USD/mt.
4. **Demurrage Cap**: USD 20,000/day max (derived from 3_SAIL_Coal_Demurrage_CAG).
5. **Port Turnaround**: Used 48 to 94 hours (derived from 2_Port_TRT_Performance).
6. **BDI Proxy**: Synthetically generated random uniform values between 500 and 3000 Index points.

## Formula Logic
- **voyage_days**: oute_distance_nm / (speed_knots * 24)
- **daily_hire_rate**: Linearly interpolated between the vessel's min and max hire range, mapped to the synthetic BDI value (500 to 3000).
- **hire_cost_usd**: daily_hire_rate * voyage_days
- **bunker_cost_usd**: oyage_days * daily_consumption * bunker_price_usd_per_mt
- **port_cost_usd**: $30,000 base + (Turnaround_Hours * /hr)
- **demurrage_usd**: Random 0 to 5 days * random rate up to $20,000/day. (50% chance of 0 demurrage).
- **freight_cost_usd**: hire_cost_usd + bunker_cost_usd + port_cost_usd + demurrage_usd
- **freight_rate_usd_per_mt**: reight_cost_usd / quantity_mt
"""
with open('DATASETS/processed/synthetic_voyages_v1_README.md', 'w') as f:
    f.write(readme)

# Print Report
print(f"Row count: {len(df)}")
print(f"Min rate: {df['freight_rate_usd_per_mt'].min()}")
print(f"Max rate: {df['freight_rate_usd_per_mt'].max()}")
print(f"Mean rate: {df['freight_rate_usd_per_mt'].mean()}")
print("First 10 rows:")
print(df.head(10).to_csv(index=False))
