import os
import pandas as pd
import numpy as np

output = []

def analyze_csv(filepath, category_name):
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        elif filepath.endswith('.json'):
            import json
            with open(filepath, 'r') as f:
                d = json.load(f)
            # Just grab the BDI part for JSON to show its structure
            if '01_BDI' in d:
                df = pd.DataFrame(d['01_BDI'])
            else:
                df = pd.DataFrame()
        else:
            return
            
        if df.empty:
            output.append(f"### {category_name}\n- **MISSING** (No data or empty file)\n")
            return
            
        out = f"### {category_name}\n"
        out += f"- **File**: {filepath}\n"
        out += f"- **Rows**: {len(df)}\n"
        
        # Columns and Types
        cols = []
        for col, dtype in df.dtypes.items():
            cols.append(f"{col} ({dtype})")
        out += f"- **Columns**: {', '.join(cols)}\n"
        
        # Date range
        date_cols = [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower() or 'day' in c.lower()]
        if date_cols:
            try:
                dt = pd.to_datetime(df[date_cols[0]], errors='coerce')
                dt = dt.dropna()
                if not dt.empty:
                    out += f"- **Date Range**: {dt.min().strftime('%Y-%m-%d')} to {dt.max().strftime('%Y-%m-%d')}\n"
                else:
                    out += f"- **Date Range**: Could not parse dates in {date_cols[0]}\n"
            except:
                out += f"- **Date Range**: Present but not easily parsable ({date_cols[0]})\n"
        else:
            out += f"- **Date Range**: N/A\n"
            
        # Units
        out += f"- **Units Detected in Headers**: "
        units = [c for c in df.columns if '(' in c and ')' in c]
        if units:
            out += ", ".join(units) + "\n"
        else:
            out += "None explicitly in column names\n"
            
        # Issues
        issues = []
        nulls = df.isnull().sum()
        if nulls.sum() > 0:
            issues.append(f"Missing values in: {', '.join(nulls[nulls > 0].index.tolist())}")
        if df.duplicated().sum() > 0:
            issues.append(f"{df.duplicated().sum()} duplicate rows")
        if not issues:
            issues.append("None obvious")
        out += f"- **Obvious Issues**: {'; '.join(issues)}\n"
        
        # Head and tail
        out += "\n**First 10 rows**:\n`csv\n"
        out += df.head(10).to_csv(index=False)
        out += "`\n"
        
        out += "\n**Last 10 rows**:\n`csv\n"
        out += df.tail(10).to_csv(index=False)
        out += "`\n"
        
        output.append(out)
    except Exception as e:
        output.append(f"### {category_name}\n- **Error reading file**: {filepath} ({str(e)})\n")

analyze_csv('DATASETS/raw/baltic_indices_historical.csv', '1. Baltic Dry Index (BDI) historical data')
analyze_csv('SIH-FRONTEND/src/data/generated/shipping_dataset.json', '2. Route / port list (origin-destination pairs, distances if present)')
analyze_csv('DATASETS/raw/SIH26006_Freight_Chartering_Dataset.xlsx', '3. Vessel specifications (class, DWT, draft, LOA, beam, speed)')
analyze_csv('DATASETS/raw/Maritime Port Performance Project Dataset.csv', '4. Port data (turnaround times, costs, restrictions, depth limits) [File 1]')
analyze_csv('DATASETS/raw/port_cost_specifications.csv', '4. Port data [File 2]')
analyze_csv('DATASETS/raw/ship_and_bunker_multiport_fuel_prices_2026-09-11_to_2026-09-25.csv', '5. Fuel / bunker price data')
analyze_csv('DATASETS/raw/marine_fuel_prices_east_coast_india.csv', '5. Fuel / bunker price data [File 2]')
output.append("### 6. Commodity list (types, typical cargo quantities per route if present)\n- **MISSING** as a dedicated file, though present as columns in the main datasets.\n")
output.append("### 7. Any freight rate data\n- **MISSING** (Freight Rate is completely blank/null in shipping_dataset.json and not present in other files).\n")
output.append("### 8. Any other dataset file present\n- complete_shipping_decision_dataset.xlsx: Same as SIH26006 dataset.\n")

with open('report_out.md', 'w', encoding='utf-8') as f:
    f.write('\\n'.join(output))

