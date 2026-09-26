import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

# Read port costs
print("\n--- PORT COSTS ---")
try:
    df = pd.read_csv('DATASETS/raw/port_cost_specifications.csv', encoding='utf-8')
    print(df.head(10).to_string())
except Exception as e:
    print(e)

# Read Excel sheets
print("\n--- FREIGHT CHARTERING EXCEL SHEETS ---")
try:
    xl = pd.ExcelFile('DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx')
    print("Sheets:", xl.sheet_names)
    for sheet in xl.sheet_names:
        print(f"\nSheet: {sheet}")
        df = pd.read_excel('DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx', sheet_name=sheet)
        print(f"Shape: {df.shape}")
        print(df.head(5).to_string())
except Exception as e:
    print(e)
