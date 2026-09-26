# Cleaning Log

## 1. `updates_20on_20indian_20port_20sector_2031032023_p10_t1.csv` -> `major_ports_traffic_cleaned.csv`
- **Issue**: Source PDF table merged title into headers. The actual column labels were pushed to row 2, with blank artifact columns inserted by PDF string-parsing.
- **Transformations Applied**:
  - Excluded rows 0-2 (Title row, Unit row, Header row, Index column row).
  - Renamed columns to semantic names: `Port`, `2017_18`, `2018_19`, `2019_20`, `2020_21`, `2021_22`, `2022_23_P`, `Change_Pct`.
  - Dropped artifact columns `Unnamed: 1`, `Unnamed: 2`.
  - Dropped structural blank rows (e.g., between groups) where `Port` is NaN.
  - Removed newline `\n` characters embedded in port names during extraction.
- **Result**: Clean, unambiguous 13-row timeseries dataset of Major Port traffic.

## 2. Mock Excel (`complete_shipping_decision_dataset.xlsx`)
- **Issue**: Detected as containing dummy rows (`Illustrative scenario`) and schemas (`Model feature`).
- **Transformations**: Excluded entirely from `processed/` normalization pipeline to prevent synthetic contamination of actual forecasting datasets.

## 3. Baltic Indices (`baltic_indices_historical.csv`)
- **Issue**: Sparse dataset representing 11 isolated dates in 2026.
- **Transformations**: None applied. Logged as insufficient for time-series forecasting.
