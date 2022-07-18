import requests
import random


def random_hex(size=64):
    bitList = []

    for i in range(0, size):
        x = str(random.randint(0, 1))
        bitList.append(x)
    bitString = ''.join(bitList)
    # print(bitString)
    return (int(bitString, 2))


for i in range(0, 86000):
    url = 'http://127.0.0.1:5000/airsign/insert'
    body = {
        "account_id": random.randrange(30),
        "hash_0": random_hex(),

    }
    print(body)
    x = requests.post(url, json=body)
