import pandas as pd
try:
    xls = pd.ExcelFile('DATASETS/raw/complete_shipping_decision_dataset.xlsx')
    print('complete:', xls.sheet_names)
    for sheet in xls.sheet_names:
        df = pd.read_excel('DATASETS/raw/complete_shipping_decision_dataset.xlsx', sheet_name=sheet, nrows=5)
        print(f"Sheet: {sheet}, cols: {df.columns.tolist()}")
except Exception as e:
    print('error', str(e))
