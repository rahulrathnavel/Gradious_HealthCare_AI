# Project Documentation

## 1. Problem Statement
Patients often struggle to identify the correct medical specialist for their specific symptoms, leading to delayed diagnoses, misdirected appointments, and increased anxiety. Additionally, understanding complex medical reports is a significant hurdle for the average patient, making it difficult for them to be informed participants in their own healthcare journey. 

This project aims to solve these issues by building an "AI-Powered Smart Healthcare Appointment & Assistance System". The system intelligently recommends the correct medical specialty based on a patient's symptoms, allows for seamless doctor discovery and appointment booking, and provides an AI-driven medical report simplification tool to empower patients.

## 2. Approach
The solution is built as a complete full-stack web application:
- **Symptom Analysis**: A Machine Learning model (Logistic Regression) was trained on a custom dataset mapping 10 binary symptoms to 8 medical specialties.
- **Doctor Booking**: A robust backend API connected to a MongoDB database handles user registration, doctor filtering by specialty, and atomic appointment booking (preventing double-booking conflicts).
- **Medical Report Assistant**: We integrated NVIDIA's state-of-the-art Generative AI (`meta/llama-3.2-11b-vision-instruct`). It parses uploaded medical text or images and outputs a highly structured, plain-English summary for the patient.

## 3. System Architecture
- **Frontend Layer**: A lightweight, responsive Single Page Application (SPA) built with Vanilla HTML, CSS, and JavaScript. It communicates asynchronously with the backend via RESTful APIs.
- **Backend API Layer**: A Python Flask server that exposes endpoints for Authentication (JWT), Recommendations, Doctor listings, Appointments, and the AI Assistant.
- **Machine Learning Layer**: `scikit-learn` model loaded natively into the Python backend using `joblib` for rapid, in-memory inference.
- **Generative AI Layer**: API integration with NVIDIA NIM endpoints. Prompts are injected server-side to guarantee safe, medical-only responses.
- **Persistence Layer**: MongoDB (Atlas) stores Users (hashed passwords), Doctors, and Appointments.

## 4. Tools Used
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Backend**: Python 3, Flask, PyJWT, bcrypt, Requests
- **Machine Learning**: Pandas, Scikit-Learn, Joblib (Logistic Regression)
- **Generative AI**: NVIDIA LLM API (`meta/llama-3.2-11b-vision-instruct`)
- **Database**: MongoDB (Atlas), PyMongo
- **Version Control**: Git, GitHub
