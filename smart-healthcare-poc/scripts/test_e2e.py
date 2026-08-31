import requests

BASE_URL = "http://localhost:5000/api"

print("1. Testing Registration...")
res = requests.post(f"{BASE_URL}/auth/register", json={
    "name": "Test Patient",
    "email": "test@example.com",
    "password": "password123"
})
if res.status_code == 400 and "already registered" in res.text:
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
print(res.json())
token = res.json()['data']['token']
headers = {"Authorization": f"Bearer {token}"}

print("\n2. Testing ML Recommendation...")
res = requests.post(f"{BASE_URL}/recommendations", headers=headers, json={
    "fever": 0, "cough": 1, "breathlessness": 1, "chest_pain": 0,
    "headache": 0, "digestive_problem": 0, "joint_or_muscle_problem": 0,
    "skin_problem": 0, "urinary_problem": 0, "fatigue": 1
})
print(res.json())
specialty = res.json()['data']['recommended_specialty']

print(f"\n3. Testing Doctor Discovery ({specialty})...")
res = requests.get(f"{BASE_URL}/doctors?specialty={specialty}", headers=headers)
doctors = res.json()['data']
print(f"Found {len(doctors)} doctors")

if doctors:
    doctor = doctors[0]
    print(f"\n4. Testing Booking with {doctor['name']}...")
    res = requests.post(f"{BASE_URL}/appointments", headers=headers, json={
        "doctor_id": doctor['_id'],
        "date": "2026-09-01",
        "time": doctor['availability'][0],
        "patient_name": "Test Patient"
    })
    print(res.json())

print("\n5. Testing AI Assistant...")
res = requests.post(f"{BASE_URL}/medical-assistant/analyze", headers=headers, json={
    "text": "The patient shows signs of mild tachycardia and elevated blood pressure."
})
print(res.json())

print("\nAll tests completed!")

