import os
import pandas as pd

for root, _, files in os.walk('C:/Users/umang/SIH'):
    if 'node_modules' in root or '.git' in root or 'venv' in root:
        continue
    for f in files:
        if f.endswith('.csv') or f.endswith('.xlsx') or f.endswith('.json'):
            fp = os.path.join(root, f)
            print(fp)
