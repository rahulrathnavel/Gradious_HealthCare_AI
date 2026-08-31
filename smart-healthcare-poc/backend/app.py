import joblib
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='/')

FEATURES = [
    "fever",
    "cough",
    "breathlessness",
    "chest_pain",
    "headache",
    "digestive_problem",
    "joint_or_muscle_problem",
    "skin_problem",
    "urinary_problem",
    "fatigue"
]

# Verified from the notebook output
CLASS_MAPPING = {
    0: "Cardiology",
    1: "Dermatology",
    2: "Gastroenterology",
    3: "General Medicine",
    4: "Neurology",
    5: "Orthopedics",
    6: "Pulmonology",
    7: "Urology"
}

# Load the model
model_path = os.path.join(os.path.dirname(__file__), "model", "logistic_regression_model.joblib")
model = joblib.load(model_path)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate fields
        answers = {}
        for feature in FEATURES:
            if feature not in data:
                return jsonify({"error": f"Missing required feature: {feature}"}), 400
            
            value = data[feature]
            if value not in [0, 1]:
                return jsonify({"error": f"Invalid value for {feature}. Must be 0 or 1."}), 400
                
            answers[feature] = value

        # Create DataFrame
        X = pd.DataFrame([[answers[f] for f in FEATURES]], columns=FEATURES)

        # Predict probabilities
        probabilities = model.predict_proba(X)[0]
        classes = model.classes_

        # Rank predictions
        ranked = sorted(
            zip(classes, probabilities),
            key=lambda x: x[1],
            reverse=True
        )

        results = []
        for class_id, probability in ranked[:3]:
            specialty_name = CLASS_MAPPING.get(int(class_id), str(class_id))
            results.append({
                "specialty": specialty_name,
                "probability": float(probability)
            })

        response = {
            "recommended_specialty": results[0]["specialty"],
            "top_matches": results
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Smart Healthcare POC server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

