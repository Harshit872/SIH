import os
import pandas as pd
import json

# 1. Excel Dump
print("1. SIH26006_Freight_Chartering_Dataset.xlsx")
xls = pd.ExcelFile('DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx')
for sheet in xls.sheet_names:
    df = pd.read_excel('DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx', sheet_name=sheet)
    df = df.dropna(how='all')
    print(f"Sheet: {sheet}")
    print(f"Columns: {df.columns.tolist()}")
    print("First 3 rows:")
    print(df.head(3).to_string(index=False))
    print("---")
