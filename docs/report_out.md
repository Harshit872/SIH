### 1. Baltic Dry Index (BDI) historical data
- **File**: DATASETS/raw/baltic_indices_historical.csv
- **Rows**: 11
- **Columns**: Date (str), BDI (int64), BCI (int64), BPI (float64), BSI (float64), BHSI (float64)
- **Date Range**: 2026-01-02 to 2026-09-02
- **Units Detected in Headers**: None explicitly in column names
- **Obvious Issues**: Missing values in: BPI, BSI, BHSI

**First 10 rows**:
`csv
Date,BDI,BCI,BPI,BSI,BHSI
2026-01-02,1882,3108,1282.0,1076.0,
2026-04-22,2675,4356,,1484.0,
2026-04-23,2673,4315,1965.0,1522.0,
2026-05-15,3151,5316,2521.0,1565.0,
2026-06-30,3063,5082,,,
2026-07-01,2562,3692,2177.0,1673.0,
2026-07-03,2717,4100,2203.0,1673.0,
2026-08-18,2815,4452,2155.0,1631.0,
2026-08-28,3186,5336,2315.0,1647.0,
2026-09-01,3157,5221,2360.0,1650.0,
`

**Last 10 rows**:
`csv
Date,BDI,BCI,BPI,BSI,BHSI
2026-04-22,2675,4356,,1484.0,
2026-04-23,2673,4315,1965.0,1522.0,
2026-05-15,3151,5316,2521.0,1565.0,
2026-06-30,3063,5082,,,
2026-07-01,2562,3692,2177.0,1673.0,
2026-07-03,2717,4100,2203.0,1673.0,
2026-08-18,2815,4452,2155.0,1631.0,
2026-08-28,3186,5336,2315.0,1647.0,
2026-09-01,3157,5221,2360.0,1650.0,
2026-09-02,3331,5642,2429.0,1657.0,
`
\n### 2. Route / port list (origin-destination pairs, distances if present)
- **File**: SIH-FRONTEND/src/data/generated/shipping_dataset.json
- **Rows**: 7
- **Columns**: Date (int64), BDI (int64), Source (str), Status (str)
- **Date Range**: 1970-01-01 to 1970-01-01
- **Units Detected in Headers**: None explicitly in column names
- **Obvious Issues**: None obvious

**First 10 rows**:
`csv
Date,BDI,Source,Status
46254,2791,Baltic Dry Index historical series,Observed
46255,2841,Baltic Dry Index historical series,Observed
46258,2882,Baltic Dry Index historical series,Observed
46259,2926,Baltic Dry Index historical series,Observed
46260,3056,Baltic Dry Index historical series,Observed
46261,3107,Baltic Dry Index historical series,Observed
46262,3186,Baltic Dry Index historical series,Observed
`

**Last 10 rows**:
`csv
Date,BDI,Source,Status
46254,2791,Baltic Dry Index historical series,Observed
46255,2841,Baltic Dry Index historical series,Observed
46258,2882,Baltic Dry Index historical series,Observed
46259,2926,Baltic Dry Index historical series,Observed
46260,3056,Baltic Dry Index historical series,Observed
46261,3107,Baltic Dry Index historical series,Observed
46262,3186,Baltic Dry Index historical series,Observed
`
\n### 3. Vessel specifications (class, DWT, draft, LOA, beam, speed)
- **File**: DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx
- **Rows**: 34
- **Columns**: SIH 2026 — PS 26006 (Ministry of Steel) (str)
- **Date Range**: N/A
- **Units Detected in Headers**: SIH 2026 — PS 26006 (Ministry of Steel)
- **Obvious Issues**: Missing values in: SIH 2026 — PS 26006 (Ministry of Steel); 4 duplicate rows

