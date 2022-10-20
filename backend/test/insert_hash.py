import tqdm
import json
import requests
import random


def random_hex(size):
    bitList = []

    for i in range(0, size):
        x = str(random.randint(0, 1))
        bitList.append(x)
    bitString = ''.join(bitList)
    # print(bitString)
    return (int(bitString, 2))


for i in tqdm.tqdm(range(0, 100)):
    url = 'http://127.0.0.1:5000/api/airsign/insert'
    #url = 'http://bas.shiya.site/api/airsign/insert'
    body = {
        "account_id": random.randrange(30),
        "hash_0": random_hex(size=16),
        "symbol_code": random.randrange(10)
    }
    # print(body)
    x = requests.post(url, json=body)
