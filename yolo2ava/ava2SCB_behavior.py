# python ava2SCB_behavior.py --csv_path ./ava/ava_v2.2/ava_train_v2.2.csv  --frames_path ./ava/trainval_frames/ --yolo_SCB_data_path ./SCB
# python ava2SCB_behavior.py --csv_path ./ava/ava_v2.2/ava_val_v2.2.csv  --frames_path ./ava/trainval_frames/ --yolo_SCB_data_path ./SCB
import os
import json
import csv
import shutil  

import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--csv_path', default='./ava/ava_v2.2/ava_train_v2.2.csv',type=str)
parser.add_argument('--frames_path', default='./ava/trainval_frames/',type=str)
parser.add_argument('--yolo_SCB_data_path', default='./SCB',type=str)


arg = parser.parse_args()

csv_path = arg.csv_path
frames_path = arg.frames_path
yolo_SCB_data_path = arg.yolo_SCB_data_path

# 先清空 yolo_SCB_data_path 下所偶文件夹及文件
if os.path.exists(yolo_SCB_data_path):  
    # 删除文件夹及其所有内容  
    shutil.rmtree(yolo_SCB_data_path)  
else:  
    print("yolo_SCB_data_path Folder does not exist.")


def gen_yolo_SCB(yolo_SCB_data_path, train_val='train', behavior_id = -1):
    # 将original_image_path复制到 yolo_SCB_data_path/images/train中
    os.makedirs(os.path.join(yolo_SCB_data_path, 'images', train_val), exist_ok=True)
    # os.system(f'cp {original_image_path} {os.path.join(yolo_SCB_data_path, "images", "train") }')
    shutil.copy(original_image_path, os.path.join(yolo_SCB_data_path, "images", "train"))

    
    if int(behavior_id) ==  47:
        yolo_behavior_id = '1'
    if int(behavior_id) ==  62:
        yolo_behavior_id = '2'
    if int(behavior_id) ==  78:
        yolo_behavior_id = '6'

    # 将coordinates 转化为字符串，追加写入 yolo_SCB_data_path/labels/train中的txt中
    # 其中txt的名字与图片的名字一样                
    coordinates_str = str(coordinates[0]) + ' ' + str(coordinates[1]) + ' ' + str(coordinates[2]) + ' ' + str(coordinates[3])
    os.makedirs(os.path.join(yolo_SCB_data_path, 'labels', train_val), exist_ok=True)
    with open(os.path.join(yolo_SCB_data_path, 'labels', train_val, f'{video_name}_{frame_id.zfill(6)}.txt'), 'a') as f:
        f.write(yolo_behavior_id + ' ' + coordinates_str)
        f.write('\n')
    



avaActionList = ["bend/bow (at the waist)", "crawl", "crouch/kneel", "dance", "fall down", "get up", "jump/leap", "lie/sleep", "martial art", "run/jog", "sit", "stand", "swim", "walk", "answer phone", "brush teeth", "carry/hold (an object)", "catch (an object)", "chop", "climb (e.g., a mountain)", "clink glass", "close (e.g., a door, a box)", "cook", "cut", "dig", "dress/put on clothing", "drink", "drive (e.g., a car, a truck)", "eat", "enter", "exit", "extract", "fishing", "hit (an object)", "kick (an object)", "lift/pick up", "listen (e.g., to music)", "open (e.g., a window, a car door)", "paint", "play board game", "play musical instrument", "play with pets", "point to (an object)", "press", "pull (an object)", "push (an object)", "put down", "read", "ride (e.g., a bike, a car, a horse)", "row boat", "sail boat", "shoot", "shovel", "smoke", "stir", "take a photo", "text on/look at a cellphone", "throw", "touch (an object)", "turn (e.g., a screwdriver)", "watch (e.g., TV)", "work on a computer", "write", "fight/hit (a person)", "give/serve (an object) to (a person)", "grab (a person)", "hand clap", "hand shake", "hand wave", "hug (a person)", "kick (a person)", "kiss (a person)", "lift (a person)", "listen to (a person)", "play with kids", "push (another person)", "sing to (e.g., self, a person, a group)", "take (an object) from (a person)", "talk to (e.g., self, a person, a group)", "watch (a person)"]

# read avaActionList[47]
# write avaActionList[62]
# talk to (e.g., self, a person, a group)  avaActionList[78]

# behavior_id_SCB = [47, 62, 78]
# behavior_id_SCB = [47, 62]
behavior_id_SCB = [78]

'''
在YOLO（You Only Look Once）目标检测中，每个边界框由其中心点坐标、宽度、高度和旋转角度表示。在将左上角和右上角坐标转换为YOLO格式时，通常需要进行归一化处理。

以下是一个简单的Python函数，用于将左上角和右上角坐标转换为YOLO格式：
'''
def box_to_yolo(x1, y1, x2, y2):  
    """  
    将左上角和右上角坐标转换为YOLO格式。  
      
    参数:  
        x1, y1: 左上角坐标  
        x2, y2: 右上角坐标  
      
    返回:  
        cx: 中心点x坐标  
        cy: 中心点y坐标  
        w: 宽度  
        h: 高度  
        theta: 旋转角度（弧度）  
    """  
    cx = (x1 + x2) / 2  
    cy = (y1 + y2) / 2  
    w = abs(x2 - x1)  
    h = abs(y2 - y1)  
    return cx, cy, w, h

# i=0
# 读取csv文件
with open(csv_path, 'r') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # 跳过csv的标题行
    
    # 遍历csv文件中的每一行数据
    for row in csv_data:
        # 获取视频名称、帧编号、坐标、行为编号和人物编号
        video_name = row[0]
        frame_id = str( ( int(row[1])-900 ) * 30 + 1)
        behavior_id = row[6]
        coordinates = box_to_yolo(float(row[2]), float(row[3]), float(row[4]), float(row[5]) )

        if int(behavior_id) in behavior_id_SCB:
            # 构建原帧图片的路径
            original_image_path = os.path.join(frames_path, video_name, f'{video_name}_{frame_id.zfill(6)}.jpg')
            # 判断original_image_path是否存在，如果不存在，报错，然后跳过
            if not os.path.exists(original_image_path):
                # raise ValueError(f'Original image path not found: {original_image_path}')
                print(f'Original image path not found: {original_image_path}')
                continue
            
            # 将original_image_path的图片复制到yolo_SCB_data_path中
            if 'train' in csv_path:
                # i=i+1
                gen_yolo_SCB(yolo_SCB_data_path, train_val='train', behavior_id=behavior_id)
            if 'val' in csv_path:
                # i=i+1
                gen_yolo_SCB(yolo_SCB_data_path, train_val='val',behavior_id=behavior_id)

# print("i:",i)