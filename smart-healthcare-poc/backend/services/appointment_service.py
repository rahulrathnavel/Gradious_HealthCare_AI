from database.db import get_db
from bson.objectid import ObjectId
import datetime
from pymongo.errors import DuplicateKeyError

class AppointmentService:
    @staticmethod
    def create_appointment(user_id: str, doctor_id: str, date: str, time: str, patient_name: str, notes: str):
        db = get_db()
        if db is None:
            raise Exception("Database unavailable")

        # Verify doctor exists
        doctor = db.doctors.find_one({"_id": ObjectId(doctor_id)})
        if not doctor:
            raise ValueError("Doctor not found")

        # Check if the user already has an appointment at this exact date and time
        user_conflict = db.appointments.find_one({
            "user_id": user_id,
            "date": date,
            "time": time,
            "status": {"$ne": "cancelled"}
        })
        
        if user_conflict:
            raise ValueError("You have already booked an appointment at this time. Kindly book at a different time or date.")

        # Check for doctor conflicts (double booking for the same doctor at the same date/time)
        doctor_conflict = db.appointments.find_one({
            "doctor_id": doctor_id,
            "date": date,
            "time": time,
            "status": {"$ne": "cancelled"}
        })
        
        if doctor_conflict:
            raise ValueError("This time slot is no longer available. Please choose another slot.")

        # Create appointment atomically
        appointment = {
            "user_id": user_id,
            "doctor_id": doctor_id,
            "doctor_name": doctor["name"],
            "specialty": doctor["specialty"],
            "patient_name": patient_name,
            "date": date,
            "time": time,
            "notes": notes,
            "status": "confirmed",
            "created_at": datetime.datetime.utcnow()
        }
        
        result = db.appointments.insert_one(appointment)
        appointment["_id"] = str(result.inserted_id)
        return appointment

    @staticmethod
    def get_user_appointments(user_id: str):
        db = get_db()
        if db is None:
            raise Exception("Database unavailable")
            
        appointments = list(db.appointments.find({"user_id": user_id}).sort("date", 1))
        
        for appt in appointments:
            appt['_id'] = str(appt['_id'])
            
        return appointments

