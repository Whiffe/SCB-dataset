# python img2video.py --img_dataset_Path ./5k_HRW_yolo_Dataset
# 图片转视频
import cv2
import os
import argparse


fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 设置输出视频为mp4格式
# cap_fps是帧率，可以根据随意设置
cap_fps = 10

#将图片转为视频
def img2video(imgPath,videPath):
    #读取图片的大小
    imgsize = cv2.imread(imgPath).shape
    imgHeight = imgsize[0]
    imgWith = imgsize[1]

    #设置视频参数
    video = cv2.VideoWriter(videPath, fourcc, cap_fps, (imgWith,imgHeight))

    img = cv2.imread(imgPath)

    #将图片写入视频中
    for index in range(6*cap_fps):
        video.write(img)
    #释放资源
    video.release()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dataset_Path', default='./5k_HRW_yolo_Dataset',type=str)

    arg = parser.parse_args()

    img_dataset_Path = arg.img_dataset_Path

    # 用os.walk 遍历img_dataset_Path
    for root, dirs, files in os.walk(img_dataset_Path):
        for name in files:
            if "checkpoint" not in name:
                # if 筛选png或者jpg为扩展名的文件
                if name.endswith('png') or name.endswith('jpg'):
                    # 图片路径
                    img_path = os.path.join(root, name)
                    # 视频路径
                    video_path = img_path.replace('images', 'videos').replace('jpg', 'mp4').replace('png', 'mp4')
                    
                    # 调用img2video函数
                    img2video(img_path, video_path)
                    print(img_path,video_path)
