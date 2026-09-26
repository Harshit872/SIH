import pandas as pd
df = pd.read_excel('DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx', header=None, nrows=10)
print(df.to_string())
