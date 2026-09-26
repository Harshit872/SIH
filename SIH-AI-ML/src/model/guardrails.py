import pandas as pd
import joblib

# 1. Compute Training Ranges
df_train = pd.read_csv('DATASETS/processed/synthetic_voyages_v1.csv')
num_features = ['quantity_mt', 'route_distance_nm', 'bunker_price_usd_per_mt', 'bdi_value_synthetic']
training_ranges = {}
for col in num_features:
    training_ranges[col] = {
        'min': df_train[col].min(),
        'max': df_train[col].max()
    }

# Load model and categories
model = joblib.load('MODELS/freight_rate_lgbm_v1.pkl')
features = ['origin_port', 'destination_port', 'vessel_class', 'cargo_type', 
            'quantity_mt', 'route_distance_nm', 'bunker_price_usd_per_mt', 'bdi_value_synthetic']
cat_cols = ['origin_port', 'destination_port', 'vessel_class', 'cargo_type']
df_train['vessel_class'] = df_train['vessel_class'].replace('Handymax / Supramax', 'Supramax')
cat_dtypes = {col: df_train[col].unique() for col in cat_cols}

# 2 & 3. Wrapper Function
def predict_with_guardrails(input_dicts):
    df_input = pd.DataFrame(input_dicts)
    
    # Cast categories exactly as in training
    for col in cat_cols:
        df_input[col] = pd.Categorical(df_input[col], categories=cat_dtypes[col])
        
    preds = model.predict(df_input[features])
    
    results = []
    for i, row in df_input.iterrows():
        out_of_range = []
        for f in num_features:
            val = row[f]
            if pd.notnull(val):
                if val < training_ranges[f]['min'] or val > training_ranges[f]['max']:
                    out_of_range.append(f)
                    
        confidence = "low_confidence_out_of_range" if len(out_of_range) > 0 else "normal"
        results.append({
            'prediction': preds[i],
            'confidence_flag': confidence,
            'out_of_range_features': out_of_range
        })
    return results

# 4. Test Scenarios
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

test_inputs = [row1, row2, row3]
results = predict_with_guardrails(test_inputs)

print("Training Ranges:")
for k, v in training_ranges.items():
    print(f"  {k}: {v['min']} to {v['max']}")

print("\nResults:")
for i, res in enumerate(results):
    print(f"Row {i+1}: Pred =  | Flag = {res['confidence_flag']} | OutOfRange = {res['out_of_range_features']}")

