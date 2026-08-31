import os
import re

def load_secrets(file_path):
    secrets = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, val = line.split('=', 1)
                    secrets[key.strip()] = val.strip()
    return secrets

SECRET_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'secret.txt'))
secrets = load_secrets(SECRET_FILE_PATH)

# Build MongoDB URI
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    base_uri = secrets.get('SRV Connection String', '')
    username = secrets.get('mongodb_username', 'Gradious')
    password = secrets.get('mongodb_password', 'Gradious')
    
    if base_uri:
        # replace whitelegend008_db_user:<db_password> or similar with credentials
        MONGO_URI = re.sub(r'://.*?@', f'://{username}:{password}@', base_uri)
    else:
        # Fallback
        MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.i6uvmfn.mongodb.net/smart_healthcare?retryWrites=true&w=majority"

# Make sure we use a specific database name
if '/?' in MONGO_URI:
    MONGO_URI = MONGO_URI.replace('/?', '/smart_healthcare?')

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", secrets.get("NVIDIA_API_KEY"))
NVIDIA_MODEL = os.environ.get("NVIDIA_MODEL", secrets.get("model_name", "meta/llama-3.2-11b-vision-instruct"))

JWT_SECRET = os.environ.get("JWT_SECRET", "super-secret-jwt-key-replace-in-prod")

