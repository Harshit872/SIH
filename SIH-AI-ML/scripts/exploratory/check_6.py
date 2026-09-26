import pandas as pd
import json

def info(f):
    try:
        if f.endswith('.csv'): df = pd.read_csv(f)
        elif f.endswith('.xlsx'): df = pd.read_excel(f)
        elif f.endswith('.json'): 
            with open(f) as j: 
                d=json.load(j)
                df = pd.DataFrame(d.get('01_BDI', []))
        print(f"{f}: {len(df)} rows, cols: {df.columns.tolist()}")
    except Exception as e:
        print(f"Error {f}: {e}")

info('DATASETS/raw/baltic_indices_historical.csv')
info('DATASETS/raw/Maritime Port Performance Project Dataset.csv')
info('DATASETS/raw/port_cost_specifications.csv')
info('DATASETS/raw/marine_fuel_prices_east_coast_india.csv')
info('DATASETS/raw/ship_and_bunker_multiport_fuel_prices_2026-09-11_to_2026-09-25.csv')
info('SIH-FRONTEND/src/data/generated/shipping_dataset.json')
