import pandas as pd
import joblib

# Load model
model = joblib.load('MODELS/freight_rate_lgbm_v1.pkl')
features = ['origin_port', 'destination_port', 'vessel_class', 'cargo_type', 
            'quantity_mt', 'route_distance_nm', 'bunker_price_usd_per_mt', 'bdi_value_synthetic']
cat_cols = ['origin_port', 'destination_port', 'vessel_class', 'cargo_type']

# Construct 3 novel rows
# Row 1: Unseen Route Combination (Gladstone -> Visakhapatnam) + Capesize
# In training, Gladstone only went to Paradip. Visakhapatnam only received from Port Hedland/Richards Bay.
row1 = {
    'origin_port': 'Gladstone, Australia',
    'destination_port': 'Visakhapatnam, India',
    'vessel_class': 'Capesize',
    'cargo_type': 'Coal',
    'quantity_mt': 150000,
    'route_distance_nm': 5500, # Approx unseen distance
    'bunker_price_usd_per_mt': 850.0,
    'bdi_value_synthetic': 1500
}

# Row 2: Extreme BDI (Out of distribution - 10,000)
row2 = {
    'origin_port': 'Port Hedland, Australia',
    'destination_port': 'Visakhapatnam, India',
    'vessel_class': 'Panamax',
    'cargo_type': 'Iron Ore',
    'quantity_mt': 75000,
    'route_distance_nm': 5300,
    'bunker_price_usd_per_mt': 800.0,
    'bdi_value_synthetic': 10000 # Max in training was 3000
}

# Row 3: Extreme Bunker Price (Out of distribution - ,500/MT)
row3 = {
    'origin_port': 'Richards Bay, South Africa',
    'destination_port': 'Visakhapatnam, India',
    'vessel_class': 'Handysize',
    'cargo_type': 'Coal',
    'quantity_mt': 25000,
    'route_distance_nm': 4600,
    'bunker_price_usd_per_mt': 2500.0, # Max in training was 1000
    'bdi_value_synthetic': 1200
}

df_unseen = pd.DataFrame([row1, row2, row3])
for col in cat_cols:
    df_unseen[col] = df_unseen[col].astype('category')

preds = model.predict(df_unseen)

for i, pred in enumerate(preds):
    print(f"Row {i+1} Pred: ")

