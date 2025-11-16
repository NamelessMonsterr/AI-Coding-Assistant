import requests

try:
    r = requests.get('http://localhost:8000/api/v1/models')
    print('Status:', r.status_code)
    print('Response:', r.json())
except Exception as e:
    print('Error:', e)