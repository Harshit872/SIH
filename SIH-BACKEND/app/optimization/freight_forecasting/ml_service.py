import os
import joblib
import pandas as pd

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../SIH-AI-ML/models/freight_rate_lgbm_v1.pkl'))

# Load model globally on module import
try:
    _model = joblib.load(MODEL_PATH)
except Exception as e:
    _model = None
    _model_error = str(e)

TRAINING_RANGES = {
    'quantity_mt': {'min': 10116, 'max': 170453},
    'route_distance_nm': {'min': 4600, 'max': 6300},
    'bunker_price_usd_per_mt': {'min': 701.64, 'max': 999.39},
    'bdi_value_synthetic': {'min': 500, 'max': 2993}
}

CAT_DTYPES = {
    'origin_port': ['Port Hedland, Australia', 'Gladstone, Australia', 'Richards Bay, South Africa'],
    'destination_port': ['Visakhapatnam, India', 'Paradip, India'],
    'vessel_class': ['Handysize', 'Supramax', 'Panamax', 'Capesize'],
    'cargo_type': ['Iron Ore', 'Coal']
}
FEATURES = ['origin_port', 'destination_port', 'vessel_class', 'cargo_type', 
            'quantity_mt', 'route_distance_nm', 'bunker_price_usd_per_mt', 'bdi_value_synthetic']

def predict_freight_rate(origin: str, destination: str, vessel_class: str, commodity: str,
                         cargo_mt: float, route_distance_nm: float, bunker_price: float, bdi_value: float):
    if _model is None:
        raise RuntimeError(f"Model failed to load at startup: {_model_error}")
        
    input_dict = {
        'origin_port': origin,
        'destination_port': destination,
        'vessel_class': vessel_class,
        'cargo_type': commodity,
        'quantity_mt': cargo_mt,
        'route_distance_nm': route_distance_nm,
        'bunker_price_usd_per_mt': bunker_price,
        'bdi_value_synthetic': bdi_value
    }
    
    df_input = pd.DataFrame([input_dict])
    
    for col, cats in CAT_DTYPES.items():
        df_input[col] = pd.Categorical(df_input[col], categories=cats)
        
    try:
        pred = _model.predict(df_input[FEATURES])[0]
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")
        
    out_of_range = []
    for col, bounds in TRAINING_RANGES.items():
        val = input_dict[col]
        if val < bounds['min'] or val > bounds['max']:
            out_of_range.append(col)
            
    confidence = "low_confidence_out_of_range" if len(out_of_range) > 0 else "normal"
    
    return {
        "predicted_freight_rate_usd_per_mt": float(pred),
        "confidence_flag": confidence,
        "out_of_range_features": out_of_range,
        "model_version": "lgbm_v1",
        "is_model_trained_on_synthetic_data": True
    }
