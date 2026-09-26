import pandas as pd
try:
    df = pd.read_excel('DATASETS/raw/SIH26006_Freight_Chartering_Dataset1.xlsx', nrows=5)
    print(df.columns.tolist())
except Exception as e:
    print('error', str(e))
