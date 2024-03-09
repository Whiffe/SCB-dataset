'''
python dataMerge.py \
    --multi_model_fusion_path /root/autodl-nas/multi_model_fusion \
    --headPose_path /root/autodl-nas/headPose \
    --face_output_txt_path /root/autodl-nas/face_output_txt \
    --studentParents_path /root/autodl-nas/studentParents \
    --behavior_path /root/autodl-nas/behavior \
    --multi_merge_path /root/autodl-nas/multi_model_fusion/multi_merge \
    --detect_frames_path /root/autodl-nas/detect_frames \
    
    
    
'''
import os
import cv2
import math
import numpy as np
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('--multi_model_fusion_path', default='/root/autodl-nas/multi_model_fusion',type=str)
parser.add_argument('--headPose_path', default='/root/autodl-nas/headPose',type=str)
parser.add_argument('--face_output_txt_path', default='/root/autodl-nas/face_output_txt',type=str)
parser.add_argument('--studentParents_path', default='/root/autodl-nas/studentParents',type=str)
parser.add_argument('--behavior_path', default='/root/autodl-nas/behavior',type=str)
parser.add_argument('--multi_merge_path', default='/root/autodl-nas/multi_model_fusion/multi_merge',type=str)
parser.add_argument('--detect_frames_path', default='/root/autodl-nas/detect_frames',type=str)



arg = parser.parse_args()
multi_model_fusion_path = arg.multi_model_fusion_path
headPose_path = arg.headPose_path
face_output_txt_path = arg.face_output_txt_path
studentParents_path = arg.studentParents_path
behavior_path = arg.behavior_path
multi_merge_path = arg.multi_merge_path
detect_frames_path = arg.detect_frames_path

new_headPose_path = os.path.join(multi_model_fusion_path, headPose_path.split('/')[-1])
new_face_output_txt_path = os.path.join(multi_model_fusion_path, face_output_txt_path.split('/')[-1])
new_studentParents_path = os.path.join(multi_model_fusion_path, studentParents_path.split('/')[-1])
new_behavior_path = os.path.join(multi_model_fusion_path, behavior_path.split('/')[-1])

os.system(f"rm -rf {multi_model_fusion_path}")
os.system(f"mkdir -p {multi_model_fusion_path}")



# 先将headpose进行文件夹分类，因为所有视频文件放在了一起
for root, dirs, files in os.walk(headPose_path, topdown=False):
    for name in files:
        if "checkpoint" not in name and ".txt" in name :
            video_name = name.split('_')[0]
            img_path = os.path.join(root, name)
            new_img_path = os.path.join(new_headPose_path, video_name)
            if not os.path.exists(new_img_path):
                os.system(f"mkdir -p {new_img_path}")
            os.system(f"cp {img_path} {os.path.join(new_img_path,name)}")

print(f"{headPose_path} done")


# 将face_output_txt进行文件夹分类，因为所有视频文件放在了一起
for root, dirs, files in os.walk(face_output_txt_path, topdown=False):
    for name in files:
        if "checkpoint" not in name and ".txt" in name :
            video_name = name.split('_')[0]
            img_path = os.path.join(root, name)
            new_img_path = os.path.join(new_face_output_txt_path, video_name)
            if not os.path.exists(new_img_path):
                os.system(f"mkdir -p {new_img_path}")
            os.system(f"cp {img_path} {os.path.join(new_img_path,name)}")

print(f"{face_output_txt_path} done")

# 修改studentParents文件夹下文件夹的名字，如exp修改其所对应的视频名01
for root, dirs, files in os.walk(studentParents_path, topdown=False):
    for name in files:
        if "checkpoint" not in name and ".txt" in name :
            video_name = name.split('_')[0]
            new_path = os.path.join(new_studentParents_path,video_name)
            if not os.path.exists(new_path):
                os.system(f"mkdir -p {new_path}")
            os.system(f"rm -rf {new_path}/*")
            os.system(f"cp -r {root} {new_path}")
            break

print(f"{studentParents_path} done")

# 修改behavior文件夹下文件夹的名字，如exp修改其所对应的视频名01
for root, dirs, files in os.walk(behavior_path, topdown=False):
    for name in files:
        if "checkpoint" not in name and ".txt" in name :
            video_name = name.split('_')[0]
            new_path = os.path.join(new_behavior_path,video_name)
            if not os.path.exists(new_path):
                os.system(f"mkdir -p {new_path}")
            os.system(f"rm -rf {new_path}/*")
            os.system(f"cp -r {root} {new_path}")
            break
print(f"{behavior_path} done")

          

if not os.path.exists(multi_merge_path):
    os.system(f"mkdir -p {multi_merge_path}")
