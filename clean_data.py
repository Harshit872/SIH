import pandas as pd
from pathlib import Path
import numpy as np

processed_dir = Path("C:/Users/umang/SIH/data/reference/processed")

# Clean Table 2 (Traffic Handled at Major Ports)
def clean_port_traffic():
    f_path = processed_dir / "updates_20on_20indian_20port_20sector_2031032023_p10_t1.csv"
    df = pd.read_csv(f_path)
    
    # Extract headers from row 1
    headers = ['Port', 'Col_Drop1', 'Col_Drop2', '2017_18', '2018_19', '2019_20', '2020_21', '2021_22', '2022_23_P', 'Change_Pct']
    
    # Take data from row 3 downwards (ignoring the "1, 2, 3" index row at row 2)
    df_clean = df.iloc[3:].copy()
    df_clean.columns = headers
    
    # Drop the empty parsing artifact columns
    df_clean = df_clean.drop(columns=['Col_Drop1', 'Col_Drop2'])
    
    # Drop rows where Port is NaN
    df_clean = df_clean.dropna(subset=['Port'])
    
    # Remove newline characters from strings
    df_clean = df_clean.replace(r'\n',' ', regex=True)
    
    df_clean.to_csv(processed_dir / "major_ports_traffic_cleaned.csv", index=False)
    print("Cleaned: major_ports_traffic_cleaned.csv")

clean_port_traffic()
