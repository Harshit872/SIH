import pandas as pd
import json

xls = pd.ExcelFile('DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx')
print(xls.sheet_names)

all_cols = []
for s in xls.sheet_names:
    df = pd.read_excel('DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx', sheet_name=s, nrows=5)
    all_cols.extend(df.columns.tolist())

print("All columns found in all sheets:")
print(set(all_cols))
