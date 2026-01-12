"""Simple signup test"""
import requests
import json

url = "http://localhost:8000/api/auth/sign-up/email"
payload = {
    "email": "test123@example.com",
    "password": "TestPassword123!"
}

print(f"Testing signup endpoint: {url}")
print(f"Payload: {json.dumps(payload)}")

try:
    response = requests.post(url, json=payload)
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {str(e)}")