**First 10 rows**:
`csv
SIH 2026 — PS 26006 (Ministry of Steel)
Intelligent Freight Forecasting Model for Optimized Vessel Chartering and Bulk Cargo Procurement
from Overseas to East Coast of India
""
"COMPILED SUPPORTING DATASET — extracted from public sources, 26 Sep 2026"
""
COLOR KEY (see tab colors / cell shading):
"  GREEN  = Verified real data, directly extracted from a cited public document/page (auditable, quote the source)."
"  YELLOW = Reference / standard industry table (vessel specs, distances) — widely used constants, not a live feed."
  ORANGE = Placeholder / synthetic — no public verified source exists; you must generate this via simulation and
           clearly label it as synthetic in your model documentation. Do NOT present as real without disclosure.
`

**Last 10 rows**:
`csv
SIH 2026 — PS 26006 (Ministry of Steel)
    to fill in port-by-port; a reference table (industry-standard vessel envelope) is provided as a starting point.
  - Port tariffs / demurrage scale-of-rates in ₹ or $ per day per vessel class — must be sourced per-port from each
    Major Port Authority's Scale of Rates notification (TAMP archive / port authority website).
""
HOW TO EXTEND THIS FILE:
  - Each sheet's last column is 'Source' — always cite the same way when you add rows.
"  - Re-run the same extraction method (web_fetch the cited page, pull the table) to refresh bunker prices and TRT"
    stats periodically — they change monthly/annually.
  - Sheets 6 (Vessel Specs) and 7 (Route Distances) are reference tables you can use as-is for a hackathon MVP;
"    they are standard industry figures, not scraped from a single page, so treat them as engineering assumptions."
`
\n### 4. Port data (turnaround times, costs, restrictions, depth limits) [File 1]
- **File**: DATASETS/raw/Maritime Port Performance Project Dataset.csv
- **Rows**: 803
- **Columns**: Unnamed: 0 (int64), Economy_Label (str), CommercialMarket_Label (str), Average_age_of_vessels_years_Value (int64), Average_age_of_vessels_years_MissingValue (float64), Median_time_in_port_days_Value (float64), Median_time_in_port_days_MissingValue (str), Average_size_GT_of_vessels_Value (int64), Average_size_GT_of_vessels_MissingValue (float64), Average_cargo_carrying_capacity_dwt_per_vessel_Value (float64), Average_cargo_carrying_capacity_dwt_per_vessel_MissingValue (str), Average_container_carrying_capacity_TEU_per_container_ship_Value (float64), Average_container_carrying_capacity_TEU_per_container_ship_MissingValue (str), Maximum_size_GT_of_vessels_Value (int64), Maximum_size_GT_of_vessels_MissingValue (float64), Maximum_cargo_carrying_capacity_dwt_of_vessels_Value (float64), Maximum_cargo_carrying_capacity_dwt_of_vessels_MissingValue (str), Maximum_container_carrying_capacity_TEU_of_container_ships_Value (float64), Maximum_container_carrying_capacity_TEU_of_container_ships_MissingValue (str), period (str)
- **Date Range**: 1970-01-01 to 1970-01-01
- **Units Detected in Headers**: None explicitly in column names
- **Obvious Issues**: Missing values in: Average_age_of_vessels_years_MissingValue, Median_time_in_port_days_Value, Median_time_in_port_days_MissingValue, Average_size_GT_of_vessels_MissingValue, Average_cargo_carrying_capacity_dwt_per_vessel_Value, Average_cargo_carrying_capacity_dwt_per_vessel_MissingValue, Average_container_carrying_capacity_TEU_per_container_ship_Value, Average_container_carrying_capacity_TEU_per_container_ship_MissingValue, Maximum_size_GT_of_vessels_MissingValue, Maximum_cargo_carrying_capacity_dwt_of_vessels_Value, Maximum_cargo_carrying_capacity_dwt_of_vessels_MissingValue, Maximum_container_carrying_capacity_TEU_of_container_ships_Value, Maximum_container_carrying_capacity_TEU_of_container_ships_MissingValue

