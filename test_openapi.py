import urllib.request
import json

req = urllib.request.Request('http://127.0.0.1:8000/api/v1/openapi.json')
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(list(data['paths'].keys()))
except Exception as e:
    print(e)
