import requests
import json

url = "http://localhost:5000/predict"

payload = {
    "fever": 0,
    "cough": 1,
    "breathlessness": 1,
    "chest_pain": 0,
    "headache": 0,
    "digestive_problem": 0,
    "joint_or_muscle_problem": 0,
    "skin_problem": 0,
    "urinary_problem": 0,
    "fatigue": 1
}

headers = {
    "Content-Type": "application/json"
}

print("Sending request to:", url)
print("Payload:")
print(json.dumps(payload, indent=2))
print("-" * 40)

try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    
    if response.status_code == 200:
        data = response.json()
        print("\nTop Recommendation:")
        print(f"  {data['recommended_specialty']}")
        
        print("\nTop 3 Specialties:")
        for idx, match in enumerate(data['top_matches']):
            print(f"  {idx + 1}. {match['specialty']} ({match['probability']:.2%})")
    else:
        print("Error Response:")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("Failed to connect. Make sure the backend server is running on http://localhost:5000")