else:
    os.system(f"rm -rf {multi_merge_path}")
    os.system(f"mkdir -p {multi_merge_path}")


# 转换yolo格式的候选框为左上(x1,y1)，右下角的坐标值(x2,y2)
def yolo_to_xywh(bbox):
    x, y, w, h = float(bbox[1]), float(bbox[2]), float(bbox[3]), float(bbox[4])
    x1 = (x - w / 2)
    # 保证x1，y1不小于0
    x1 = x1 if x1 > 0 else 0
    y1 = (y - h / 2)
    y1 = y1 if y1 > 0 else 0
    x2 = x1 + w
    y2 = y1 + h
    return x1, y1, x2, y2

def iou(box1, box2):
    '''
    两个框（二维）的 iou 计算
    
    注意：边框以左上为原点
    
    box:[x1,y2,x2,y2],依次为左上右下坐标
    '''
    h = max(0, min(box1[2], box2[2]) - max(box1[0], box2[0]))
    w = max(0, min(box1[3], box2[3]) - max(box1[1], box2[1]))
    area_box1 = ((box1[2] - box1[0]) * (box1[3] - box1[1]))
    area_box2 = ((box2[2] - box2[0]) * (box2[3] - box2[1]))
    inter = w * h
    union = area_box1 + area_box2 - inter
    iou = inter / union
    return iou

def is_point_in_bbox(point, bbox):
    x, y = point
    xmin, ymin, xmax, ymax = bbox
    
    if xmin <= x <= xmax and ymin <= y <= ymax:
        return True
    else:
        return False

