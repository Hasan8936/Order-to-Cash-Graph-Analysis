import requests
import json

resp = requests.post(
    'http://127.0.0.1:8000/api/chat',
    json={'message': 'List customers', 'history': []},
    timeout=30
)
print(resp.status_code)
print(resp.text)
