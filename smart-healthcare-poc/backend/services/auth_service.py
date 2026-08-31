import bcrypt
import jwt
import datetime
from database.db import get_db
from bson.objectid import ObjectId
import config

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def generate_token(user_id: str, email: str) -> str:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id,
            'email': email
        }
        return jwt.encode(payload, config.JWT_SECRET, algorithm='HS256')

    @staticmethod
    def register_user(name: str, email: str, password: str):
        db = get_db()
        if db is None:
            raise Exception("Database unavailable")
            
        existing_user = db.users.find_one({"email": email})
        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = AuthService.hash_password(password)
        
        user_doc = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.datetime.utcnow()
        }
        
        result = db.users.insert_one(user_doc)
        return str(result.inserted_id)

    @staticmethod
    def login_user(email: str, password: str):
        db = get_db()
        if db is None:
            raise Exception("Database unavailable")
            
        user = db.users.find_one({"email": email})
        if not user:
            raise ValueError("Invalid email or password")

        if not AuthService.check_password(password, user["password"]):
            raise ValueError("Invalid email or password")

        token = AuthService.generate_token(str(user["_id"]), email)
        
        return {
            "token": token,
            "user": {
                "id": str(user["_id"]),
                "name": user.get("name"),
                "email": email
            }
        }

