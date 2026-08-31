from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"success": False, "error": {"message": "Name, email, and password are required"}}), 400

    try:
        user_id = AuthService.register_user(name, email, password)
        # Auto-login after register
        auth_data = AuthService.login_user(email, password)
        return jsonify({
            "success": True, 
            "data": auth_data
        }), 201
    except ValueError as e:
        return jsonify({"success": False, "error": {"message": str(e)}}), 400
    except Exception as e:
        return jsonify({"success": False, "error": {"message": "Internal server error"}}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"success": False, "error": {"message": "Email and password are required"}}), 400

    try:
        auth_data = AuthService.login_user(email, password)
        return jsonify({
            "success": True,
            "data": auth_data
        }), 200
    except ValueError as e:
        return jsonify({"success": False, "error": {"message": str(e)}}), 401
    except Exception as e:
        return jsonify({"success": False, "error": {"message": "Internal server error"}}), 500

