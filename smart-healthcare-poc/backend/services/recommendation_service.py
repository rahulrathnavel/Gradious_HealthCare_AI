import joblib
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

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

class RecommendationService:
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            model_path = os.path.join(os.path.dirname(__file__), "..", "ml", "logistic_regression_model.joblib")
            self.model = joblib.load(model_path)
            logger.info("Logistic Regression model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")

    def predict_specialty(self, answers: dict) -> dict:
        if not self.model:
            raise Exception("ML model is not available")

        # Extract features in exact order
        feature_values = [answers.get(f, 0) for f in FEATURES]
        
        # Create DataFrame
        X = pd.DataFrame([feature_values], columns=FEATURES)

        # Predict probabilities
        probabilities = self.model.predict_proba(X)[0]
        classes = self.model.classes_

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

        return {
            "recommended_specialty": results[0]["specialty"],
            "top_matches": results
        }

# Singleton instance
recommendation_service = RecommendationService()

