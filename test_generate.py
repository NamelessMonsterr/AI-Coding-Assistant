import requests
import json

body = {
    "prompt": "Create a Python function to calculate factorial",
    "language": "python",
    "temperature": 0.2,
    "max_tokens": 1000
}

try:
    r = requests.post('http://localhost:8000/api/v1/generate', json=body)
    print('Status:', r.status_code)
    print('Response:', json.dumps(r.json(), indent=2))
except Exception as e:
    print('Error:', e)