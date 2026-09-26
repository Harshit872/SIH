import pandas as pd
import os
import glob
from pathlib import Path

raw_dir = Path("C:/Users/umang/SIH/DATASETS/raw")

print("--- baltic_indices_historical.csv ---")
df_baltic = pd.read_csv(raw_dir / "baltic_indices_historical.csv")
print(df_baltic.head())
print("Columns:", df_baltic.columns)
print("Range:", df_baltic['Date'].min(), "to", df_baltic['Date'].max())

print("\n--- complete_shipping_decision_dataset.xlsx ---")
df_decision = pd.read_excel(raw_dir / "complete_shipping_decision_dataset.xlsx", sheet_name=None)
for sheet_name, df in df_decision.items():
    print(f"Sheet: {sheet_name}")
    print(df.head(2))
    print("Columns:", df.columns)

print("\n--- 2018-19 Tables ---")
tables_dir = raw_dir / "20210818130617Shipping_Statistics_2018_19" / "2018-19"
for file in glob.glob(str(tables_dir / "Table-*.xlsx")):
    print(f"\n{os.path.basename(file)}:")
    try:
        df_t = pd.read_excel(file, header=None)
        print(df_t.head(5))
    except Exception as e:
        print("Error:", e)
