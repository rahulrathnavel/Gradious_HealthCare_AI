import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from database.db import init_db, get_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

doctors = [
    {
        "name": "Dr. Sarah Jenkins",
        "specialty": "Cardiology",
        "experience": "15 years",
        "bio": "Specializes in preventive cardiology and heart failure.",
        "availability": ["09:00 AM", "10:30 AM", "02:00 PM", "03:30 PM"],
        "active": True
    },
    {
        "name": "Dr. Michael Chen",
        "specialty": "Dermatology",
        "experience": "10 years",
        "bio": "Expert in medical and cosmetic dermatology.",
        "availability": ["10:00 AM", "11:00 AM", "01:00 PM"],
        "active": True
    },
    {
        "name": "Dr. Emily Wong",
        "specialty": "Gastroenterology",
        "experience": "12 years",
        "bio": "Specializes in digestive disorders and endoscopy.",
        "availability": ["08:30 AM", "11:30 AM", "04:00 PM"],
        "active": True
    },
    {
        "name": "Dr. Robert Smith",
        "specialty": "General Medicine",
        "experience": "20 years",
        "bio": "Comprehensive primary care for adults.",
        "availability": ["09:00 AM", "12:00 PM", "02:00 PM", "04:00 PM"],
        "active": True
    },
    {
        "name": "Dr. Linda Davis",
        "specialty": "Neurology",
        "experience": "14 years",
        "bio": "Focuses on headaches, epilepsy, and stroke.",
        "availability": ["10:00 AM", "01:30 PM", "03:00 PM"],
        "active": True
    },
    {
        "name": "Dr. James Wilson",
        "specialty": "Orthopedics",
        "experience": "18 years",
        "bio": "Sports medicine and joint replacement surgery.",
        "availability": ["08:00 AM", "09:30 AM", "02:30 PM"],
        "active": True
    },
    {
        "name": "Dr. Amanda Martinez",
        "specialty": "Pulmonology",
        "experience": "11 years",
        "bio": "Asthma, COPD, and sleep medicine.",
        "availability": ["11:00 AM", "01:00 PM", "03:30 PM"],
        "active": True
    },
    {
        "name": "Dr. William Taylor",
        "specialty": "Urology",
        "experience": "16 years",
        "bio": "Treats urinary tract conditions and men's health.",
        "availability": ["09:00 AM", "10:00 AM", "02:00 PM"],
        "active": True
    },
    {
        "name": "Dr. Richard Roe",
        "specialty": "Cardiology",
        "experience": "8 years",
        "bio": "Focuses on arrhythmias and electrophysiology.",
        "availability": ["10:00 AM", "01:00 PM", "04:00 PM"],
        "active": True
    }
]

def seed():
    logger.info("Initializing database connection...")
    init_db()
    db = get_db()
    
    if db is None:
        logger.error("Could not connect to database. Aborting.")
        return

    logger.info("Clearing existing doctors...")
    db.doctors.delete_many({})

    logger.info("Inserting seed doctors...")
    result = db.doctors.insert_many(doctors)
    
    logger.info(f"Successfully inserted {len(result.inserted_ids)} doctors.")
    logger.info("Database seeding complete.")

if __name__ == "__main__":
    seed()

