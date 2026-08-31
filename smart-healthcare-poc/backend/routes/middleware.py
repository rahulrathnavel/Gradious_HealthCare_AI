from functools import wraps
from flask import request, jsonify
import jwt
import config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
        if not token:
            return jsonify({
                "success": False,
                "error": {"message": "Authentication token is missing"}
            }), 401
            
        try:
            data = jwt.decode(token, config.JWT_SECRET, algorithms=['HS256'])
            current_user_id = data['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({
                "success": False,
                "error": {"message": "Token has expired"}
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                "success": False,
                "error": {"message": "Invalid token"}
            }), 401
            
        return f(current_user_id, *args, **kwargs)
        
    return decorated

