from flask import Blueprint, request, jsonify
from routes.middleware import token_required
from services.recommendation_service import recommendation_service
from services.doctor_service import DoctorService
from services.appointment_service import AppointmentService
from services.medical_ai_service import MedicalAIService
import base64
import filetype

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"success": True, "status": "ok"})

@api_bp.route('/recommendations', methods=['POST'])
@token_required
def recommend(current_user_id):
    data = request.json
    if not data:
        return jsonify({"success": False, "error": {"message": "No data provided"}}), 400
        
    try:
        result = recommendation_service.predict_specialty(data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": {"message": str(e)}}), 500

@api_bp.route('/doctors', methods=['GET'])
@token_required
def get_doctors(current_user_id):
    specialty = request.args.get('specialty')
    try:
        doctors = DoctorService.get_doctors_by_specialty(specialty)
        return jsonify({"success": True, "data": doctors})
    except Exception as e:
        return jsonify({"success": False, "error": {"message": str(e)}}), 500

@api_bp.route('/appointments', methods=['POST'])
@token_required
def book_appointment(current_user_id):
    data = request.json
    doctor_id = data.get('doctor_id')
    date = data.get('date')
    time = data.get('time')
    patient_name = data.get('patient_name')
    notes = data.get('notes', '')

    if not all([doctor_id, date, time, patient_name]):
        return jsonify({"success": False, "error": {"message": "Missing required fields"}}), 400

    try:
        appointment = AppointmentService.create_appointment(
            user_id=current_user_id,
            doctor_id=doctor_id,
            date=date,
            time=time,
            patient_name=patient_name,
            notes=notes
        )
        return jsonify({"success": True, "data": appointment}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": {"message": str(e)}}), 400
    except Exception as e:
        return jsonify({"success": False, "error": {"message": str(e)}}), 500

@api_bp.route('/appointments', methods=['GET'])
@token_required
def get_appointments(current_user_id):
    try:
        appointments = AppointmentService.get_user_appointments(current_user_id)
        return jsonify({"success": True, "data": appointments})
    except Exception as e:
        return jsonify({"success": False, "error": {"message": str(e)}}), 500

@api_bp.route('/medical-assistant/analyze', methods=['POST'])
@token_required
def analyze_content(current_user_id):
    # Handle both multipart form data (files) and JSON (text)
    text = None
    image_b64 = None
    mime_type = "image/jpeg"
    
    if request.is_json:
        text = request.json.get('text')
    else:
        text = request.form.get('text')
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file_bytes = file.read()
                kind = filetype.guess(file_bytes)
                if not kind or not kind.mime.startswith('image/'):
                    return jsonify({"success": False, "error": {"message": "Invalid file type. Only images are supported currently."}}), 400
                
                mime_type = kind.mime
                image_b64 = base64.b64encode(file_bytes).decode('utf-8')
                
                # Check size (e.g. 5MB)
                if len(file_bytes) > 5 * 1024 * 1024:
                    return jsonify({"success": False, "error": {"message": "File too large. Max 5MB."}}), 400
                    
    if not text and not image_b64:
        return jsonify({"success": False, "error": {"message": "Please provide text or an image"}}), 400

    try:
        result_text = MedicalAIService.analyze_medical_content(text=text, image_b64=image_b64, mime_type=mime_type)
        return jsonify({"success": True, "data": {"analysis": result_text}})
    except Exception as e:
        return jsonify({"success": False, "error": {"message": str(e)}}), 500

