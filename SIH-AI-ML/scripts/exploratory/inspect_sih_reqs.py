import pandas as pd
import sys

with open('sih_workbook_dump.txt', 'w', encoding='utf-8') as f:
    xl = pd.ExcelFile('DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx')
    for sheet in xl.sheet_names:
        f.write(f"\n--- SHEET: {sheet} ---\n")
        df = pd.read_excel(xl, sheet_name=sheet)
        f.write(df.to_string())
