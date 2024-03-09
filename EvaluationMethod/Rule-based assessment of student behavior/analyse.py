'''
python analyse.py \
    --csvs_path /root/autodl-nas/multi_model_fusion/multi_merge \
    --focus_path /root/autodl-nas/multi_model_fusion/focus \

'''

import argparse
import csv
import numpy as np
import pandas as pd
import os
import math
import difflib

parser = argparse.ArgumentParser()
parser.add_argument('--csvs_path', default='/root/autodl-nas/multi_model_fusion/multi_merge',type=str)
parser.add_argument('--focus_path', default='/root/autodl-nas/multi_model_fusion/focus',type=str)

arg = parser.parse_args()
csvs_path = arg.csvs_path
focus_path = arg.focus_path


focus_summary_csv_path = os.path.join(focus_path, 'focus_summary.csv')

if not os.path.exists(focus_summary_csv_path):
    os.system(f"mkdir -p {focus_path}")
    os.system(f"touch {focus_summary_csv_path}")
else:
    os.system(f"rm -rf {focus_path}")
    os.system(f"mkdir -p {focus_path}")
    os.system(f"touch {focus_summary_csv_path}")

'''
1 
若行为序列匹配相似度>=0.75，
学生行为序列所代表的专注水平按专家规则选取；
若判断该条序列代表高专注水平，
则高专注水平序列持续时长为该序列的长度，
那么相应的低专注水平序列持续时长为0秒；
反之，亦然。



2 
若行为序列匹配相似度<0.75，
学生行为序列所代表的的专注水平定义为低专注，
则低专注水平序列持续时长为该序列的长度，
那么高专注水平序列持续时长为0秒。

'''

with open(focus_summary_csv_path,"a+") as csvfile: 
    writer = csv.writer(csvfile)
    writer.writerow(["file_name", # 
                     "behavior_sequence_orig" , # 学生行为动作原始序列（家长除外）
                     "behavior_sequence_merg", # 学生行为动作合并序列（家长除外）
                     "behavior_best_match_sequence", # 学生行为动作序列匹配相似度
                     "behavior_sequence_match_similarity", # 
                     "behavior_sequence_concentration_index",  # 学生行为序列代表的专注水平，1-高专注、0-低专注
                     "high_concentration_time", # 高专注水平的学生行为序列持续时长，秒（s）
                     "low_concentration_time", # 低专注水平的学生行为序列持续时长，秒（s）
                     "anger_time",  # 生气情感持续时长
                     "disgust_time", # 厌倦情感持续时长
                     "fear_time",  # 害怕情感持续时长
                     "happiness_time", # 开心情感持续时长
                     "sadness_time", # 悲伤情感持续时长
                     "surprise_time",  # 惊讶情感持续时长
                     "high_concentration_count" , # 是头部姿态高专注次数
                     "low_concentration_count", # 是头部姿态低专注次数
                     ])

