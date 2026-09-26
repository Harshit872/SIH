import pandas as pd
import joblib

df = pd.read_csv('DATASETS/processed/synthetic_voyages_v1.csv')
df['date'] = pd.to_datetime(df['date'])
df['vessel_class'] = df['vessel_class'].replace('Handymax / Supramax', 'Supramax')
df = df.sort_values('date').reset_index(drop=True)
split_idx = int(len(df) * 0.8)
test_df = df.iloc[split_idx:].copy()

model = joblib.load('MODELS/freight_rate_lgbm_v1.pkl')
features = ['origin_port', 'destination_port', 'vessel_class', 'cargo_type', 
            'quantity_mt', 'route_distance_nm', 'bunker_price_usd_per_mt', 'bdi_value_synthetic']

cat_cols = ['origin_port', 'destination_port', 'vessel_class', 'cargo_type']
for col in cat_cols:
    test_df[col] = test_df[col].astype('category')

sample = test_df.sample(5, random_state=42)
sample['lgbm_pred'] = model.predict(sample[features])

for idx, row in sample.iterrows():
    actual = row['freight_rate_usd_per_mt']
    pred = row['lgbm_pred']
    print("Route: " + str(row['origin_port']) + " -> " + str(row['destination_port']) + " | Vessel: " + str(row['vessel_class']) + " | Actual: $" + str(round(actual,2)) + " | Pred: $" + str(round(pred,2)))
