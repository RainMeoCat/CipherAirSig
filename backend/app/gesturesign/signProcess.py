import json
from scipy.spatial import distance
import re
import os
import argparse
import numpy as np
import scipy.interpolate as interpolate
# from natsort import natsorted
#設定執行參數
parser=argparse.ArgumentParser()
parser.add_argument('--id', help='轉換id,輸入all就會全部一起轉換')
parser.add_argument('--action', help='是否進入修復程序')
args=parser.parse_args()


# threshold

# # 指標：是否一起轉換
# # PROCESS_ALL = args.id=='all'
# # if(not PROCESS_ALL):
# #     TARGET_ID = args.id
# # with open('fix_table.json') as json_file:
# #             fix_table = json.load(json_file)
# # #捏指距離閾值
# # threshold = fix_table['thresholds'][int(args.id)]
# # #修復列表，如果裡面有需要修復的索引，代表有簽名需要修復
# # fix_list = fix_table['fix_table'][int(args.id)]['fix_list']
# # #接合列表，接合筆劃之用
# # join_strokes= fix_table['fix_table'][int(args.id)]['join_strokes']
# # #筆劃刪除列表
# # drop_strokes= fix_table['fix_table'][int(args.id)]['drop_strokes']
# # #簽名的平滑化參數
# # smooth_vals= fix_table['smooth_vals'][int(args.id)]
# #簽名開始時間，給
# #回傳大拇指相對於四隻手指的相對距離
# #使用的index參照mediapipe的手部關節index文件

def return_distances(res):
    # 大拇指X,Y,Z
    X=res[4]['x']
    Y=res[4]['y']
    Z=res[4]['z']
    INDEX_X = res[8]['x']
    INDEX_Y = res[8]['y']
    INDEX_Z = res[8]['z']
    MIDDLE_X = res[12]['x']
    MIDDLE_Y = res[12]['y']
    MIDDLE_Z = res[12]['z']
    RING_X = res[16]['x']
    RING_Y = res[16]['y']
    RING_Z = res[16]['z']
    PINKY_X = res[20]['x']
    PINKY_Y = res[20]['y']
    PINKY_Z = res[20]['z']
    # 以WRIST與食指的距離作為大小，縮放距離為相對距離
    WRIST_X = res[0]['x']
    WRIST_Y = res[0]['y']
    WRIST_Z = res[0]['z']
    INDEX_MCP_X = res[5]['x']
    INDEX_MCP_Y = res[5]['y']
    INDEX_MCP_Z = res[5]['z']
    HAND_SIZE = round(distance.euclidean((WRIST_X, WRIST_Y, WRIST_Z), (INDEX_MCP_X,INDEX_MCP_Y,INDEX_MCP_Z)),2)
    return {
        "index": round(distance.euclidean((X, Y), (INDEX_X,INDEX_Y))/HAND_SIZE,2),
        "middle": round(distance.euclidean((X, Y), (MIDDLE_X,MIDDLE_Y))/HAND_SIZE,2),
        "ring": round(distance.euclidean((X, Y), (RING_X,RING_Y))/HAND_SIZE,2),
        "pinky": round(distance.euclidean((X, Y), (PINKY_X,PINKY_Y))/HAND_SIZE,2)
    }

def process_sign(hand_series,hand_index,threshold):
    processed_sign = [{
                        "line": [],
                        "time_series": [],
                        "pinch": "",
                        #start_time 固定
                        "start_time": 0,
                        "end_time": 0
                    }]
    # 線條數量指標
    stroke_indicator = 0
    # 下筆指標
    writing = False
    # 間隔暫用，用於以單個簽名為單位的間隔
    intervals=[]
    # 遍歷手掌距離list
    for j in hand_series:
        # 取得距離
        dist = return_distances(j['landmark'])
        for index,key in enumerate(dist):
            # 這裡判斷捏指達到最小距離時下筆的行為
            # 初次正規化後使用的最小距離為threshold
            if(dist[key]<float(threshold)):
                # 算法參照mediapipe文件，四指手指固定的index間隔
                X=j['landmark'][8+(index)*4]['x']
                Y=j['landmark'][8+(index)*4]['y']
                processed_sign[stroke_indicator]["line"].append((X,Y))
                processed_sign[stroke_indicator]["time_series"].append(j['unix_time'])
                processed_sign[stroke_indicator]["pinch"] = key
                if(processed_sign[stroke_indicator]["start_time"] == 0):
                    processed_sign[stroke_indicator]["start_time"] = j['unix_time']
                processed_sign[stroke_indicator]["end_time"]= j['unix_time']
                # writing能夠讓線條不間斷，同時在提筆的時候，如果不間斷為true，代表需要提筆，線條新增至list
                writing = True
                # 處理提筆間隔
                intervals.append(True)
            if min(dist.values())>float(threshold) and writing == True:
                # 這裡儲存現在正在第幾條線
                # 斷開線條之後就可以將第幾條線的指標+1，存入簽名列表
                # 並新增一個新的線條dict
                stroke_indicator += 1
                processed_sign.append({
                        "line": [],
                        "time_series": [],
                        "pinch": "",
                        "start_time": 0,
                        "end_time": 0
                        })
                writing = False
                # 處理提筆間隔
                intervals.append(False)
            elif(min(dist.values())>float(threshold)):
                # 處理提筆間隔，此處解決線條間只有一個false的錯誤
                intervals.append(False)
    # ❗❗❗如果簽名時是以下筆的狀態結束簽名，執行這次pop會丟失一條線條，需要修正❗❗❗
    # 反之，如果是以提筆的狀態結束簽名，最後一筆將會多出一組空的線條dict，pop掉
    if(processed_sign[len(processed_sign)-1] == {"line": [],"time_series": [],"pinch": "","start_time": 0,"end_time": 0}):
        processed_sign.pop()
    # 正規化和因應camera的影像翻轉
    for i in range(len(processed_sign)):
        processed_sign[i]={'line' : [(abs(j[0]-1), j[1]) for j in processed_sign[i]['line']],
        "time_series": processed_sign[i]['time_series'],
        'pinch':processed_sign[i]['pinch'],
        "start_time": processed_sign[i]['start_time'],
        "end_time": processed_sign[i]['end_time']}
    return processed_sign,intervals


def convert(landmark, id):
    sign_info = []
    with open('./app/gesturesign/DB/' +str(id) + '/template/dist.txt') as dist_file:
        sign_info = dist_file.read().splitlines()
    sign_list_processed = []
    intervals_data = []
    sign_list_processed,intervals_data = process_sign(landmark,0,sign_info[1])
    return sign_list_processed

if __name__ == '__main__':
    original_sign = {}
    with open('test_2.json') as json_file:
        original_sign  = json.load(json_file)
    converted = convert(original_sign, 2)
    # with open('test_output.json', "w") as json_file:
    #     json.dump(converted, json_file)
    # print(original_sign)
