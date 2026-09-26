import pdfplumber
from pathlib import Path
import os
import pandas as pd

raw_dir = Path("C:/Users/umang/SIH/DATASETS/raw")
out_dir = Path("C:/Users/umang/SIH/data/reference/processed")
out_dir.mkdir(parents=True, exist_ok=True)

def inspect_pdf(filename, max_pages=15):
    filepath = raw_dir / filename
    print(f"\n=====================================")
    print(f"Inspecting {filename}")
    print(f"=====================================")
    
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return
        
    try:
        with pdfplumber.open(filepath) as pdf:
            print(f"Total pages: {len(pdf.pages)}")
            
            table_count = 0
            for i, page in enumerate(pdf.pages[:max_pages]):
                tables = page.extract_tables()
                if tables:
                    for j, table in enumerate(tables):
                        table_count += 1
                        print(f"\n--- Page {i+1} Table {j+1} (Rows: {len(table)}, Cols: {len(table[0]) if table else 0}) ---")
                        # Print first 3 rows
                        for row in table[:3]:
                            print([str(cell)[:50].replace('\n', ' ') if cell else '' for cell in row])
                            
                        # Extract table to CSV if it looks structured
                        if len(table) > 2 and len(table[0]) > 2:
                            df = pd.DataFrame(table[1:], columns=table[0])
                            out_name = f"{filename.split('.')[0]}_p{i+1}_t{j+1}.csv"
                            df.to_csv(out_dir / out_name, index=False)
                            print(f"-> Saved as {out_name}")
                            
            print(f"\nTotal tables found in first {max_pages} pages: {table_count}")
    except Exception as e:
        print(f"Error reading {filename}: {e}")

pdfs_to_check = [
    "Cargo handled at Major Ports April 2026.pdf",
    "Indian_20Shipping_20Statistics_202025.pdf.pdf",
    "updates_20on_20indian_20port_20sector_2031032023.pdf.pdf"
]

for pdf in pdfs_to_check:
    inspect_pdf(pdf)

