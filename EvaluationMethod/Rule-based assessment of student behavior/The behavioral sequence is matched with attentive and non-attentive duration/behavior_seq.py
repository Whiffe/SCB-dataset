import csv

# 确定子集在数组中的起点
def find_subsets_starts(arrs, subset):
    indices = []
    subset_len = len(subset)
    for i in range(len(arrs) - subset_len + 1):
        if arrs[i:i+subset_len] == subset:
            indices.append(i)
    return indices



# 获取数组的所有子集
def getsubsets(arr):  
    if not arr:  
        return [[]]  # 如果原始数组为空，返回空集  
    result = []  
    
    # 下面的循环实现核心功能：
    '''
    如：[4, 2]的子集：[4, 2]
    如：[0, 2, 4, 2]的子集：[0, 2], [2, 4], [4, 2], [0, 2, 4], [2, 4, 2], [0, 2, 4, 2]
    '''
    for i in range(2,len(arr)+1):
        for j in range(len(arr)+1-i):
            result.append(arr[j:j+i])
    return result

def find_continuous_intersection(arr1, arr2):
    """
    :type arr1:list
    :type arr2:list
    :rtype :list
    """

    # arr1长度不能低于1
    if len(arr1) <= 1:
        return []


    # 获取arr1数组的所有子集
    subsets = getsubsets(arr1)

    # 去掉子集中的空集与长度为1的子集
    subsets = [subset for subset in subsets if len(subset) > 1]


    # 获取arr2数组的所有子集
    subsets2 = getsubsets(arr2)

    # 去掉子集中的空集与长度为1的子集
    subsets2 = [subset for subset in subsets2 if len(subset) > 1]



    # print(subsets)
    # 遍历arr1所有子集
    max_subset = []
    for subset in subsets:
        # 判断子集是否是 arr2 的子集
        if subset in subsets2:
            #return subset
            if len(subset) > len(max_subset):
                max_subset = subset
    return max_subset



#读取behvavior_seq.csv,从第二行开始读

focus_seq_intersections = [['focus_seq_intersections']]
focus_seq_start_end = [['focus_seq_start_end']]
focus_seq_org = [['focus_seq_org']]
focus_seq_time = [['focus_seq_time']]
unfocus_seq_time = [['unfocus_seq_time']]

with open('behavior_seq.csv','r') as f:
    reader = csv.reader(f)
    for index,row in enumerate(reader):
        if index == 0:
            continue
        for i in range(len(row)):
            row[i] = row[i]
            # 将字符转成数组
            row[i] = row[i].split(',')
            # 将数组中的元素转化为整数
            for j in range(len(row[i])):
                try:
                    row[i][j] = int(row[i][j])
                except:
                    pass

        # row[0] behavior_sequence_orig
        # row[1] behavior_sequence_merg
        # row[2] behavior_best_match_sequence
        
        # 计算row[1]和row[2]的交集
        focus_seq = find_continuous_intersection(row[1],row[2])
        focus_seq_intersections.append(focus_seq)

        
        if len(focus_seq) == 0:
            focus_seq_start_end.append([])
            focus_seq_org.append([])
            focus_seq_time.append(0)
            unfocus_seq_time.append(len(row[0]))
            continue
        indices_starts = find_subsets_starts(row[1],focus_seq)
        
        # merg_index 代表融合行为序列下标
        merg_index = 0
        # org_start_temp 代表原序列开始下标，temp临时
        org_start_temp = 0
        # traversal_len_TF 代表是否在遍历：匹配上的原序列长度
        traversal_len_TF = False
        # traversal_len 代表遍历：匹配上的原序列长度
        traversal_len = 0
        # focus_seq_start_end_temp 代表匹配上的原序列开始与结束下标，临时，最后存入focus_seq_start_end
        focus_seq_start_end_temp = []

        focus_seq_org_temp = []
        
        focus_seq_time_temp = 0

        # 遍历row[0]
        for index2, i in enumerate(range(len(row[0]))):
            # 第一次进来时，首先判断merg_index（第一个值）是否在indices_starts中
            if not traversal_len_TF:
                if merg_index in indices_starts:
                    org_start_temp = index2
                    traversal_len_TF = True
                    traversal_len = 1
            # 判断下一个值是否越界
            if i+1 < len(row[0]):
                # 判断当前值与下一个值是不是相同的
                if row[0][i] == row[0][i+1]:
                    continue
                else:
                    # 如果traversal_len_TF为True，代表正在匹配序列中
                    if traversal_len_TF:
                        # 如果traversal_len的长度与focus_seq长度一样，说明遍历完成
                        if traversal_len == len(focus_seq):
                            # traversal_len == len(focus_seq)，说明已经遍历完成
                            # traversal_len_TF = false，设置traversal_len_TF为false
                            traversal_len_TF = False
                            traversal_len = 0
                            focus_seq_start_end_temp.append([org_start_temp,index2])
                            focus_seq_org_temp.append(row[0][org_start_temp:index2+1])
                            focus_seq_time_temp = focus_seq_time_temp + index2 - org_start_temp + 1
                        # 继续遍历
                        else:
                            traversal_len = traversal_len + 1
                    # 如果traversal_len_TF为False，代表没有在匹配
                    else:
                        # 不是在遍历匹配上的原序列长度，那么就判断是否是起点
                        # 如果是起点，那么就记录起点，并且设置traversal_len_TF为true
                        if merg_index in indices_starts:
                            org_start_temp = index2
                            traversal_len_TF = True
                            traversal_len = 1
                    merg_index = merg_index + 1
            # 遍历到最后一个
            else:
                if traversal_len_TF:  
                    if traversal_len == len(focus_seq):
                        # traversal_len == len(focus_seq)，说明已经遍历完成
                        # traversal_len_TF = false，设置traversal_len_TF为false
                        traversal_len_TF = False
                        traversal_len = 0
                        focus_seq_start_end_temp.append([org_start_temp,index2])
                        focus_seq_org_temp.append(row[0][org_start_temp:index2+1])
                        focus_seq_time_temp = focus_seq_time_temp + index2 - org_start_temp + 1

        focus_seq_start_end.append(focus_seq_start_end_temp)
        focus_seq_org.append(focus_seq_org_temp)
        focus_seq_time.append(focus_seq_time_temp)
        unfocus_seq_time.append(len(row[0]) - focus_seq_time_temp)

# 将生成的数据写入csv

with open('focus_seq.csv','w',newline='') as f:
    writer = csv.writer(f)
    for i in range(len(focus_seq_intersections)):
        writer.writerow([focus_seq_intersections[i],focus_seq_start_end[i],focus_seq_org[i],focus_seq_time[i],unfocus_seq_time[i]])


