import argparse
import os
import logging
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def setup_logging():
    os.makedirs('logs', exist_ok=True)
    log_file = os.path.join('logs', 'batch_log.txt')
    
    logger = logging.getLogger('batch_scoring')
    logger.setLevel(logging.INFO)
    
    if logger.hasHandlers():
        logger.handlers.clear()
        
    file_handler = logging.FileHandler(log_file, mode='a')
    console_handler = logging.StreamHandler()
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def score_row(args_tuple):
    idx, row_dict, session, url = args_tuple
    payload = {"customer": row_dict}
    try:
        response = session.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            data = response.json()
            prob = data.get("churn_probability", 0.0)
            pred = data.get("churn_prediction", "No")
            row_dict["churn_probability"] = prob
            row_dict["churn_prediction"] = pred
            return idx, row_dict, True, prob, None
        else:
            err_msg = f"Status {response.status_code}: {response.text}"
            row_dict["churn_probability"] = None
            row_dict["churn_prediction"] = "ERROR"
            return idx, row_dict, False, 0.0, err_msg
    except Exception as e:
        row_dict["churn_probability"] = None
        row_dict["churn_prediction"] = "ERROR"
        return idx, row_dict, False, 0.0, str(e)

def run_batch_scoring(input_path, api_url="http://localhost:8000/predict", output_path="scored_customers.csv"):
    logger = setup_logging()
    logger.info(f"Starting batch scoring job for input file: {input_path}")
    
    if not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}")
        return

    df = pd.read_csv(input_path)
    total_requests = len(df)
    logger.info(f"Total customers to score: {total_requests}")

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50)
    session.mount('http://', adapter)

    # Verify working API endpoint
    test_payload = {"customer": df.iloc[0].to_dict()}
    working_url = api_url
    try:
        res = session.post(api_url, json=test_payload, timeout=3)
        if res.status_code != 200:
            for alt_host in ["http://127.0.0.1:8000/predict", "http://192.168.0.102:8000/predict"]:
                try:
                    alt_res = session.post(alt_host, json=test_payload, timeout=2)
                    if alt_res.status_code == 200:
                        working_url = alt_host
                        logger.info(f"Using active endpoint URL: {working_url}")
                        break
                except Exception:
                    pass
    except Exception:
        pass

    tasks = [(idx, row.to_dict(), session, working_url) for idx, row in df.iterrows()]
    
    scored_results = [None] * total_requests
    success_count = 0
    failure_count = 0
    total_churn_prob = 0.0

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(score_row, tasks)
        for idx, row_dict, success, prob, err_msg in results:
            scored_results[idx] = row_dict
            if success:
                success_count += 1
                total_churn_prob += prob
            else:
                failure_count += 1
                logger.error(f"Row {idx} prediction failed: {err_msg}")

    scored_df = pd.DataFrame(scored_results)
    scored_df.to_csv(output_path, index=False)
    logger.info(f"Scored results saved to: {output_path}")

    avg_probability = (total_churn_prob / success_count) if success_count > 0 else 0.0
    
    logger.info("=== BATCH SCORING SUMMARY ===")
    logger.info(f"Total Requests Processed: {total_requests}")
    logger.info(f"Successful Predictions:   {success_count}")
    logger.info(f"Failed Predictions:       {failure_count}")
    logger.info(f"Average Churn Probability: {avg_probability:.4f}")
    logger.info("=============================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Scoring Script for Customer Churn Model")
    parser.add_argument("--input", type=str, default="test_data/all_customers.csv", help="Path to input CSV file")
    args = parser.parse_args()
    
    run_batch_scoring(args.input)
