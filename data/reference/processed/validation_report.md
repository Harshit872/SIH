# Data Validation and Normalization Report

## 1. Extracted CSV Validation
Extracted tables in `data/reference/processed/*.csv` were cross-referenced against the raw PDF structure.
- **Row Counts / Totals**: Raw PDF row spacing introduced `NaN` filler rows in the CSVs. Where extracted cleanly (e.g. `major_ports_traffic_cleaned.csv`), row counts now accurately match the 12 Major Ports + Total rows.
- **Headers & Units**: PDFs nested units like "(000' Tonnes)" under the main title. This disrupted automatic header mapping. Cleaned tables push units to the data dictionary and standardize column headers.
- **Values**: Representative values (e.g., Paradip's 16.5% YOY growth) verified accurately extracted from the source matrix.

## 2. Baltic Indices Historical Analysis
- **Source**: `baltic_indices_historical.csv`
- **Columns**: `Date`, `BDI`, `BCI` (Capesize), `BPI` (Panamax), `BSI` (Supramax), `BHSI` (Handysize)
- **Date Range**: 2026-01-02 to 2026-09-02
- **Missing Periods**: Extremely sparse. Only 11 observations total over a 9-month period. `BHSI` is 100% null. `BPI` and `BSI` are partially null. 
- **Relevance**: BDI, BCI, BPI, BSI are highly relevant leading indicators for global bulk freight. However, index values are unitless benchmarks, **not actual fixture rates (USD/mt)**. 

## 3. Fuel-Price Tables
- **Review Result**: **None found.** 
- None of the provided Government PDFs, Excel statistical files, or CSVs contained any tables on VLSFO, HSFO, or MGO bunker prices. 

## 4. Dataset Classification
- **Usable as-is**: `baltic_indices_historical.csv` (requires imputation if used, but structurally sound).
- **Usable after cleaning**: All PDF-extracted CSVs (`Cargo handled at Major Ports...`, `Indian Shipping Statistics...`). Requires removing merged headers and `NaN` spacing (demonstrated via `major_ports_traffic_cleaned.csv`).
- **Contextual only**: `Shipping_Statistics_2018_19` (Historical context only, outdated fleet details).
- **Unsuitable**: `complete_shipping_decision_dataset.xlsx`. Contains schema templates and single "Illustrative scenario" rows. Excluded to prevent synthetic data contamination.

## 5. Outstanding Missing Datasets
To operate The Odyssey's engines, the following real operational datasets remain entirely absent:
1. **Cost Estimation / Scenario**: Bunker Prices (VLSFO/HSFO) at major hubs, Port Disbursements, Daily Demurrage rates.
2. **Forecasting**: Route-Specific Historical Freight Rates ($/mt) (the Baltic index is a benchmark, not a payable rate).
3. **Port Delay / Vessel Feasibility**: Turnaround Time (TRT), pre-berthing wait times, verified Draft/LOA/Beam constraints per berth.
4. **Machine Learning / Validation**: Historical Voyage/Fixture records (actual booked shipments).
