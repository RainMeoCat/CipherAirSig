import numpy as np
import time
from pylepton import Lepton
import requests
import json
import cv2
url = 'http://bas.shiya.site/api/lepton/raw_insert'
with Lepton() as l:
    while 1:
        stime = time.time()
        a, _ = l.capture(log_time=False, debug_print=False)

        raw_img = np.divide(a, 100)-273.5
        img = np.reshape(raw_img, (60, 80))
        out = img.tolist()
        body = {
            "raw_data": json.dumps(out)}
        #x = requests.post(url, json=body)
        # print(time.time()-stime,x.status_code)
        cv2.imshow('123', img)
        cv2.waitKey(1)
        # time.sleep(0.5)
