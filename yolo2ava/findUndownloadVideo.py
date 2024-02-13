# python findUndownloadVideo.py --video_path ./ava/trainval --csv_path ./ava/ava_v2.2/ava_train_v2.2.csv
# python findUndownloadVideo.py --video_path ./ava/trainval --csv_path ./ava/ava_v2.2/ava_val_v2.2.csv
import csv
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--video_path', default='./ava/trainval',type=str)
parser.add_argument('--csv_path', default='./ava/ava_v2.2/ava_train_v2.2.csv',type=str)

arg = parser.parse_args()

video_path = arg.video_path
csv_path = arg.csv_path

# 获取./ava/trainval文件夹下所有视频名，视频格式有mp4，mkv，webm，MOV，但是不存储视频的后缀
video_names = []

undownloadVideos = []

for filename in os.listdir(video_path):
    if filename.endswith('.mp4') or filename.endswith('.mkv') or filename.endswith('.webm') or filename.endswith('.MOV'):
        video_names.append(filename.split('.')[0])
# 读取csv文件
with open(csv_path, 'r') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # 跳过csv的标题行

        # 遍历csv文件中的每一行数据
    for row in csv_data:
        video_name = row[0]
        # 判断video_name在不在video_names中，如果不在就判断video_name在不在undownloadVideos，如果都不在，就将video_name添加到undownloadVideos
        if video_name not in video_names:
            if video_name not in undownloadVideos:
                undownloadVideos.append(video_name)
print(undownloadVideos)