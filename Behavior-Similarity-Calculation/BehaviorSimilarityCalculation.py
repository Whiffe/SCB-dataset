import os


def compute_iou(rec1, rec2):
    """
    computing IoU
    rec1: (x0, y0, x1, y1)
    rec2: (x0, y0, x1, y1)
    :return: scala value of IoU
    """
    # computing area of each rectangle
    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

    # computing the sum_area
    sum_area = S_rec1 + S_rec2

    # find the each edge of intersect rectangle
    left_line = max(rec1[1], rec2[1])
    right_line = min(rec1[3], rec2[3])
    top_line = max(rec1[0], rec2[0])
    bottom_line = min(rec1[2], rec2[2])

    # judge if there is an intersect area
    if left_line >= right_line or top_line >= bottom_line:
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        return (intersect / (sum_area - intersect)) * 1.0


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
    return [x1, y1, x2, y2]

def find_matching_rows(arr):
    rows = len(arr)
    
    count_overlap = {}
    count_category = {}
    # 遍历每一行
    for i in range(rows):
        # 获取当前行的类别和bbox
        current_row = arr[i]
        current_category = current_row[0]
        current_bbox = yolo_to_xywh(current_row)
        
        try:
            count_category[current_category] = count_category[current_category] +1
        except:
            count_category[current_category] = 1

        # 在当前行之后的行中进行匹配
        for j in range(i+1, rows):
            # 获取下一行的类别和bbox
            next_row = arr[j]
            next_category = next_row[0]
            next_bbox = yolo_to_xywh(next_row)
            
            if current_category == next_category:
                continue
            
            # 判断bbox是否重叠
            # print(current_bbox, next_bbox)
            if compute_iou(current_bbox, next_bbox) > 0.95:
                # 匹配成功，记录数量
                
                if int(current_category) < int(next_category):
                    key_category = current_category + " " + next_category
                else:
                    key_category = next_category + " " + current_category
                    
                try:
                    count_overlap[key_category] = count_overlap[current_category + " " + next_category] +1  
                except:
                    count_overlap[key_category] = 1
    return count_category, count_overlap
all_count_category = {}
all_count_overlap = {}
for root, dirs, files in os.walk("./5k_HRW_labels", topdown=False):
     for name in files:
        if "checkpoint" not in name and ".txt" in name :
            HRW_Data = [] 
            txtPath = os.path.join(root,name)
            with open(txtPath) as file:
                lines = file.readlines()
                for line in lines:
                    HRW_Data.append(line.split(' '))
            count_category, count_overlap = find_matching_rows(HRW_Data)
            
            for key in count_category:
                try:
                    all_count_category[key] = all_count_category[key] + count_category[key]
                except:
                    all_count_category[key] = count_category[key]

            for key in count_overlap:
                try:
                    all_count_overlap[key] = all_count_overlap[key] + count_overlap[key]
                except:
                    all_count_overlap[key] = count_overlap[key]

print("all_count_category:",all_count_category)
print("all_count_overlap:",all_count_overlap)
            

