from dtaidistance import dtw
from scipy import stats
import numpy as np
import json 
import os
import re
from natsort import natsorted
from dtaidistance import dtw_ndim
# 手勢密碼檢查
def pinch_check(sign, template_list):
    PINCH_RANK = {
        "index": 0.1,
        "middle": 0.2,
        "ring":  0.3,
        "pinky": 0.4
    }
    pinch_signal = []
    check_count = 0
    data = sign
    for i in range(len(data)):
        pinch_signal.extend([PINCH_RANK[data[i]['pinch']]] * int(20 * ((data[i]['end_time'] - data[i]['start_time']) / 1000)))
        if i != len(data) -1:
            pinch_signal.extend([0] * int(20 * ((data[i+1]['start_time'] - data[i]['end_time']) / 1000)))
    for i in range(len(template_list)):
        template_temp = []
        for j in range(len(template_list[i])):
            template_temp.extend([PINCH_RANK[template_list[i][j]['pinch']]] * int(20 * ((template_list[i][j]['end_time'] - template_list[i][j]['start_time']) / 1000)))
            if j != len(template_list[i]) -1:
                template_temp.extend([0] * int(20 * ((template_list[i][j+1]['start_time'] - template_list[i][j]['end_time']) / 1000)))
        template_list[i]=template_temp
    for template in template_list:
        distance = dtw.distance(pinch_signal, template)
        if(distance == 0):
            check_count=check_count + 1
    if(check_count == 5):
        return True
    else:
        return False

# 簽名圖形筆跡檢查
def graph_check(sign, template_list, dist):
    sign_x = []
    sign_y = []
    for j in sign:
        sign_x.extend([k[0] for k in j['line']])
        sign_y.extend([k[1] for k in j['line']])
    series1 = stats.zscore(np.array(list(zip(sign_x, sign_y)), dtype=np.double))
    sign_x_list = []
    sign_y_list = []
    check_count = 0
    for i in range(len(template_list)):
        data = template_list[i]
        sign_x = []
        sign_y = []
        for j in data:
            sign_x.extend([k[0] for k in j['line']])
            sign_y.extend([k[1] for k in j['line']])
        sign_x_list.append(sign_x)
        sign_y_list.append(sign_y)
    for j in range(5):
        series2 = stats.zscore(np.array(list(zip(sign_x_list[j], sign_y_list[j])), dtype=np.double))
        d = dtw_ndim.distance(series1, series2, window=15)
        if(d<float(dist)):
            check_count = check_count+1
        # print('簽名' + str(i + 1) + ' vs 簽名' + str(j + 1) + ': '+str(d))
    return check_count >= 4

def sign_validate(sign, id):
    file_path = './app/gesturesign/DB/' +str(id) + '/template/' 
    template_list = [None] * 5
    files = [f for f in os.listdir(file_path) if os.path.isfile(file_path+f)]
    r = re.compile('(' + str(id) +').*(.json)')
    file_list =  natsorted(list(filter(r.match, files)))
    #以全部簽名的名單載入json簽名檔並予以取代
    for i in range(len(template_list)):
        with open(file_path + file_list[i]) as json_file:
            template_list[i] = json.load(json_file)
            
    with open('./app/gesturesign/DB/' +str(id) + '/template/dist.txt') as dist_file:
        sign_info = dist_file.read().splitlines()
    if(not pinch_check(sign, list(template_list))):
        return False, 'pinch'
    if(not graph_check(sign, list(template_list), sign_info[0])):
        return False, 'graph'
    return True, 'pass'
