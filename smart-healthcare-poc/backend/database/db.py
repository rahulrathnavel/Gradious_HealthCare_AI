from pymongo import MongoClient
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = None
db = None

def init_db():
    global client, db
    try:
        client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)
        # Attempt to fetch server info to verify connection
        client.server_info() 
        db = client.get_database() # Uses the DB in the URI (smart_healthcare)
        logger.info("Successfully connected to MongoDB.")
        
        # Create indexes safely
        db.users.create_index("email", unique=True)
        db.doctors.create_index("specialty")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        db = None
        return False

def get_db():
    global db
    if db is None:
        logger.info("Attempting to reconnect to MongoDB...")
        init_db()
    return db
