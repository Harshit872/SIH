import pandas as pd
import json

files = {
    'marine_fuel_prices': 'DATASETS/raw/marine_fuel_prices_east_coast_india.csv',
    'port_performance': 'DATASETS/raw/Maritime Port Performance Project Dataset.csv',
    'port_costs': 'DATASETS/raw/port_cost_specifications.csv',
    'freight_chartering': 'DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx'
}

for name, path in files.items():
    print(f"\n--- {name.upper()} ---")
    try:
        if path.endswith('.csv'):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("Sample data:")
        print(df.head(2).to_string())
    except Exception as e:
        print(f"Error reading {path}: {e}")