**First 10 rows**:
`csv
Unnamed: 0,Economy_Label,CommercialMarket_Label,Average_age_of_vessels_years_Value,Average_age_of_vessels_years_MissingValue,Median_time_in_port_days_Value,Median_time_in_port_days_MissingValue,Average_size_GT_of_vessels_Value,Average_size_GT_of_vessels_MissingValue,Average_cargo_carrying_capacity_dwt_per_vessel_Value,Average_cargo_carrying_capacity_dwt_per_vessel_MissingValue,Average_container_carrying_capacity_TEU_per_container_ship_Value,Average_container_carrying_capacity_TEU_per_container_ship_MissingValue,Maximum_size_GT_of_vessels_Value,Maximum_size_GT_of_vessels_MissingValue,Maximum_cargo_carrying_capacity_dwt_of_vessels_Value,Maximum_cargo_carrying_capacity_dwt_of_vessels_MissingValue,Maximum_container_carrying_capacity_TEU_of_container_ships_Value,Maximum_container_carrying_capacity_TEU_of_container_ships_MissingValue,period
0,World,All ships,18,,1.07,,14285,,25725.0,,3407.0,,236583,,404389.0,,24000.0,,2022-S1
1,World,Liquid bulk carriers,15,,1.0,,16298,,28286.0,,,Not available or not separately reported,170618,,323183.0,,,Not available or not separately reported,2022-S1
2,World,Liquefied petroleum gas carriers,16,,1.03,,10726,,11986.0,,,Not available or not separately reported,60784,,64220.0,,,Not available or not separately reported,2022-S1
3,World,Liquefied natural gas carriers,12,,1.12,,96843,,75614.0,,,Not available or not separately reported,168189,,155159.0,,,Not available or not separately reported,2022-S1
4,World,Dry bulk carriers,14,,2.23,,32735,,58640.0,,,Not available or not separately reported,204014,,404389.0,,,Not available or not separately reported,2022-S1
5,World,Dry breakbulk carriers,21,,1.19,,5571,,7604.0,,,Not available or not separately reported,91784,,138743.0,,,Not available or not separately reported,2022-S1
6,World,Roll-on/ roll-off ships,17,,,Not available or not separately reported,25706,,10319.0,,,Not available or not separately reported,100430,,55828.0,,,Not available or not separately reported,2022-S1
7,World,Container ships,15,,0.84,,36855,,,Not available or not separately reported,3407.0,,236583,,,Not available or not separately reported,24000.0,,2022-S1
8,World,Passenger ships,20,,,Not available or not separately reported,8075,,,Not available or not separately reported,,Not available or not separately reported,235600,,,Not available or not separately reported,,Not available or not separately reported,2022-S1
9,Australia,All ships,17,,1.61,,32686,,82425.0,,4475.0,,152305,,297633.0,,9572.0,,2022-S1
`

