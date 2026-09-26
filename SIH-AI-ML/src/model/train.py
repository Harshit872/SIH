import os
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import joblib

# Load Data
df = pd.read_csv('DATASETS/processed/synthetic_voyages_v1.csv')
df['date'] = pd.to_datetime(df['date'])

# Step 0: Clean vessel_class
df['vessel_class'] = df['vessel_class'].replace('Handymax / Supramax', 'Supramax')

# Step 1: Train/Test Split (Time-based)
df = df.sort_values('date').reset_index(drop=True)
split_idx = int(len(df) * 0.8)
cutoff_date = df.iloc[split_idx]['date']

train_df = df.iloc[:split_idx].copy()
test_df = df.iloc[split_idx:].copy()

print(f"Cutoff date: {cutoff_date.strftime('%Y-%m-%d')}")
print(f"Train size: {len(train_df)}")
print(f"Test size: {len(test_df)}")

# Step 2: Naive Baseline (Last known rate per group)
baseline_preds = []
group_cols = ['origin_port', 'destination_port', 'vessel_class']

for _, row in test_df.iterrows():
    # Find the most recent matching row in the training set
    match = train_df[(train_df['origin_port'] == row['origin_port']) & 
                     (train_df['destination_port'] == row['destination_port']) & 
                     (train_df['vessel_class'] == row['vessel_class'])]
    if not match.empty:
        pred = match.iloc[-1]['freight_rate_usd_per_mt']
    else:
        # Fallback if group unseen in train: global train mean
        pred = train_df['freight_rate_usd_per_mt'].mean()
    baseline_preds.append(pred)

test_df['baseline_pred'] = baseline_preds
baseline_mae = mean_absolute_error(test_df['freight_rate_usd_per_mt'], test_df['baseline_pred'])
baseline_mape = mean_absolute_percentage_error(test_df['freight_rate_usd_per_mt'], test_df['baseline_pred'])

print(f"Baseline MAE: {baseline_mae:.2f}")
print(f"Baseline MAPE: {baseline_mape:.2%}")

# Step 3: LightGBM Model
features = ['origin_port', 'destination_port', 'vessel_class', 'cargo_type', 
            'quantity_mt', 'route_distance_nm', 'bunker_price_usd_per_mt', 'bdi_value_synthetic']
target = 'freight_rate_usd_per_mt'

# Convert categoricals to 'category' type for LightGBM native support
cat_cols = ['origin_port', 'destination_port', 'vessel_class', 'cargo_type']
for col in cat_cols:
    train_df[col] = train_df[col].astype('category')
    test_df[col] = test_df[col].astype('category')

X_train = train_df[features]
y_train = train_df[target]
X_test = test_df[features]
y_test = test_df[target]

model = lgb.LGBMRegressor(random_state=42, n_estimators=100)
model.fit(X_train, y_train, categorical_feature=cat_cols)

train_preds = model.predict(X_train)
test_preds = model.predict(X_test)

lgbm_train_mae = mean_absolute_error(y_train, train_preds)
lgbm_train_mape = mean_absolute_percentage_error(y_train, train_preds)
lgbm_test_mae = mean_absolute_error(y_test, test_preds)
lgbm_test_mape = mean_absolute_percentage_error(y_test, test_preds)

print(f"LGBM Train MAE: {lgbm_train_mae:.2f}, MAPE: {lgbm_train_mape:.2%}")
print(f"LGBM Test MAE: {lgbm_test_mae:.2f}, MAPE: {lgbm_test_mape:.2%}")

# Feature importance
imp = pd.DataFrame({'feature': features, 'importance': model.feature_importances_})
imp = imp.sort_values('importance', ascending=False)
print("Feature Importances (split count):")
print(imp.to_string(index=False))

# Save model
os.makedirs('MODELS', exist_ok=True)
joblib.fit_predict = None # Dummy to avoid pickling issues if any
joblib.dump(model, 'MODELS/freight_rate_lgbm_v1.pkl')

# Step 4: Sanity Check
print("\nSanity Check (5 Random Test Rows):")
sample = test_df.sample(5, random_state=42)
sample['lgbm_pred'] = model.predict(sample[features])
for idx, row in sample.iterrows():
    print(f"Route: {row['origin_port']} -> {row['destination_port']} | Vessel: {row['vessel_class']} | "
          f"Actual:  | Pred: ")

