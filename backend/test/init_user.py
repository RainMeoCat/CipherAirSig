from matplotlib.font_manager import json_load
import requests
import random
import json
import hashlib
with open('./user_info.json', 'r') as f:
    user = json.loads(f.read())

for k, v in user.items():
    url = 'http://127.0.0.1:5000/api/user/register'
    pwd = hashlib.sha256(b"test").hexdigest()
    
    body = {
        "uuid": v["UUID"],
        "account": v["email"],
        "user_name": v["user_name"],
        "email": v["email"],
        "age": v["age"],
        "gender": v["gender"],
        "password": pwd}

    print(body)
    x = requests.post(url, json=body)
    print(x.status_code)
