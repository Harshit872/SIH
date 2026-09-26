# Data Dictionary: training_table_freight_v1.csv

## Source Files
1. DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx
2. DATASETS/raw/baltic_indices_historical.csv
3. DATASETS/raw/marine_fuel_prices_east_coast_india.csv
4. DATASETS/raw/ship_and_bunker_multiport_fuel_prices_2026-09-11_to_2026-09-25.csv

## Column Derivation & Assumptions

- **date**: Missing. The base file SIH26006_Freight_Chartering_Dataset.xlsx is a reference workbook and contains no transactional voyage dates.
- **origin_port**: Missing in base file.
- **destination_port**: Missing in base file.
- **vessel_type**: Missing in base file.
- **cargo_type**: Missing in base file.
- **quantity_mt**: Missing in base file. (Cannot derive 0 counts since column does not exist).
- **freight_rate_usd_per_mt**: Could not derive because Freight_Cost_USD and Quantity_MT do not exist in the base file.
- **bunker_cost_usd**: Missing in base file.
- **demurrage_usd_day**: Missing in base file.
- **bdi_value**: Could not join because base file lacks a date column.
- **bdi_30_day_avg**: Could not join.
- **route_distance_nm**: Could not be calculated via Haversine because origin/destination rows are missing in the base file.
- **fuel_price_midpoint_usd_per_mt**: Could not be joined because base file lacks date (year) and Destination_Port.
- **selected_option**: Missing in base file.

## Haversine Coordinates Provided
If rows had existed, the following verified coordinates would have been used for the calculation:
- Gladstone: -23.83, 151.25
- Newcastle: -32.92, 151.78
- Hay Point: -21.27, 149.30
- Dalrymple Bay: -21.28, 149.30
- Dhamra: 20.80, 86.97
- Paradip: 20.26, 86.67
- Haldia: 22.02, 88.06
- Visakhapatnam: 17.68, 83.28

## Fuel Price Midpoint Logic
If rows had existed, string ranges like " - ,020" would be stripped of $ and ,, split by -, and averaged. Year matching would use the exact date.year to match the columns 2022, 2023, 2024, and 2025-2026.

**CRITICAL FLAG:** The resulting CSV contains 0 rows because the requested base table SIH26006_Freight_Chartering_Dataset.xlsx is a multi-sheet reference workbook that does **not** contain transactional data (date, Quantity_MT, Freight_Cost_USD, etc.). No synthetic data was generated to force the join.
