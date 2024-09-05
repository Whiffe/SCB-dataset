# https://blog.csdn.net/qq_36785194/article/details/129223405
import os
from PIL import Image
 
 
# 获取指定目录下的所有png图片
def get_all_png_files(dir):
    files_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if os.path.splitext(file)[1] == '.png':
                files_list.append(os.path.join(root, file))
    return files_list
 
 
# 批量转换png图片为jpg格式
def png2jpg(files_list):
    for file in files_list:
        img = Image.open(file)
        new_file = os.path.splitext(file)[0] + '.jpg'
        img.convert('RGB').save(new_file)
 
 
if __name__ == '__main__':
    # dir = './5k_HRW_yolo_Dataset/images/train/' #png图片目录
    dir = './5k_HRW_yolo_Dataset/images/val/' #png图片目录
    files_list = get_all_png_files(dir)
    png2jpg(files_list)
