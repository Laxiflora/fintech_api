import requests
import json
import jwt
import time
url = 'http://127.0.0.1:5000/users'
payload ="""
    {
\"user_id\":\"1000\"
    }
"""
valid_token = jwt.encode(
        {
        'user_id':'1000',
        'timestamp':int(time.time())
        },
        'password',algorithm='HS256').decode('utf-8')


headers ={
#    'auth':valid_token,
    'Content-Type':'application/json'
}

response = requests.request("GET",url,headers=headers,data=payload)
print(response.text)
