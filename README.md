# AI-Powered Smart Healthcare Appointment & Assistance System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)

This is a complete, professional, production-quality full-stack application. It securely handles patient symptom recommendations, doctor appointments, and medical report parsing via GenAI.

## Features
1. **Specialist Recommendation**: Uses the trained Logistic Regression model to recommend 1 of 8 medical specialties based on 10 binary symptoms. If no symptoms are selected, routes gracefully to manual doctor booking.
2. **Doctor Discovery & Appointment Booking**: Browse doctors by specialty, view dynamic availability, and book appointments securely. Includes logic to prevent double bookings.
3. **Medical Report Assistant**: Upload medical reports or paste text to receive a simplified explanation powered by NVIDIA's Generative AI (`meta/llama-3.2-11b-vision-instruct`). Uses custom prompt structures for patient-friendly plain English formatting.

## Architecture
- **Frontend**: Clean, professional, single-page application built with HTML, CSS, and Vanilla JavaScript. Features routing, modals, toast notifications, and responsive design.
- **Backend API**: Flask (Python) exposing RESTful endpoints. 
- **Database**: MongoDB (Atlas) for robust persistence of users, doctors, and appointments.
- **Machine Learning**: `scikit-learn` and `joblib` running inference on a pre-trained model.
- **Generative AI**: NVIDIA NIM APIs for structured medical text/image simplification.

## Folder Structure
```
smart-healthcare-poc/
├── AGENT.md                      # Project development contract
├── README.md                     # This file
├── .gitignore                    # Version control ignores
├── backend/
│   ├── app.py                    # Main Flask application entry
│   ├── config.py                 # Secure configuration loading
│   ├── requirements.txt          # Python dependencies
│   ├── routes/                   # API Route definitions
│   ├── services/                 # Business logic & AI/ML integration
│   ├── database/                 # MongoDB connection
│   └── ml/                       # Stored model (.joblib)
├── frontend/
│   ├── index.html                # Main SPA layout
│   ├── style.css                 # Professional healthcare styling
│   └── script.js                 # Frontend application logic
├── scripts/
│   └── seed_database.py          # Populates MongoDB with doctors
```

## Environment Configuration
The backend safely reads secrets from `secret.txt` located in the root of the workspace.
It expects:
- MongoDB SRV string (or fallback to user/pass)
- NVIDIA API Key (`NVIDIA_API_KEY`)

## How to Install & Run Locally
1. Ensure `secret.txt` is in the parent directory (`R:\zzzzzzzzzzz_Gradious_OA\secret.txt`).
2. Open terminal in the `backend` directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Seed the database (run once):
   ```bash
   python ../scripts/seed_database.py
   ```
5. Start the server:
   ```bash
   python app.py
   ```
6. Open your browser to `http://localhost:5000`.

## Testing the Application (Demo Workflow)
1. **Register**: Create an account on the landing page.
2. **Dashboard**: Navigate to "Find the right specialist".
3. **ML Prediction**: Answer the 10 questions.
4. **Recommendation**: View the ML model's prediction (e.g., Pulmonology).
5. **Booking**: Choose a doctor from the filtered list, pick a time slot, and confirm.
6. **AI Assistant**: Return to the dashboard, open the Medical Assistant, and paste medical text or upload a medical image/PDF.

## Security & Limitations
- Passwords are securely hashed using `bcrypt`.
- Routes are protected via JWT tokens.
- **Medical Disclaimer**: The AI and ML modules are strictly proofs-of-concept. The system explicitly blocks non-medical GenAI queries and displays disclaimers that it is not a diagnostic tool.
