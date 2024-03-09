'''
python generate_down_videos3.py \
    --txt_path ./videos_raw.txt \
    --videos_path ./videos \
    --videos_list_path ./videos_list.txt

'''

# 打开videos_raw.txt文件，然后一行一行遍历

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--txt_path', default='./videos_raw.txt',type=str)
parser.add_argument('--videos_path', default='./videos',type=str)
parser.add_argument('--videos_list_path', default='./videos_list.txt',type=str)

arg = parser.parse_args()

txt_path = arg.txt_path
videos_path = arg.videos_path
videos_list_path = arg.videos_list_path


if not os.path.exists(videos_list_path):
    os.system(f"touch {videos_list_path}")
else:
    os.system(f"rm -rf {videos_list_path}")
    os.system(f"touch {videos_list_path}")

with open(txt_path, 'r') as f:
    for line in f:
        # 去掉每行末尾的换行符
        line = line.strip()

        # 只要每行中 /seed开头，.MOV,.MP4结尾的字符
        # if '.mp4' in line:

        # 定位到line中 “/seed的起始位置”
        spilt_start = line.find('/seed')
        # 定位到line中 “.MOV.MP4结尾的起始位置”
        if '.mp4' in line:
            spilt_end = line.find('.mp4') + len(".mp4")
        elif '.MP4' in line:
            spilt_end = line.find('.MP4') + len(".MP4")
        elif '.mov' in line:
            spilt_end = line.find('.mov') + len(".mov")
        elif '.MOV' in line:
            spilt_end = line.find('.MOV') + len(".MOV")
        else:
            assert False, "line.find('.mp4') or line.find('.MP4') or line.find('.mov') or line.find('.MOV') == -1"

        print(line[spilt_start:spilt_end].split("/")[-1].split('.')[0])
        with open(videos_list_path,"a+") as f:
            f.write(line[spilt_start:spilt_end].split("/")[-1].split('.')[0]+"\n") 
        #os.system('wget -P ' + videos_path + ' ' + video_path)

        
