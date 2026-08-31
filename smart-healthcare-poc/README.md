# Smart Healthcare Doctor Specialty Recommendation POC (Phase 1)

This is a Phase 1 Proof-of-Concept for a symptom-based doctor specialty recommendation system. It features a simple frontend questionnaire and a Python Flask backend serving predictions from a pre-trained Logistic Regression model.

## Features
- **Clean UI**: Simple question-by-question flow for 10 binary symptoms.
- **Backend API**: Python Flask endpoint to process the answers and return predictions.
- **Machine Learning Integration**: Loads a `.joblib` model and maps its numerical outputs to exact medical specialties.

## Project Structure
```
smart-healthcare-poc/
│
├── backend/
│   ├── app.py                         # Flask server and API endpoint
│   ├── requirements.txt               # Python dependencies
│   ├── test_api.py                    # Script to test the /predict endpoint
│   └── model/
│       └── logistic_regression_model.joblib  # Trained ML model
│
└── frontend/                          # Simple HTML/CSS/JS web application
    ├── index.html
    ├── style.css
    └── script.js
```

## How to Install

1. Navigate to the `backend` directory.
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Where the model file goes
The pre-trained model `logistic_regression_model.joblib` must be placed inside the `backend/model/` directory.

## How to Run
Start the backend server (which also serves the frontend):
```bash
python app.py
```
Then, open your web browser and navigate to the local URL:
**http://localhost:5000**

## How the Frontend Talks to the Backend
The frontend JavaScript collects the answers to all 10 questions into a JSON object and sends a `POST` request to the backend's `/predict` API endpoint. The backend processes this JSON, feeds it to the Logistic Regression model, and returns the top 3 recommended specialties along with their probabilities.

## 10 Input Feature Names
The model expects exactly these 10 features in this specific order. Values must be `1` (Yes) or `0` (No).
1. `fever`
2. `cough`
3. `breathlessness`
4. `chest_pain`
5. `headache`
6. `digestive_problem`
7. `joint_or_muscle_problem`
8. `skin_problem`
9. `urinary_problem`
10. `fatigue`

## Prediction API Request/Response Format

**Endpoint:** `POST /predict`

**Request Format (JSON):**
```json
{
  "fever": 0,
  "cough": 1,
  "breathlessness": 1,
  "chest_pain": 0,
  "headache": 0,
  "digestive_problem": 0,
  "joint_or_muscle_problem": 0,
  "skin_problem": 0,
  "urinary_problem": 0,
  "fatigue": 1
}
```

**Response Format (JSON):**
```json
{
  "recommended_specialty": "Pulmonology",
  "top_matches": [
    {
      "specialty": "Pulmonology",
      "probability": 0.82
    },
    {
      "specialty": "Cardiology",
      "probability": 0.09
    },
    {
      "specialty": "General Medicine",
      "probability": 0.06
    }
  ]
}
```

## Scope Control
This is Phase 1 ONLY. It intentionally excludes databases, authentication, advanced routing, appointment booking, or conversational AI.

