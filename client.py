
import requests


r = requests.get('127.0.0.1:8888',)

data = r.json()

print(data)
