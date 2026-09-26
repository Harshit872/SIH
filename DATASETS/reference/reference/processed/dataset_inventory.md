# Dataset Inventory

## Analyzed Sources
1. **Cargo handled at Major Ports (Monthly Reports - e.g., April 2026)**
   - Format: PDF
   - Relevant Content: 
     - Table 1 (Page 6): Major Port-wise Monthly Cargo handled
     - Table 2 (Page 7): Commodity-wise Cargo handled by Major Ports
2. **Indian Shipping Statistics (e.g., 2025, 2022-2023, 2024)**
   - Format: PDF
   - Relevant Content: 
     - Table 1, 2, 3 (Pages 14-15): Age composition of Indian Shipping Fleet (Total, Overseas, Coastal).
3. **Updates on Indian Port Sector (e.g., March 2023, Sep 2024)**
   - Format: PDF
   - Relevant Content:
     - Table 2 (Page 10): Traffic Handled at Major Ports (Historical trends).
     - Table 3 (Page 11): Commodity-wise Traffic Handled at Major Ports.
     - Table 5 (Page 14): Traffic Handled by Non-Major Ports by Maritime State.
     - Table 6 (Page 15): Commodity-wise Traffic Handled by Non-Major Ports.
4. **Baltic Indices Historical**
   - Format: CSV
   - Relevant Content: Time series of BDI, BCI, BPI, BSI from Jan 2026 to Sep 2026.
5. **Shipping Statistics 2018-19 Tables**
   - Format: Excel (Table-1.xlsx to Table-12.xlsx)
   - Relevant Content: Fleet registration, tonnages, built years.

## Extracted Tables
1. **`Cargo handled at Major Ports April 2026_p6_t1.csv`**
   - Source: Cargo handled at Major Ports April 2026.pdf (Page 6, Table 1)
   - Period: April 2025 vs April 2026 (Monthly & YTD)
   - Dimensions: Port (Major Ports)
   - Units: Tonnes
   - Status: Actual (A) and Provisional (P)
   - Note: Multi-level headers parsed as single string; requires cleaning before DB ingestion.
2. **`Cargo handled at Major Ports April 2026_p7_t1.csv`**
   - Source: Cargo handled at Major Ports April 2026.pdf (Page 7, Table 1)
   - Period: April 2025 vs April 2026
   - Dimensions: Principal Commodities
   - Units: Tonnes
3. **`Indian_Shipping_Statistics_2025_p14_t1.csv` / `p15_t1` / `p15_t2`**
   - Source: Indian_Shipping_Statistics_2025.pdf (Pages 14-15)
   - Period: As of 2021
   - Dimensions: Fleet age brackets (0-5, 6-10, 11-15, etc.) vs Vessel counts
   - Units: Number of Vessels
4. **`updates_on_indian_port_sector_31032023_p10_t1.csv`**
   - Source: updates_on_indian_port_sector_31032023.pdf (Page 10)
   - Period: 2017-18 to 2022-23
   - Dimensions: Major Ports
   - Units: 000' Tonnes
   - Status: Historical Actuals and Provisional (P)
5. **`updates_on_indian_port_sector_31032023_p11_t1.csv`**
   - Source: updates_on_indian_port_sector_31032023.pdf (Page 11)
   - Period: 2017-18 to 2022-23
   - Dimensions: Commodities
   - Units: 000' Tonnes

## Identified Extraction Issues
- PDF table extractions merge multi-level column headers (e.g., Year/Month and (P) or (A) suffixes). 
- Blank rows exist due to structural formatting in the original PDFs.
- Port Performance metrics (Wait times, Turnaround Time, Draft) were generally not tabularized in these top-level traffic summary tables.

## Missing Datasets
The following data domains required by The Odyssey backend are missing from the raw repository:
1. **Historical Freight Rates**: Route-specific ($/mt) or time-charter equivalent rates. (Baltic CSV contains indices, not route-specific rates).
2. **Bunker / Marine Fuel Prices**: Daily or monthly prices for VLSFO, HSFO, MGO at key bunkering hubs (e.g., Singapore, Fujairah, Colombo).
3. **Port Performance / Charges**: Vessel turnaround times (TRT), pre-berthing delays, and port tariffs (pilotage, berth hire, dues) necessary for Voyage Costing.
4. **Voyage/Fixture Records**: Actual historical bookings and charters for ML training.
