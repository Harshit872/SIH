import sys
import os
sys.path.append(os.path.abspath('SIH-BACKEND'))
from app.data_acquisition.dataset_loader import _dataset
ds = _dataset()
for k in ds.keys():
    print(f"Key: {k}, Rows: {len(ds[k])}")
    if len(ds[k]) > 0:
        print("  Sample keys:", list(ds[k][0].keys()))
