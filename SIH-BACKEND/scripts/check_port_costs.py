import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')
df = pd.read_csv('DATASETS/raw/port_cost_specifications.csv')
print(df.to_string())
