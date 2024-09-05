import pandas as pd
import datetime

# 将秒数转换为hh:mm:ss格式
def seconds_to_hms(seconds):
    return str(datetime.timedelta(seconds=seconds))

# 读取Excel文件并清理数据
file_path = 'behavior.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(file_path, index_col=0)  # 设置行为列为索引
df = df.dropna(axis=1, how='all')  # 删除所有空白列
df = df.dropna(axis=0, how='all')  # 删除所有空白行
input(df)
# 初始化结果字典
result = {}

# 遍历每一行，处理每个行为
for behavior, times in df.iterrows():
    times = times.dropna().tolist()  # 获取每一行的有效数据
    result[behavior] = []
    
    start_time = None
    duration = 0
    
    # 遍历每一秒的数据
    for second, value in enumerate(times, start=1):
        if value > 0:  # 如果有该行为
            if start_time is None:
                start_time = second  # 记录开始时间
            duration += 1
        else:
            if duration >= 3:  # 如果行为持续了3秒或以上
                end_time = second - 1
                result[behavior].append(f"{seconds_to_hms(start_time)} - {seconds_to_hms(end_time)}")
            start_time = None
            duration = 0
    
    # 处理最后一段持续的行为
    if duration >= 3:
        end_time = second
        result[behavior].append(f"{seconds_to_hms(start_time)} - {seconds_to_hms(end_time)}")

# 输出结果
for behavior, time_ranges in result.items():
    print(f'"{behavior}": {time_ranges}')
