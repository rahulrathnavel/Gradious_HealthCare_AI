from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from database.db import init_db
from routes.auth_routes import auth_bp
from routes.api_routes import api_bp
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)  # Enable CORS for all routes if testing externally

# Initialize Database
init_db()

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

# Frontend Serving Routes
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Catch-all for SPA routes to index.html or static files
@app.route('/<path:path>')
def static_proxy(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# Error Handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": {"message": "Endpoint not found"}}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Smart Healthcare Application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