behavior_all_times = {0:0, 1:0, 2:0, 3:0, 4:0} 
behavior_max_times = {0:0, 1:0, 2:0, 3:0, 4:0} 
behavior_min_times = {0:10000, 1:10000, 2:10000, 3:10000, 4:10000} 
for csv_file in os.listdir(csvs_path):
    if "checkpoint" in csv_file:
        continue
    csv_file_path = os.path.join(csvs_path, csv_file)
    csv_file_PD = pd.read_csv(csv_file_path)
    
    video_frame_IDs = csv_file_PD["video_frame_ID"]
    
    studentParents_ID = csv_file_PD["studentParents_ID"]
    
    headPose_yaw = csv_file_PD["headPose_yaw"]
    headPose_pitch = csv_file_PD["headPose_pitch"]
    headPose_roll = csv_file_PD["headPose_roll"]
    
    behavior_ID = csv_file_PD["behavior_ID"]
    behavior_conf = csv_file_PD["behavior_conf"]
    
    face_ID = csv_file_PD["face_ID"]
    
    focus_csv_path = os.path.join(focus_path, csv_file)
    
    if not os.path.exists(focus_csv_path):
        os.system(f"mkdir -p {focus_path}")
        os.system(f"touch {focus_csv_path}")
    else:
        os.system(f"rm -rf {focus_path}")
        os.system(f"mkdir -p {focus_path}")
        os.system(f"touch {focus_csv_path}")
        
        
    with open(focus_csv_path,"a+") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["video_frame_ID", "headPose_focus", "face_ID", "behavior_ID", "behavior_conf"])
    
    behavior_sequence_orig = []
    behavior_sequence_merg = []
    
    behavior_times = {0:[], 1:[], 2:[], 3:[], 4:[]} 
    behavior_time_temp = 0
    behavior_pre = ''
    
    # filter_face_ID 是筛选出学生的face_ID
    filter_face_ID = []
    
    # headPose_focus是统计学生专注与非专注
    filter_headPose_focus = []
    
    for index, video_frame_ID in enumerate(video_frame_IDs):

        csvRow = np.array([video_frame_ID])

        if studentParents_ID[index] == 0.0 :
            
            filter_face_ID.append(face_ID[index])
            
            # 头部姿态专注度判断
            # 0 代表 低专注度
            # 1 代表 高专注度
            headPose_focus = 0
            if headPose_yaw[index] >= -60 and headPose_yaw[index] <= 10:
                if headPose_pitch[index] >= -40 and headPose_pitch[index] <= 40:
                    if headPose_roll[index] >= -30 and headPose_roll[index] <= 30:
                        headPose_focus = 1
                        csvRow = np.append( csvRow, np.array([1]) )
            if headPose_focus == 0:
                csvRow = np.append( csvRow, np.array([0]) )
                
            filter_headPose_focus.append(headPose_focus)
            
            # 面部表情统计
            try:
                csvRow = np.append( csvRow, np.array([ int(face_ID[index]) ] ) )
            except:
                csvRow = np.append( csvRow, np.array([-1]) )
                                    
            # 行为统计
            csvRow = np.append( csvRow, np.array([ int(behavior_ID[index]), int(behavior_conf[index])  ] ) )
            
            
            with open(focus_csv_path,"a+") as csvfile: 
                writer = csv.writer(csvfile)
                writer.writerow(csvRow)
            
            '''
            行为专注度判断
            0 称重
            1 测高度
            2 丢球
            3 测大小
            4 记录
            
            [0 4 1 2 3 4 1 2 3 4 1 2 3 4] 高
            [0 1 2 3 4 1 2 3 4 1 2 3 4] 高
            [1 2 3 4 1 2 3 4 1 2 3 4] 高
            
            [1 2 3 1 2 3 1 2 3] 低
            [2 3 2 3 2 3] 低


            [0 4 1 2 3 4 1 2 3 4] 高
            [0 1 2 3 4 1 2 3 4] 高
            [1 2 3 4 1 2 3 4] 高

            [1 2 3 1 2 3] 低
            [2 3 2 3] 低
            '''
            
            if float(behavior_conf[index]) >= 0.75:
                if len(behavior_sequence_orig) == 0:
                    behavior_pre = behavior_ID[index]
                    behavior_time_temp = 1
                    behavior_sequence_orig.append( int(behavior_ID[index]) )
                else:
                    # behavior_sequence_orig 的长度是从2开始的，因为筛选条件是最少需要2帧连续动作
                    if len(behavior_sequence_orig) == 1:
                        behavior_sequence_orig = []
                    if behavior_ID[index] == behavior_pre:
                        behavior_time_temp += 1
                        if behavior_time_temp == 2:
                            # behavior_sequence_orig 操作两次是因为之前的删除，这里补上
                            behavior_sequence_orig.append( int(behavior_ID[index]) )
                            behavior_sequence_orig.append( int(behavior_ID[index]) )
                        if behavior_time_temp > 2:
                            behavior_sequence_orig.append( int(behavior_ID[index]) )
                    else:
                        behavior_times[int(behavior_ID[index])].append(behavior_time_temp)
                        behavior_time_temp = 1
                        behavior_pre = behavior_ID[index]
    pre_temp = ''
    for enum in behavior_sequence_orig:
        if enum != pre_temp:
            behavior_sequence_merg.append(enum)
            pre_temp = enum



    for index in range(len(behavior_all_times)):
        behavior_all_times[index] = sum(behavior_times[index])+behavior_all_times[index]
        if len(behavior_times[index]) == 0:
            continue
        
        
        if max(behavior_times[index]) > behavior_max_times[index]:
            behavior_max_times[index] = max(behavior_times[index])
        
        if min(behavior_times[index]) < behavior_min_times[index] and min(behavior_times[index]) != 0:
            behavior_min_times[index] = min(behavior_times[index])

    
    behavior_focus_standard_high1 = [0,4,1,2,3,4,1,2,3,4,1,2,3,4]
    behavior_focus_standard_high2 = [0,1,2,3,4,1,2,3,4,1,2,3,4]
    behavior_focus_standard_high3 = [1,2,3,4,1,2,3,4,1,2,3,4]
    behavior_focus_standard_high4 = [0,4,1,2,3,4,1,2,3,4]
    behavior_focus_standard_high5 = [0,1,2,3,4,1,2,3,4]
    behavior_focus_standard_high6 = [1,2,3,4,1,2,3,4]

    behavior_focus_standard_low1 = [1,2,3,1,2,3,1,2,3]
    behavior_focus_standard_low2 = [2,3,2,3,2,3]
    behavior_focus_standard_low3 = [1,2,3,1,2,3]
    behavior_focus_standard_low4 = [2,3,2,3]

    # 创建一个空的最佳匹配变量和最大相似度变量
    best_match_sequence = None
    max_similarity = 0
    index_max = -1
        
    # 比较输入序列与给定序列，并更新最佳匹配和最大相似度
    sequences = [behavior_focus_standard_high1, behavior_focus_standard_high2, behavior_focus_standard_high3, behavior_focus_standard_high4, behavior_focus_standard_high5, behavior_focus_standard_high6, behavior_focus_standard_low1, behavior_focus_standard_low2, behavior_focus_standard_low3, behavior_focus_standard_low4]
    for index, sequence in enumerate(sequences):
        similarity = difflib.SequenceMatcher(None, behavior_sequence_merg, sequence).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            index_max = index
            best_match_sequence = sequence
    
    behavior_sequence_match_similarity = max_similarity
    
    print()
    print("row:",behavior_sequence_orig)
    print("behavior_sequence_merg:",behavior_sequence_merg)
    print("csv_file:",csv_file)
    # 打印最佳匹配序列和相似度
    print("Best match sequence:", best_match_sequence)
    print("Similarity:", max_similarity)
    if index_max < 6 and behavior_sequence_match_similarity >= 0.75:
        print("行为高专注度",index_max)
        behavior_sequence_concentration_index = 1
    else:
        print("行为低专注度",index_max)
        behavior_sequence_concentration_index = 0

    anger_time = np.sum(np.array(filter_face_ID).T == 0.0) # angry(生气)
    disgust_time = np.sum(np.array(filter_face_ID).T == 1.0) # disgust (厌恶)
    fear_time = np.sum(np.array(filter_face_ID).T == 2.0) # fear(害怕)
    happiness_time = np.sum(np.array(filter_face_ID).T == 3.0) # happy(快乐)
    # face_ID_neutral_time = np.sum(np.array(filter_face_ID).T == 4.0) # neutral (中性)
    sadness_time = np.sum(np.array(filter_face_ID).T == 5.0) # sad(悲伤)
    surprise_time = np.sum(np.array(filter_face_ID).T == 6.0) # surprise(惊奇)
    
    
    high_concentration_count = np.sum(np.array(filter_headPose_focus).T == 1.0)
    low_concentration_count = np.sum(np.array(filter_headPose_focus).T == 0.0)

    if int(behavior_sequence_concentration_index) == 1:
        high_concentration_time = len(behavior_sequence_orig)
        low_concentration_time = 0
    else:
        low_concentration_time = len(behavior_sequence_orig)
        high_concentration_time = 0
    
    with open(focus_summary_csv_path,"a+") as csvfile: 
        writer = csv.writer(csvfile)

        writer.writerow([csv_file.split('.')[0], 
                         behavior_sequence_orig, 
                         behavior_sequence_merg, 
                         best_match_sequence, 
                         behavior_sequence_match_similarity, 
                         behavior_sequence_concentration_index,
                         high_concentration_time, 
                         low_concentration_time,
                         anger_time, 
                         disgust_time, 
                         fear_time, 
                         happiness_time, 
                         sadness_time, 
                         surprise_time, 
                         high_concentration_count, 
                         low_concentration_count ])
        
print("behavior_all_times:",behavior_all_times)
print("avg_behavior_all_times:"," 称重: ", behavior_all_times[0]/511," 测高度: ", behavior_all_times[1]/511," 丢球: ",behavior_all_times[2]/511," 测大小: ",behavior_all_times[3]/511," 记录: ", behavior_all_times[4]/511)
print("behavior_max_times:"," 称重: ", behavior_max_times[0]," 测高度: ", behavior_max_times[1]," 丢球: ",behavior_max_times[2]," 测大小: ",behavior_max_times[3]," 记录: ", behavior_max_times[4])
print("behavior_min_times:"," 称重: ", behavior_min_times[0]," 测高度: ", behavior_min_times[1]," 丢球: ",behavior_min_times[2]," 测大小: ",behavior_min_times[3]," 记录: ", behavior_min_times[4])

