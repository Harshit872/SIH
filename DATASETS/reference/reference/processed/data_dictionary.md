# Data Dictionary

This document maps the extracted fields from the raw PDFs to the semantic meanings required by The Odyssey dataset requirements.

## 1. Port Traffic Tables (Major & Non-Major)
*Sources: `Cargo handled at Major Ports...`, `updates_on_indian_port_sector...`*

| Field Name in Extraction | Interpreted Meaning | Units | Remarks |
| :--- | :--- | :--- | :--- |
| **Port / Name of Ports** | Port Identifier (Origin/Destination) | String | Major Indian Ports (e.g., Paradip, Kandla). |
| **Maritime State/UT** | Regional grouping for Non-Major ports | String | e.g., Gujarat, Odisha. |
| **[Date] (e.g., April 2026)** | Cargo handled during specific month | Tonnes | Actual (A) or Provisional (P). |
| **[Year] (e.g., 2021-22)** | Annual cargo handled | 000' Tonnes | Usually financial year (April - March). |
| **Percentage Change...** | Year-over-Year Growth | Percentage | Comparative growth indicator. |

## 2. Commodity Traffic Tables
*Sources: `Cargo handled at Major Ports...`, `updates_on_indian_port_sector...`*

| Field Name in Extraction | Interpreted Meaning | Units | Remarks |
| :--- | :--- | :--- | :--- |
| **Principal Commodities** | Commodity Type | String | e.g., Thermal Coal, Iron Ore, POL. |
| **[Date / Year]** | Cargo volume handled in period | Tonnes or 000' Tonnes | Dependent on the report. |

## 3. Fleet Age Composition
*Source: `Indian_Shipping_Statistics_2025`*

| Field Name in Extraction | Interpreted Meaning | Units | Remarks |
| :--- | :--- | :--- | :--- |
| **0-5 years**, **6-10 years**, etc. | Age Bracket | Count | Number of vessels in this age group. |
| **Total** | Total Fleet Size | Count | Aggregation of vessels. |

## 4. Baltic Indices (CSV)
*Source: `baltic_indices_historical.csv`*

| Field Name | Interpreted Meaning | Units | Remarks |
| :--- | :--- | :--- | :--- |
| **Date** | Date of Index publication | YYYY-MM-DD | Range: Jan 2026 - Sep 2026 |
| **BDI** | Baltic Dry Index | Index Points | Global benchmark for dry bulk freight. |
| **BCI** | Baltic Capesize Index | Index Points | Capesize specific index. |
| **BPI** | Baltic Panamax Index | Index Points | Panamax specific index. |
| **BSI** | Baltic Supramax Index | Index Points | Supramax specific index. |
| **BHSI** | Baltic Handysize Index | Index Points | Handysize specific index. |

---

## 🛑 Required but Missing Fields
To operate The Odyssey's engines, the following fields must be supplied in future datasets:

### Voyage Costing
- **Bunker Price (VLSFO/HSFO)** [USD/mt]
- **Port Tariffs (Pilotage, Berth Hire, Port Dues)** [USD or INR]
- **Port Disbursement Account (PDA) Estimates** [USD]
- **Demurrage Rate** [USD/day]

### Fleet & Port Feasibility
- **Draft limits, LOA limits, Beam limits** per Berth [meters]
- **Vessel characteristics (DWT, Draft, Speed, Consumption)** [mt, m, knots, mt/day]

### Forecasting & Risk
- **Route-specific Freight Rates** [USD/mt]
- **Turnaround Time (TRT)** [days/hours]
- **Pre-berthing Wait Times** [days/hours]
