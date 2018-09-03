import time
import torch
import os
import numpy as np
from glob import glob
from torch.utils.data.dataset import Dataset
from torch.utils.data.dataloader import DataLoader
from torchvision import transforms
from PIL import Image
import torchvision
import torch.nn.functional as F
from torch.nn.parameter import Parameter
import math
import torch.nn as nn
import torch.optim as optim
import timeit


tranforms_train = transforms.Compose([

    transforms.Grayscale(1),  # Convert image to grayscale.
    transforms.RandomRotation((-15, 15)),
    transforms.Resize((32, 32)),
    transforms.ToTensor(),

])

tranforms_test = transforms.Compose([

    transforms.Grayscale(1),  # Convert image to grayscale.
    # transforms.RandomRotation((-15, 15)),
    transforms.Resize((32, 32)),
    transforms.ToTensor(),

])
train_dataset = torchvision.datasets.ImageFolder("../PIC/预处理", transform=tranforms_train)
train_data = DataLoader(train_dataset, batch_size=8, shuffle=True)

test_dataset = torchvision.datasets.ImageFolder("../PIC/测试", transform=tranforms_test)
test_data = DataLoader(test_dataset, batch_size=8, shuffle=True)


class Cap_Net(nn.Module):  # 搭建神经网络

    def __init__(self):
        super(Cap_Net, self).__init__()

        self.conv1 = nn.Conv2d(1, 16, 5)

        self.pooling = nn.MaxPool2d(2)

        self.conv2 = nn.Conv2d(16, 16, 5)

        self.pooling2 = nn.MaxPool2d(2)

        self.classfier = nn.Sequential(
            nn.Linear(400, 120),
            nn.ReLU(inplace=True),
            nn.Linear(120, 36),
        )

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x, inplace=True)
        x = self.pooling(x)

        x = self.conv2(x)
        x = F.relu(x, inplace=True)
        x = self.pooling2(x)
        x = x.view(-1, 400)
        x = self.classfier(x)

        return x


def train(train_loader):

    model.train()

    running_loss = 0.

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    for batch_idx, (data, labels) in enumerate(train_loader):

        data, labels = data.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(data)

        loss = loss_f(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        if (batch_idx + 1) % 10 == 0:
            print("loss:", loss.item())


model = Cap_Net()  # 生成一个cnn

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# device = torch.device("cuda:0" )

model = model.to(device)  # 确定走gpu还是cpu
loss_f = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=2e-3, momentum=0.9)  # 确定优化函数

start_time = timeit.default_timer()

for i in range(0, 100):
    cur_epoch = i + 1
    print("Epoch:", cur_epoch)
    train(train_data)

train_duration = timeit.default_timer() - start_time

correct = 0
total = 0

for data in test_data:
                images, labels = data
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
# 取得分最高的那个类
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum()
                # if(predicted == labels):
                print("结果："+str(predicted)+" 标签："+str(labels))

print('识别准确率为：%d%%' % (100 * correct / total))
torch.save(model,"D:/Code/PIC/model/" + str(100 * correct / total).replace('tensor', '') + "-net.pkl")  # 保存整个神经网络
print('训练总时间为: ', train_duration)