# Customer Churn Prediction API & Batch Scoring Pipeline

This repository provides a production-ready deployment of a Customer Churn Prediction model. It includes a real-time HTTP inference API built with Flask, an automated nightly batch scoring pipeline with monitoring logs, and a model maintenance strategy.

---

## 📁 Repository Structure

```text
customer-churn-api/
│
├── app/
│   ├── __init__.py          # Empty file making 'app' a module
│   ├── main.py              # Flask application listening on port 8000
│   ├── model.pkl            # Trained Logistic Regression churn model
│   ├── transformer.pkl      # Scikit-learn preprocessing ColumnTransformer
│   └── utils.py             # Inference helper functions
│
├── test_data/
│   ├── sample_input.json    # Sample JSON payload for POST /predict
│   └── all_customers.csv    # Customer dataset for batch scoring
│
├── batch.py                 # Batch scoring pipeline script
├── requirements.txt         # Python dependencies
├── README.md                # Documentation and maintenance plan
└── .gitignore               # Ignored runtime and output files
```

---

## 🚀 Quick Start Guide

### 1. Installation
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Starting the Real-Time Inference API
From the project root (`customer-churn-api`), start the Flask application as a module:
```bash
python -m app.main
```
The API server will launch locally on **`http://localhost:8000`**.

### 3. Real-Time Single Prediction Test
Send a POST request with customer JSON data to `/predict`:

```bash
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d @test_data/sample_input.json
```

**Response Example:**
```json
{
  "churn_prediction": "No",
  "churn_probability": 0.6387
}
```

---

## 🧪 Batch Scoring Pipeline

Run the batch pipeline to score all active customers and generate monitoring statistics:

```bash
python batch.py --input test_data/all_customers.csv
```

### Outputs:
- **`scored_customers.csv`**: Contains all customer input data appended with `churn_probability` and `churn_prediction`.
- **`logs/batch_log.txt`**: Logs total processed requests, failed requests, and average churn probability.

---

## 📊 Maintenance Plan

### 🧠 Retraining Strategy
The customer churn model will be retrained on a monthly scheduled basis using updated 30-day active customer transaction and retention data. Additionally, automated event-driven retraining is triggered if performance monitoring reveals a drop in ROC-AUC below 0.75 or accuracy below 78% on a labeled validation sample. The retraining pipeline automatically ingests raw data from the data lake, applies the pre-fitted `ColumnTransformer` structure to maintain feature consistency, fits a new `LogisticRegression` model, and calculates validation metrics. If the new candidate model out-performs the production baseline on a held-out evaluation dataset by at least 1.5% ROC-AUC without schema errors, the pipeline packages the updated `model.pkl` and `transformer.pkl` artifacts, updates the staging registry, and initiates a blue-green API deployment.

### 📉 Drift Detection
Data and model drift monitoring are integrated into the nightly batch scoring workflow and real-time logging infrastructure. For feature data drift, we calculate Population Stability Index (PSI) and Kolmogorov-Smirnov (KS) statistic on numerical features (`tenure`, `MonthlyCharges`, `TotalCharges`) and Jensen-Shannon distance on categorical feature distributions against training baselines. A PSI > 0.25 flags significant data drift. For concept/model drift, prediction distribution shifts are monitored daily: if the rolling 7-day average churn probability strays by more than 15% from the historical 0.26 baseline, or if API HTTP error rates exceed 1%, an alert is dispatched via PagerDuty/Slack to the MLOps team for root-cause investigation.

### 🛠️ Versioning & Documentation
We enforce Semantic Versioning (`vMAJOR.MINOR.PATCH`) across model artifacts and API code. Major versions (`v2.0.0`) correspond to breaking schema modifications or feature engineering changes requiring pipeline updates. Minor versions (`v1.1.0`) represent scheduled retraining on new data, while patch releases (`v1.0.1`) address bug fixes or hyperparameter tuning. Each model release artifacts (`model_v1.1.0.pkl`, `transformer_v1.1.0.pkl`) are registered in MLflow Artifact Store alongside a Model Card detailing dataset checksums, hyperparameters, accuracy/ROC-AUC metrics, and author details. Git tags track corresponding release code, ensuring full reproducibility and seamless zero-downtime rollback via container image tags.
