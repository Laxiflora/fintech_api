import requests
import json

url = "https://api.covid19api.com/summary"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

data = json.loads(response.text)
print(data['Global']['NewConfirmed'])
