import os
import pandas as pd
import numpy as np
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

def train():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "customer_churn_dataset-training-master (1).csv")
    if not os.path.exists(data_path):
        data_path = os.path.join(base_dir, "customer_churn_dataset-training-master (1).csv")
    if not os.path.exists(data_path):
        data_path = "customer_churn_dataset-training-master (1).csv"

    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)

    # Creating X and y
    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    # Step 1: Drop the 'customerID' column
    if 'customerID' in X.columns:
        X = X.drop(columns=['customerID'])

    # Step 2: Convert 'TotalCharges' to numeric (handles spaces or non-numeric values)
    X['TotalCharges'] = pd.to_numeric(X['TotalCharges'], errors='coerce')

    # Step 3: Convert target column 'y' to binary values
    if y.dtype == object:
        y = y.map({'Yes': 1, 'No': 0})

    # Step 4: Identify column types
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    print("Numerical columns:", numerical_cols)
    print("Categorical columns:", categorical_cols)

    # Step 5: Define preprocessing pipeline (no model yet)
    try:
        ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown='ignore', sparse=False)

    preprocessor = ColumnTransformer(transformers=[
        ('num', SimpleImputer(strategy='mean'), numerical_cols),
        ('cat', ohe, categorical_cols)
    ])

    # Step 6: Apply the transformation to the data
    X_cleaned = preprocessor.fit_transform(X)
    print("Transformed shape:", X_cleaned.shape)

    # Train Model
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_cleaned, y)

    acc = accuracy_score(y, model.predict(X_cleaned))
    auc = roc_auc_score(y, model.predict_proba(X_cleaned)[:, 1])
    print(f"Model Accuracy: {acc:.4f}, ROC-AUC: {auc:.4f}")

    app_dir = os.path.join(base_dir, "app")
    os.makedirs(app_dir, exist_ok=True)

    joblib.dump(model, os.path.join(app_dir, "model.pkl"))
    joblib.dump(preprocessor, os.path.join(app_dir, "transformer.pkl"))
    print("Model and Transformer saved successfully in app/ directory.")

if __name__ == "__main__":
    train()
