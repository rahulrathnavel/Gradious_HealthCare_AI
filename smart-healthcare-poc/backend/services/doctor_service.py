from database.db import get_db
from bson.objectid import ObjectId

class DoctorService:
    @staticmethod
    def get_doctors_by_specialty(specialty: str = None):
        db = get_db()
        if db is None:
            raise Exception("Database unavailable")
            
        query = {}
        if specialty:
            query['specialty'] = specialty
            
        doctors = list(db.doctors.find(query))
        
        # Serialize ObjectIds
        for doc in doctors:
            doc['_id'] = str(doc['_id'])
            
        return doctors

    @staticmethod
    def get_doctor_by_id(doctor_id: str):
        db = get_db()
        if db is None:
            raise Exception("Database unavailable")
            
        try:
            doctor = db.doctors.find_one({"_id": ObjectId(doctor_id)})
            if doctor:
                doctor['_id'] = str(doctor['_id'])
            return doctor
        except:
            return None