# 以new_behavior_path作为循环来匹配其他模型
# 第一层循环拿到视频文件名
behaviorVideo_files = os.listdir(new_behavior_path)
behaviorVideo_files.sort()
for video_name in behaviorVideo_files:
    # 获取图片帧的大小 
    # 获取目录下的所有文件和文件夹列表
    detect_frames_list = os.listdir(os.path.join(detect_frames_path,video_name))
    
    detect_frames_img_path = os.path.join(detect_frames_path, video_name, detect_frames_list[0])
    
    detect_frames_img = cv2.imread(detect_frames_img_path)  #读取图片信息
    
    sp = detect_frames_img.shape #[高|宽|像素值由三种原色构成]
    detect_frames_height = sp[0]
    detect_frames_width = sp[1]
    
    # # 第二层循环拿到视频文件夹下的图片
    behavior_files = os.listdir(os.path.join(new_behavior_path, video_name, 'labels'))
    behavior_files.sort()
    for file_name in behavior_files:
        if "checkpoint" not in file_name and ".txt" in file_name:
            
            behavior_txt_path = os.path.join(new_behavior_path, video_name, 'labels', file_name)
            face_txt_path = os.path.join(new_face_output_txt_path, video_name, file_name)
            
            headPose_txt_path = os.path.join(new_headPose_path, video_name, file_name)
            studentParents_txt_path = os.path.join(new_studentParents_path, video_name, 'labels', file_name)
            # studentParents_txt_path = os.path.join(new_face_output_txt_path, video_name, 'labels', file_name)
            
            # 循环收集 behaviorData 的数据，
            behaviorData = []
            with open(behavior_txt_path) as file:
                lines = file.readlines()
                for line in lines:
                    data_temp = line.split(" ")
                    # behaviorID 是行为 ID
                    behaviorID = int(data_temp[0])
                    x1, y1, x2, y2 = yolo_to_xywh(data_temp)
                    behaviorData.append([ behaviorID, x1*detect_frames_width, y1*detect_frames_height, x2*detect_frames_width, y2*detect_frames_height, data_temp[5]])
            
            # 循环收集 face 的数据
            faceData = []
            if os.path.exists(face_txt_path):
                with open(face_txt_path) as file:
                    lines = file.readlines()
                    for line in lines:
                        data_temp = line.split(" ")
                        # faceID 是面部表情ID
                        faceID = int(data_temp[-1])
                        faceData.append([ faceID, float(data_temp[0]), float(data_temp[1]), float(data_temp[2]), float(data_temp[3])])
            
            # 循环收集 headPoseData 的数据
            headPoseData = []
            if os.path.exists(headPose_txt_path):
                with open(headPose_txt_path) as file:
                    lines = file.readlines()
                    for line in lines:
                        data_temp = line.split(" ")
                        headPoseData.append([ float(data_temp[0]), float(data_temp[1]), float(data_temp[2]), float(data_temp[3]), float(data_temp[4]) ])
            
            # 循环收集 studentParentsData 的数据
            studentParentsData = []
            if os.path.exists(studentParents_txt_path):
                with open(studentParents_txt_path) as file:
                    lines = file.readlines()
                    for line in lines:
                        data_temp = line.split(" ")
                        # SP 是身份ID
                        SP = int(data_temp[0])
                        x1, y1, x2, y2 = yolo_to_xywh(data_temp)
                        studentParentsData.append([ SP, x1*detect_frames_width, y1*detect_frames_height, x2*detect_frames_width, y2*detect_frames_height])

            
            # 循环 behaviorData 数据，然后根据headPoseData的数据来逐个匹配其他模型数据
            for behaviorDataTemp in behaviorData:
                behaviorBBox = [behaviorDataTemp[1], behaviorDataTemp[2], behaviorDataTemp[3], behaviorDataTemp[4]]
                
                # 匹配studentParentsData的数据
                filter_studentParentsData_Temp = ""
                for studentParentsData_Temp in studentParentsData:
                    studentParentsBBox = [studentParentsData_Temp[1],studentParentsData_Temp[2],studentParentsData_Temp[3],studentParentsData_Temp[4]]
                    if iou(behaviorBBox, studentParentsBBox)> 0.7:
                        filter_studentParentsData_Temp = studentParentsData_Temp
                        break
                
                # 匹配face的数据
                filter_faceData_Temp = ""
                for faceData_Temp in faceData:
                    faceDataPoint = [(faceData_Temp[1]+faceData_Temp[3])/2, (faceData_Temp[2]+faceData_Temp[4])/2]
                    if is_point_in_bbox(faceDataPoint, behaviorBBox):
                        filter_faceData_Temp = faceData_Temp
                        break
                
                # 匹配 headPose 的数据
                filter_headPoint_Temp = ""
                for headPoseData_Temp in headPoseData:
                    headPoint = [headPoseData_Temp[0],headPoseData_Temp[1]]
                    if is_point_in_bbox(headPoint, behaviorBBox):
                        filter_headPoint_Temp = headPoseData_Temp
                        break
                
                
                '''
                multi_merge_video_path = os.path.join(multi_merge_path, video_name)
                if not os.path.exists(multi_merge_video_path):
                    os.system(f"mkdir -p {multi_merge_video_path}")

                multi_merge_csv_path = os.path.join(multi_merge_video_path, file_name.split('.')[0]+'.csv')
                '''

                multi_merge_csv_path = os.path.join(multi_merge_path, video_name.split('.')[0]+'.csv')
                
                if not os.path.exists(multi_merge_csv_path):
                    with open(multi_merge_csv_path,"a+") as csvfile: 
                        writer = csv.writer(csvfile)
                        writer.writerow(["video_frame_ID","behavior_ID", "behavior_x1", "behavior_y1", "behavior_x2", "behavior_y2", "behavior_conf", "studentParents_ID", "studentParents_x1", "studentParents_y1", "studentParents_x2", "studentParents_y2", "headPose_x", "headPose_y", "headPose_yaw", "headPose_pitch", "headPose_roll", "face_ID", "face_x1", "face_y1", "face_x2", "face_y2"])
                else:
                    
                    csvRow = np.array([file_name.split(".")[0], behaviorDataTemp[0], behaviorDataTemp[1], behaviorDataTemp[2], behaviorDataTemp[3], behaviorDataTemp[4], behaviorDataTemp[-1]])
                    
                    # studentParents
                    if filter_studentParentsData_Temp != "": 
                        csvRow = np.append( csvRow,
                            np.array([
                            filter_studentParentsData_Temp[0], filter_studentParentsData_Temp[1], filter_studentParentsData_Temp[2], filter_studentParentsData_Temp[3],filter_studentParentsData_Temp[4]
                            ])
                        )
                    else:
                        csvRow = np.append( csvRow,
                            np.array(['','','','',''])
                        )
                    
                    # headPose
                    if filter_headPoint_Temp != "":
                        csvRow = np.append( csvRow,
                            np.array([
                            filter_headPoint_Temp[0], filter_headPoint_Temp[1], filter_headPoint_Temp[2], filter_headPoint_Temp[3],filter_headPoint_Temp[4]
                            ])
                        )
                    else:
                        csvRow = np.append( csvRow,
                            np.array(['','','','',''])
                        )
                        
                    
                    # face
                    if filter_faceData_Temp !=  "":
                        csvRow = np.append( csvRow,
                            np.array([
                                filter_faceData_Temp[0], filter_faceData_Temp[1], filter_faceData_Temp[2], filter_faceData_Temp[3], filter_faceData_Temp[4]
                            ])
                        )
                    else:
                        csvRow = np.append( csvRow,
                            np.array(['','','','',''])
                        )
                    
                    with open(multi_merge_csv_path,"a+") as csvfile: 
                        writer = csv.writer(csvfile)
                        writer.writerow(csvRow)

                
 
