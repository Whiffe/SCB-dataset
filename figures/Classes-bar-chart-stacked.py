import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# 设置Seaborn样式
sns.set(style="whitegrid")

# 类别和对应的数量
categories = [
    'hand-raising', 'read', 'write', 'screen', 'blackboard', 'discuss',
    'guide', 'answer', 'on-stage-interaction', 'blackboard-writing', 'stand',
    'teacher', 'bow-head', 'turn-head', 'talk'
]
counts_train = [
    10538, 17539, 6447, 1566, 2547, 3607,
    1286, 2547, 516, 793, 9670,
    6047, 4422, 7943, 4184
]
counts_val = [ 
    2915, 6539, 3394, 514, 933, 1785,
    146, 475, 62, 141, 3299,
    1680, 540, 3213, 1322
]

# 对类别和数量进行排序
sorted_pairs = sorted(zip(categories, counts_train, counts_val), key=lambda x: x[1], reverse=True)
sorted_categories, sorted_counts_train, sorted_counts_val = zip(*sorted_pairs)

# 绘制柱状图
plt.figure(figsize=(6, 6))  # 调整图形大小

# 绘制训练集数据的柱状图
bars_train = plt.bar(sorted_categories, sorted_counts_train, color='skyblue', width=0.6, label='Train Dataset')

# 绘制验证集数据的柱状图，叠加在训练集的柱状图上
bars_val = plt.bar(sorted_categories, sorted_counts_val, color='lightcoral', width=0.6, 
                   bottom=sorted_counts_train, label='Val Dataset')

# 添加标题和标签
plt.ylabel('Numbers (in thousands)', fontsize=14)

# 旋转横坐标标签
plt.xticks(rotation=90, ha='center', fontsize=14)

# 添加网格线
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 自定义纵坐标格式
formatter = FuncFormatter(lambda x, pos: f'{x/1000:.1f}')
plt.gca().yaxis.set_major_formatter(formatter)

# 添加图例
plt.legend()

# 保存图形为PDF
plt.savefig('Classes-bar-chart-stacked.pdf', bbox_inches='tight', pad_inches=0.1)

# 显示图形
plt.tight_layout()
plt.show()