**Last 10 rows**:
`csv
Unnamed: 0,Economy_Label,CommercialMarket_Label,Average_age_of_vessels_years_Value,Average_age_of_vessels_years_MissingValue,Median_time_in_port_days_Value,Median_time_in_port_days_MissingValue,Average_size_GT_of_vessels_Value,Average_size_GT_of_vessels_MissingValue,Average_cargo_carrying_capacity_dwt_per_vessel_Value,Average_cargo_carrying_capacity_dwt_per_vessel_MissingValue,Average_container_carrying_capacity_TEU_per_container_ship_Value,Average_container_carrying_capacity_TEU_per_container_ship_MissingValue,Maximum_size_GT_of_vessels_Value,Maximum_size_GT_of_vessels_MissingValue,Maximum_cargo_carrying_capacity_dwt_of_vessels_Value,Maximum_cargo_carrying_capacity_dwt_of_vessels_MissingValue,Maximum_container_carrying_capacity_TEU_of_container_ships_Value,Maximum_container_carrying_capacity_TEU_of_container_ships_MissingValue,period
793,United Kingdom,Passenger ships,20,,,Not available or not separately reported,13028,,,Not available or not separately reported,,Not available or not separately reported,185206,,,Not available or not separately reported,,Not available or not separately reported,2023-S2
794,United States of America,All ships,26,,1.51,,18889,,49634.0,,5799.0,,235600,,323183.0,,19224.0,,2023-S2
795,United States of America,Liquid bulk carriers,12,,1.73,,37271,,64920.0,,,Not available or not separately reported,170611,,323183.0,,,Not available or not separately reported,2023-S2
796,United States of America,Liquefied petroleum gas carriers,9,,1.82,,31440,,35435.0,,,Not available or not separately reported,60784,,63770.0,,,Not available or not separately reported,2023-S2
797,United States of America,Liquefied natural gas carriers,6,,1.34,,106652,,85337.0,,,Not available or not separately reported,149367,,107662.0,,,Not available or not separately reported,2023-S2
798,United States of America,Dry bulk carriers,21,,1.99,,28716,,51829.0,,,Not available or not separately reported,108901,,209854.0,,,Not available or not separately reported,2023-S2
799,United States of America,Dry breakbulk carriers,19,,1.76,,13012,,17200.0,,,Not available or not separately reported,91784,,116173.0,,,Not available or not separately reported,2023-S2
800,United States of America,Roll-on/ roll-off ships,15,,,Not available or not separately reported,59121,,21470.0,,,Not available or not separately reported,100430,,55828.0,,,Not available or not separately reported,2023-S2
801,United States of America,Container ships,15,,1.07,,64946,,,Not available or not separately reported,5799.0,,194308,,,Not available or not separately reported,19224.0,,2023-S2
802,United States of America,Passenger ships,30,,,Not available or not separately reported,9880,,,Not available or not separately reported,,Not available or not separately reported,235600,,,Not available or not separately reported,,Not available or not separately reported,2023-S2
`
\n### 4. Port data [File 2]
- **File**: DATASETS/raw/port_cost_specifications.csv
- **Rows**: 12
- **Columns**: Dataset (str), Cost Component (str), Basis of Measurement (str), Standard Foreign Rate (USD / SGD) (str), Coastal Rate (INR) (str), Free Time Allowance (str), Slab Tiers / Post-Free Time Escalation (str)
- **Date Range**: 0001-01-01 to 0001-01-01
- **Units Detected in Headers**: Standard Foreign Rate (USD / SGD), Coastal Rate (INR)
- **Obvious Issues**: Missing values in: Coastal Rate (INR), Free Time Allowance

**First 10 rows**:
`csv
Dataset,Cost Component,Basis of Measurement,Standard Foreign Rate (USD / SGD),Coastal Rate (INR),Free Time Allowance,Slab Tiers / Post-Free Time Escalation
East India (Paradip Port),Port Dues,Per GRT per entry,$0.45,₹12.50,,Flat entry fee based on vessel liquid/dry bulk class
East India (Paradip Port),Pilotage & Towage,Per GRT per inward+outward move,$1.00,₹27.00,,Includes 2 standard tug assists; extra fees for overstaying pilot
East India (Paradip Port),Berth Hire (Dockage),Per GRT per hour,$0.009,₹0.448,,Calculated continuously from first line fast to unberth
East India (Paradip Port),Penal Berth Hire,Per GRT per hour,Slab Equivalent,₹16.61 to ₹49.84,2 Hours,"Applies after 2 hrs of cargo completion: 0-6h, 6-12h, >12h stepped rates"
East India (Paradip Port),Port Demurrage (Dry Bulk),Per Metric Tonne per day,Slab Equivalent,₹15 to ₹60,5 Days,Days 1-5: ₹15/MT | Days 6-10: ₹30/MT | >10 Days: ₹60/MT
East India (Paradip Port),Container Terminal Demurrage,Per TEU per day,$15.00,Equivalent INR,3 Days,Days 4-10: $15/day | >10 Days: $30/day (FEU is 200%)
International (Singapore - MPA/PSA),Port Dues (Cargo Call),Per 100 GT per stay length,SGD $8.00 to $9.00,,,Day 1: SGD $8.00 | Day 2: SGD $8.50 | Day 3: SGD $9.00 (per 100 GT)
International (Singapore - MPA/PSA),Port Dues (Bunker Concession),Per 100 GT per stay length,SGD $1.00 to $5.50,,,Concession for short stays: Day 1: SGD $1.00 | Day 2: SGD $5.50
International (Singapore - MPA/PSA),PSA Pilotage,Per movement (Base + Hourly),SGD $250 + $120/hr,,,Base charge plus dynamic blocks based on vessel GT matrix
International (Singapore - MPA/PSA),Towage / Tug Services,Per tug per hour,SGD $600 to $1200,,,Varies by bollard pull capacity and time block increments
`

