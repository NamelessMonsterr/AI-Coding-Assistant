import requests

# Test /docs
try:
    r = requests.get('http://localhost:8000/docs')
    print('/docs Status:', r.status_code)
    print('/docs Content-Type:', r.headers.get('content-type', 'unknown'))
    print('/docs Length:', len(r.text))
except Exception as e:
    print('/docs Error:', e)

# Test /redoc
try:
    r = requests.get('http://localhost:8000/redoc')
    print('/redoc Status:', r.status_code)
    print('/redoc Content-Type:', r.headers.get('content-type', 'unknown'))
    print('/redoc Length:', len(r.text))
except Exception as e:
    print('/redoc Error:', e)