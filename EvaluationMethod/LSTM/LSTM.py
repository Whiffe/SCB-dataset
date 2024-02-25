! pip install pandas
import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F

# 定义LSTM模型
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

# 自定义数据集类
class CustomDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sequence = list(map(int, str(self.data.iloc[idx, 0]).split(', '))) # 将字符串序列转换为整数列表
        label = int(self.data.iloc[idx, 1]) # 获取标签
        return torch.tensor(sequence), torch.tensor(label)

# 超参数设置
input_size = 1 # 输入特征维度（每个行为序列中的元素个数）
hidden_size = 128 # LSTM隐藏单元数
num_layers = 2 # LSTM层数
num_classes = 3 # 分类类别数
batch_size = 4
num_epochs = 20
learning_rate = 0.0001

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def collate_fn(batch):
    sequences, labels = zip(*batch)
    # 找到最长的序列长度
    max_length = max([len(seq) for seq in sequences])
    # 填充序列
    sequences_padded = [torch.cat([seq, torch.zeros(max_length - len(seq)).long()]) for seq in sequences]
    return torch.stack(sequences_padded, dim=0), torch.tensor(labels)


# 加载数据集
dataset = CustomDataset('/root/LSTM2/train.csv')  # 修改为Excel文件的路径



loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)

# loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)


# 初始化模型、损失函数和优化器
model = LSTMModel(input_size, hidden_size, num_layers, num_classes).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# 训练模型
total_step = len(loader)
for epoch in range(num_epochs):
    for i, (sequences, labels) in enumerate(loader):
        # print(i, (sequences, labels))
        # input()
        sequences = sequences.view(-1, len(sequences[0]), input_size).float().to(device) # 将输入形状调整为(batch_size, sequence_length, input_size)
        labels = labels.to(device)

        # 正向传播
        outputs = model(sequences)
        loss = criterion(outputs, labels)

        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (i+1) % 20 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, i+1, total_step, loss.item()))

print('训练完成')

# 在测试集上评估模型
# ...
# 加载测试数据集
test_dataset = CustomDataset('/root/LSTM2/test.csv')  # 使用测试集的CSV文件路径
# test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)

# 将模型设置为评估模式
model.eval()

total_correct = 0
total_samples = 0
with torch.no_grad():
    for sequences, labels in test_loader:
        sequences = sequences.view(-1, len(sequences[0]), input_size).float().to(device) # 将输入形状调整为(batch_size, sequence_length, input_size)
        # sequences = sequences.unsqueeze(2).to(device)  # 添加一个维度，将序列变成三维张量
        labels = labels.to(device)

        # 正向传播
        outputs = model(sequences)
        # probabilities = F.softmax(outputs, dim=1)  # 应用softmax变换
        _, predicted = torch.max(outputs, 1)

        # 统计正确预测的样本数量
        total_correct += (predicted == labels).sum().item()
        total_samples += labels.size(0)

# 计算准确率
accuracy = total_correct / total_samples
print('在测试集上的准确率: {:.2f}%'.format(accuracy * 100))
