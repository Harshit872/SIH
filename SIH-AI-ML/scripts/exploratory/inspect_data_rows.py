import sys
import os
sys.path.append(os.path.abspath('SIH-BACKEND'))
from app.data_acquisition.dataset_loader import _dataset
ds = _dataset()
print("ROUTE BENCHMARKS:")
for row in ds['06_Route_Benchmarks']: print(row)
print("\nBUNKER PRICES:")
for row in ds['07_Bunker_Prices']: print(row)
print("\nMODEL ASSUMPTIONS:")
for row in ds['08_Model_Assumptions']: print(row)
