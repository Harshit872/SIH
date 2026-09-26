import pandas as pd
df = pd.read_excel('DATASETS/raw/complete_shipping_decision_dataset.xlsx', sheet_name='11_Decision_Input')
print(df.head(3).to_string())
print(len(df))
