import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify

try:
    from app.utils import preprocess_and_predict
except ImportError:
    from utils import preprocess_and_predict

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400

        result = preprocess_and_predict(data)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask API server on port 8000...", flush=True)
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)