**Last 10 rows**:
`csv
Dataset,Cost Component,Basis of Measurement,Standard Foreign Rate (USD / SGD),Coastal Rate (INR),Free Time Allowance,Slab Tiers / Post-Free Time Escalation
East India (Paradip Port),Berth Hire (Dockage),Per GRT per hour,$0.009,₹0.448,,Calculated continuously from first line fast to unberth
East India (Paradip Port),Penal Berth Hire,Per GRT per hour,Slab Equivalent,₹16.61 to ₹49.84,2 Hours,"Applies after 2 hrs of cargo completion: 0-6h, 6-12h, >12h stepped rates"
East India (Paradip Port),Port Demurrage (Dry Bulk),Per Metric Tonne per day,Slab Equivalent,₹15 to ₹60,5 Days,Days 1-5: ₹15/MT | Days 6-10: ₹30/MT | >10 Days: ₹60/MT
East India (Paradip Port),Container Terminal Demurrage,Per TEU per day,$15.00,Equivalent INR,3 Days,Days 4-10: $15/day | >10 Days: $30/day (FEU is 200%)
International (Singapore - MPA/PSA),Port Dues (Cargo Call),Per 100 GT per stay length,SGD $8.00 to $9.00,,,Day 1: SGD $8.00 | Day 2: SGD $8.50 | Day 3: SGD $9.00 (per 100 GT)
International (Singapore - MPA/PSA),Port Dues (Bunker Concession),Per 100 GT per stay length,SGD $1.00 to $5.50,,,Concession for short stays: Day 1: SGD $1.00 | Day 2: SGD $5.50
International (Singapore - MPA/PSA),PSA Pilotage,Per movement (Base + Hourly),SGD $250 + $120/hr,,,Base charge plus dynamic blocks based on vessel GT matrix
International (Singapore - MPA/PSA),Towage / Tug Services,Per tug per hour,SGD $600 to $1200,,,Varies by bollard pull capacity and time block increments
International (Singapore - MPA/PSA),Berth Dockage / Quay Hire,Per 100m LOA per hour,SGD $35 to $75,,,Charged based on Length Overall occupancy grid at terminal quay
International (Singapore - MPA/PSA),Terminal Container Demurrage,Per TEU per day,SGD $40 to $80,,3 to 5 Days,Days 6-10: SGD $40/day | >10 Days: SGD $80/day
`
\n### 5. Fuel / bunker price data
- **File**: DATASETS/raw/ship_and_bunker_multiport_fuel_prices_2026-09-11_to_2026-09-25.csv
- **Rows**: 33
- **Columns**: date (str), port (str), VLSFO_USD_per_mt (float64), MGO_USD_per_mt (float64), HSFO_IFO380_USD_per_mt (float64), source (str), source_url (str)
- **Date Range**: 2026-09-11 to 2026-09-25
- **Units Detected in Headers**: None explicitly in column names
- **Obvious Issues**: None obvious

