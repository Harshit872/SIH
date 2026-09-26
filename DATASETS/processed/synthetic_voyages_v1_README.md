# Data Dictionary: synthetic_voyages_v1.csv

**WARNING: All data in this file is SYNTHETIC (is_synthetic=True for all rows).**
This dataset was generated for training purposes using base assumptions grounded in the actual reference files provided in SIH26006_Freight_Chartering_Dataset.xlsx.

## References Used
1. **Vessel Specs** (5_Vessel_Class_Reference): 
   - Handysize (10-40k DWT, 13.5kn, 21 t/day, Hire: -14k/day)
   - Handymax / Supramax (40-60k DWT, 13.5kn, 26 t/day, Hire: -16k/day)
   - Panamax (60-100k DWT, 13.5kn, 30 t/day, Hire: -20k/day)
   - Capesize (100-180k DWT, 14.5kn, 45 t/day, Hire: -30k/day)
   *Hire rates are typical public ranges scaling linearly with the Baltic Dry Index.*
2. **Route Distances** (6_Route_Distances_Reference):
   - Port Hedland, Australia to Visakhapatnam, India: 5300 nm (Iron Ore)
   - Gladstone, Australia to Paradip, India: 6300 nm (Coal)
   - Richards Bay, South Africa to Visakhapatnam, India: 4600 nm (Coal)
3. **Bunker Prices**: Sampled randomly between  and ,000 USD/mt.
4. **Demurrage Cap**: USD 20,000/day max (derived from 3_SAIL_Coal_Demurrage_CAG).
5. **Port Turnaround**: Used 48 to 94 hours (derived from 2_Port_TRT_Performance).
6. **BDI Proxy**: Synthetically generated random uniform values between 500 and 3000 Index points.

## Formula Logic
- **voyage_days**: 
oute_distance_nm / (speed_knots * 24)
- **daily_hire_rate**: Linearly interpolated between the vessel's min and max hire range, mapped to the synthetic BDI value (500 to 3000).
- **hire_cost_usd**: daily_hire_rate * voyage_days
- **bunker_cost_usd**: oyage_days * daily_consumption * bunker_price_usd_per_mt
- **port_cost_usd**: $30,000 base + (Turnaround_Hours * /hr)
- **demurrage_usd**: Random 0 to 5 days * random rate up to $20,000/day. (50% chance of 0 demurrage).
- **freight_cost_usd**: hire_cost_usd + bunker_cost_usd + port_cost_usd + demurrage_usd
- **freight_rate_usd_per_mt**: reight_cost_usd / quantity_mt
