import urllib.request
import json

base_url = "http://localhost:8000/api/v1"

# 1. Login to get token
login_data = json.dumps({"username": "harshit.sachan@example.com", "password": "password123"}).encode('utf-8')
login_req = urllib.request.Request(f"{base_url}/auth/login", data=login_data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(login_req) as response:
        token = json.loads(response.read().decode())['access_token']
except Exception as e:
    # try signing up
    signup_data = json.dumps({
        "first_name": "Test", "last_name": "User", "email": "test@test.com", "password": "password123"
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(f"{base_url}/auth/signup", data=signup_data, headers={'Content-Type': 'application/json'}))
    login_data = json.dumps({"username": "test@test.com", "password": "password123"}).encode('utf-8')
    with urllib.request.urlopen(urllib.request.Request(f"{base_url}/auth/login", data=login_data, headers={'Content-Type': 'application/json'})) as res:
        token = json.loads(res.read().decode())['access_token']

url = f"{base_url}/evaluate_scenarios"
payload = {
    "origin": "Dampier",
    "destination": "Paradip",
    "commodity": "Coal",
    "cargoMt": 80000,
    "deliveryDate": "2026-10-15",
    "contract": "Voyage Charter",
    "laycan": "01 Oct 2026 - 10 Oct 2026",
    "noOfVoyages": 1
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