**First 10 rows**:
`csv
date,port,VLSFO_USD_per_mt,MGO_USD_per_mt,HSFO_IFO380_USD_per_mt,source,source_url
2026-09-25,Fujairah,983.5,1694.5,705.0,Ship & Bunker,https://shipandbunker.com/prices/emea/me/ae-fjr-fujairah
2026-09-25,Hong Kong,895.0,1327.5,850.5,Ship & Bunker,https://shipandbunker.com/prices/apac/ea/cn-hok-hong-kong
2026-09-25,Singapore,879.0,1310.0,740.0,Ship & Bunker,https://shipandbunker.com/prices/apac/sea/sg-sin-singapore
2026-09-24,Fujairah,996.0,1698.0,701.0,Ship & Bunker,https://shipandbunker.com/prices/emea/me/ae-fjr-fujairah
2026-09-24,Hong Kong,903.0,1331.0,826.0,Ship & Bunker,https://shipandbunker.com/prices/apac/ea/cn-hok-hong-kong
2026-09-24,Singapore,874.0,1325.0,711.5,Ship & Bunker,https://shipandbunker.com/prices/apac/sea/sg-sin-singapore
2026-09-23,Fujairah,982.0,1686.0,679.5,Ship & Bunker,https://shipandbunker.com/prices/emea/me/ae-fjr-fujairah
2026-09-23,Hong Kong,881.5,1341.5,788.0,Ship & Bunker,https://shipandbunker.com/prices/apac/ea/cn-hok-hong-kong
2026-09-23,Singapore,859.5,1328.5,695.0,Ship & Bunker,https://shipandbunker.com/prices/apac/sea/sg-sin-singapore
2026-09-22,Fujairah,994.0,1661.5,702.0,Ship & Bunker,https://shipandbunker.com/prices/emea/me/ae-fjr-fujairah
`

**Last 10 rows**:
`csv
date,port,VLSFO_USD_per_mt,MGO_USD_per_mt,HSFO_IFO380_USD_per_mt,source,source_url
2026-09-16,Singapore,916.5,1464.0,764.0,Ship & Bunker,https://shipandbunker.com/prices/apac/sea/sg-sin-singapore
2026-09-15,Fujairah,1005.0,1702.5,763.5,Ship & Bunker,https://shipandbunker.com/prices/emea/me/ae-fjr-fujairah
2026-09-15,Hong Kong,938.0,1452.0,813.5,Ship & Bunker,https://shipandbunker.com/prices/apac/ea/cn-hok-hong-kong
2026-09-15,Singapore,908.0,1448.0,770.0,Ship & Bunker,https://shipandbunker.com/prices/apac/sea/sg-sin-singapore
2026-09-14,Fujairah,987.5,1698.5,769.5,Ship & Bunker,https://shipandbunker.com/prices/emea/me/ae-fjr-fujairah
2026-09-14,Hong Kong,929.5,1402.5,811.5,Ship & Bunker,https://shipandbunker.com/prices/apac/ea/cn-hok-hong-kong
2026-09-14,Singapore,895.0,1428.0,766.0,Ship & Bunker,https://shipandbunker.com/prices/apac/sea/sg-sin-singapore
2026-09-11,Fujairah,959.0,1608.5,720.0,Ship & Bunker,https://shipandbunker.com/prices/emea/me/ae-fjr-fujairah
2026-09-11,Hong Kong,910.5,1370.5,776.0,Ship & Bunker,https://shipandbunker.com/prices/apac/ea/cn-hok-hong-kong
2026-09-11,Singapore,878.5,1375.0,721.5,Ship & Bunker,https://shipandbunker.com/prices/apac/sea/sg-sin-singapore
`
\n### 5. Fuel / bunker price data [File 2]
- **File**: DATASETS/raw/marine_fuel_prices_east_coast_india.csv
- **Rows**: 24
- **Columns**: Port / Location (str), Region (str), Fuel Grade (str), 2022 (str), 2023 (str), 2024 (str), 2025-2026 (str)
- **Date Range**: N/A
- **Units Detected in Headers**: None explicitly in column names
- **Obvious Issues**: None obvious

