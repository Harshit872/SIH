import pandas as pd
xls = pd.ExcelFile('DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx')
print(xls.sheet_names)
