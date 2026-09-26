import os
import pandas as pd
import numpy as np
import re
from math import radians, sin, cos, sqrt, atan2

# Port Coordinates (Lat, Lon) for Verification
PORT_COORDS = {
    'Gladstone': (-23.83, 151.25),
    'Newcastle': (-32.92, 151.78),
    'Hay Point': (-21.27, 149.30),
    'Dalrymple Bay': (-21.28, 149.30),
    'Dhamra': (20.80, 86.97),
    'Paradip': (20.26, 86.67),
    'Haldia': (22.02, 88.06),
    'Visakhapatnam': (17.68, 83.28)
}

def haversine_nm(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance_km = R * c
    return distance_km * 0.539957 # km to nm

# 1. Base table
df = pd.read_excel('DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx')
df['date'] = pd.to_datetime(df['date'])

# 2. Derive freight_rate_usd_per_mt
qty_zero_mask = (df['Quantity_MT'] == 0) | (df['Quantity_MT'].isnull())
qty_zero_count = qty_zero_mask.sum()
df['freight_rate_usd_per_mt'] = np.where(
    ~qty_zero_mask,
    df['Freight_Cost_USD'] / df['Quantity_MT'],
    np.nan
)

# 3. Join BDI
bdi_df = pd.read_csv('DATASETS/raw/baltic_indices_historical.csv')
bdi_df['date'] = pd.to_datetime(bdi_df['date'])
bdi_df = bdi_df[['date', 'bdi_value', '30_day_avg']]
bdi_df = bdi_df.rename(columns={'30_day_avg': 'bdi_30_day_avg'})

df = df.merge(bdi_df, on='date', how='left')

# 4. Route Distance
def get_distance(row):
    orig = row['Origin_Port']
    dest = row['Destination_Port']
    if pd.isna(orig) or pd.isna(dest):
        return np.nan
    if orig in PORT_COORDS and dest in PORT_COORDS:
        return haversine_nm(PORT_COORDS[orig][0], PORT_COORDS[orig][1], PORT_COORDS[dest][0], PORT_COORDS[dest][1])
    return np.nan

df['route_distance_nm'] = df.apply(get_distance, axis=1)

# 5. Clean Fuel Prices
fuel_df = pd.read_csv('DATASETS/raw/marine_fuel_prices_east_coast_india.csv')

def parse_range(val_str):
    if pd.isna(val_str):
        return np.nan
    m = re.findall(r'\d+,\d+|\d+', str(val_str))
    if len(m) == 2:
        v1 = float(m[0].replace(',', ''))
        v2 = float(m[1].replace(',', ''))
        return (v1 + v2) / 2.0
    return np.nan

for col in ['2022', '2023', '2024', '2025-2026']:
    fuel_df[f'{col}_midpoint'] = fuel_df[col].apply(parse_range)

# Extract simple port name from "Paradip (INPRT)"
fuel_df['Port_Name'] = fuel_df['Port / Location'].apply(lambda x: x.split(' (')[0] if pd.notna(x) else x)
fuel_df['Port_Name'] = fuel_df['Port_Name'].replace('Haldia / Kolkata', 'Haldia')

# Keep only VLSFO 0.5% (Assumption: typical compliant fuel for model consistency)
fuel_df_vlsfo = fuel_df[fuel_df['Fuel Grade'].str.contains('VLSFO')].copy()

# 6. Join Fuel Prices
def get_fuel_price(row):
    dest = row['Destination_Port']
    year = row['date'].year
    
    # Match port
    port_match = fuel_df_vlsfo[fuel_df_vlsfo['Port_Name'] == dest]
    if port_match.empty:
        return np.nan
    
    # Match year
    col_to_use = None
    if year <= 2022: col_to_use = '2022_midpoint'
    elif year == 2023: col_to_use = '2023_midpoint'
    elif year == 2024: col_to_use = '2024_midpoint'
    elif year >= 2025: col_to_use = '2025-2026_midpoint'
    
    if col_to_use:
        return port_match.iloc[0][col_to_use]
    return np.nan

df['fuel_price_midpoint_usd_per_mt'] = df.apply(get_fuel_price, axis=1)

# 7. Output CSV
out_cols = [
    'date', 'Origin_Port', 'Destination_Port', 'Vessel_Type', 'Cargo_Type',
    'Quantity_MT', 'freight_rate_usd_per_mt', 'Bunker_Cost_USD',
    'Demurrage_USD_Day', 'bdi_value', 'bdi_30_day_avg', 'route_distance_nm',
    'fuel_price_midpoint_usd_per_mt', 'Selected_Option'
]
df_final = df[out_cols].copy()
df_final = df_final.rename(columns={'Origin_Port': 'origin_port', 'Destination_Port': 'destination_port',
                                    'Vessel_Type': 'vessel_type', 'Cargo_Type': 'cargo_type',
                                    'Quantity_MT': 'quantity_mt', 'Bunker_Cost_USD': 'bunker_cost_usd',
                                    'Demurrage_USD_Day': 'demurrage_usd_day', 'Selected_Option': 'selected_option'})

os.makedirs('DATASETS/processed', exist_ok=True)
csv_path = 'DATASETS/processed/training_table_freight_v1.csv'
df_final.to_csv(csv_path, index=False)

# Collect report metrics
report = {
    'total_rows': len(df_final),
    'total_cols': len(df_final.columns),
    'nulls': df_final.isnull().sum().to_dict(),
    'qty_zero_count': qty_zero_count,
    'bdi_missing': df_final['bdi_value'].isnull().sum(),
}
import json
with open('DATASETS/processed/report.json', 'w') as f:
    json.dump(report, f)