**First 10 rows**:
`csv
Port / Location,Region,Fuel Grade,2022,2023,2024,2025-2026
Chennai (INMAA),East Coast India,VLSFO 0.5%,"$890 - $1,020",$640 - $780,$625 - $716,"$662 - $1,015"
Chennai (INMAA),East Coast India,LSMGO 0.1%,"$1,280 - $1,460","$890 - $1,080",$810 - $893,"$814 - $1,420"
Visakhapatnam (INVTZ),East Coast India,VLSFO 0.5%,"$915 - $1,040",$665 - $795,$640 - $745,"$925 - $1,020"
Visakhapatnam (INVTZ),East Coast India,LSMGO 0.1%,"$1,310 - $1,490","$920 - $1,110",$835 - $915,"$1,380 - $1,490"
Haldia / Kolkata (INHAL),East Coast India,VLSFO 0.5%,"$900 - $1,035",$650 - $785,$635 - $730,$659 - $998
Haldia / Kolkata (INHAL),East Coast India,MGO 0.1%,"$1,320 - $1,510","$910 - $1,130",$825 - $920,"$827 - $1,450"
Paradip (INPRT),East Coast India,VLSFO 0.5%,"$920 - $1,050",$660 - $790,$630 - $735,"$675 - $1,020"
Paradip (INPRT),East Coast India,LSMGO 0.1%,"$1,320 - $1,520","$910 - $1,115",$830 - $920,"$840 - $1,460"
Dhamra (INDHM),East Coast India,VLSFO 0.5%,"$935 - $1,065",$675 - $805,$645 - $750,"$690 - $1,035"
Dhamra (INDHM),East Coast India,LSMGO 0.1%,"$1,340 - $1,540","$930 - $1,130",$845 - $935,"$860 - $1,485"
`

**Last 10 rows**:
`csv
Port / Location,Region,Fuel Grade,2022,2023,2024,2025-2026
Tuticorin (INTUT),South/East Coast Edge,VLSFO 0.5%,"$895 - $1,025",$640 - $770,$620 - $715,"$655 - $1,005"
Tuticorin (INTUT),South/East Coast Edge,LSMGO 0.1%,"$1,285 - $1,475","$890 - $1,085",$810 - $895,"$815 - $1,415"
Gopalpur (INGPR),East Coast India,VLSFO 0.5%,"$925 - $1,055",$668 - $798,$638 - $740,"$680 - $1,025"
Gopalpur (INGPR),East Coast India,LSMGO 0.1%,"$1,330 - $1,530","$915 - $1,120",$835 - $925,"$850 - $1,475"
Gangavaram (INGAV),East Coast India,VLSFO 0.5%,"$915 - $1,040",$660 - $790,$638 - $742,"$920 - $1,018"
Gangavaram (INGAV),East Coast India,LSMGO 0.1%,"$1,310 - $1,490","$920 - $1,110",$835 - $915,"$1,375 - $1,485"
Singapore (SGSIN),Southeast Asia Hub,VLSFO 0.5%,$750 - $904,$580 - $710,$590 - $680,$773 - $874
Singapore (SGSIN),Southeast Asia Hub,LSMGO 0.1%,"$1,050 - $1,350",$760 - $940,$720 - $850,"$1,300 - $1,351"
Colombo (LKCMB),Sri Lanka Hub,VLSFO 0.5%,"$870 - $1,010",$630 - $760,$615 - $710,"$694 - $1,005"
Colombo (LKCMB),Sri Lanka Hub,MGO 0.1%,"$1,120 - $1,410","$840 - $1,030",$770 - $880,"$799 - $1,360"
`
\n### 6. Commodity list (types, typical cargo quantities per route if present)
- **MISSING** as a dedicated file, though present as columns in the main datasets.
\n### 7. Any freight rate data
- **MISSING** (Freight Rate is completely blank/null in shipping_dataset.json and not present in other files).
\n### 8. Any other dataset file present
- complete_shipping_decision_dataset.xlsx: Same as SIH26006 dataset.
