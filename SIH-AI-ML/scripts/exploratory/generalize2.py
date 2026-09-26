import pandas as pd
import joblib

# Load model
model = joblib.load('MODELS/freight_rate_lgbm_v1.pkl')
features = ['origin_port', 'destination_port', 'vessel_class', 'cargo_type', 
            'quantity_mt', 'route_distance_nm', 'bunker_price_usd_per_mt', 'bdi_value_synthetic']
cat_cols = ['origin_port', 'destination_port', 'vessel_class', 'cargo_type']

row1 = {
    'origin_port': 'Gladstone, Australia',
    'destination_port': 'Visakhapatnam, India',
    'vessel_class': 'Capesize',
    'cargo_type': 'Coal',
    'quantity_mt': 150000,
    'route_distance_nm': 5500,
    'bunker_price_usd_per_mt': 850.0,
    'bdi_value_synthetic': 1500
}

row2 = {
    'origin_port': 'Port Hedland, Australia',
    'destination_port': 'Visakhapatnam, India',
    'vessel_class': 'Panamax',
    'cargo_type': 'Iron Ore',
    'quantity_mt': 75000,
    'route_distance_nm': 5300,
    'bunker_price_usd_per_mt': 800.0,
    'bdi_value_synthetic': 10000 
}

row3 = {
    'origin_port': 'Richards Bay, South Africa',
    'destination_port': 'Visakhapatnam, India',
    'vessel_class': 'Handysize',
    'cargo_type': 'Coal',
    'quantity_mt': 25000,
    'route_distance_nm': 4600,
    'bunker_price_usd_per_mt': 2500.0,
    'bdi_value_synthetic': 1200
}

df_unseen = pd.DataFrame([row1, row2, row3])

# Crucial: LightGBM needs the categories to match the training data's categories exactly, 
# otherwise it might fail or give bad predictions.
# We must load the original training data's categories.
df_train = pd.read_csv('DATASETS/processed/synthetic_voyages_v1.csv')
df_train['vessel_class'] = df_train['vessel_class'].replace('Handymax / Supramax', 'Supramax')
for col in cat_cols:
    df_unseen[col] = pd.Categorical(df_unseen[col], categories=df_train[col].unique())

preds = model.predict(df_unseen[features])

for i, pred in enumerate(preds):
    print('Row ' + str(i+1) + ' Pred: USD ' + str(round(pred, 2)))

