import csv

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

with open('behavior_seq.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
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
        print("focus_seq:",focus_seq)

        print(row[1],row[2])
        input()




