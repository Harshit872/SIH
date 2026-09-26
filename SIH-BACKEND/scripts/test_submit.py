import urllib.request
import json
import os

base_url = "http://localhost:8000/api/v1"

# 1. Login to get token
login_data = json.dumps({"username": "harshit.sachan@example.com", "password": "password123"}).encode('utf-8')
req = urllib.request.Request(f"{base_url}/auth/login", data=login_data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as res:
        token = json.loads(res.read().decode())['access_token']
except Exception as e:
    signup_data = json.dumps({
        "first_name": "Test", "last_name": "User", "email": "test@test.com", "password": "password123"
    }).encode('utf-8')
    try:
        urllib.request.urlopen(urllib.request.Request(f"{base_url}/auth/signup", data=signup_data, headers={'Content-Type': 'application/json'}))
    except: pass
    login_data = json.dumps({"username": "test@test.com", "password": "password123"}).encode('utf-8')
    with urllib.request.urlopen(urllib.request.Request(f"{base_url}/auth/login", data=login_data, headers={'Content-Type': 'application/json'})) as res:
        token = json.loads(res.read().decode())['access_token']

url = f"{base_url}/voyage/submit"
payload = {
    "origin": "Gladstone",
    "destination": "West Australia",
    "commodity": "Iron Ore",
    "cargoMt": 56789,
    "deliveryDate": "2026-10-15",
    "contract": "Bareboat Charter",
    "laycan": "21 Oct 2026 - 27 Oct 2026",
    "noOfVoyages": 2
}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})

try:
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        print(json.dumps(json.loads(response.read().decode()), indent=2))
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code)
    print(e.read().decode())
