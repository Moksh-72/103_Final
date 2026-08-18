import os
import joblib
import pandas as pd

# Load model and transformer relative to this file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
TRANSFORMER_PATH = os.path.join(BASE_DIR, "transformer.pkl")

model = joblib.load(MODEL_PATH)
transformer = joblib.load(TRANSFORMER_PATH)

def load_artifacts():
    """Returns loaded model and transformer."""
    return model, transformer

def preprocess_and_predict(customer_data):
    """
    Accepts raw customer JSON data as a dict, applies preprocessing pipeline,
    and returns churn prediction and probability.
    """
    # Handle optional outer 'customer' key
    if isinstance(customer_data, dict) and "customer" in customer_data:
        customer_dict = customer_data["customer"]
    else:
        customer_dict = customer_data

    # Convert to single-row DataFrame
    df = pd.DataFrame([customer_dict])

    # Remove non-feature columns if present
    for col in ['customerID', 'Churn']:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Ensure TotalCharges is numeric
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Apply preprocessing pipeline
    X_transformed = transformer.transform(df)

    # Make probability prediction
    proba = float(model.predict_proba(X_transformed)[0][1])
    pred_label = "Yes" if proba >= 0.5 else "No"

    return {
        "churn_probability": round(proba, 4),
        "churn_prediction": pred_label
    }
