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

tranforms_type = transforms.Compose([

    transforms.Grayscale(1),
    transforms.Resize((32, 32)),
    transforms.ToTensor(),

])
train_dataset = torchvision.datasets.ImageFolder("G:/验证码/预处理", transform=tranforms_type)
train_data = DataLoader(train_dataset, batch_size=4, shuffle=True)
test_dataset = torchvision.datasets.ImageFolder("G:/验证码/测试", transform=tranforms_type)
test_data = DataLoader(test_dataset, batch_size=4, shuffle=True)

class Cap_Net(nn.Module):

    def __init__(self):
        super(Cap_Net, self).__init__()

        self.conv1 = nn.Conv2d(1, 16, 5)

        self.pooling = nn.MaxPool2d(2)

        self.conv1_1 = nn.Conv2d(16, 16, 5)

        self.pooling2 = nn.MaxPool2d(2)

        self.classfier = nn.Sequential(
            nn.Linear(400, 120),
            nn.ReLU(inplace=True),
            nn.Linear(120, 35),
        )

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x, inplace=True)
        x = self.pooling(x)

        x = self.conv1_1(x)
        x = F.relu(x, inplace=True)
        x = self.pooling2(x)
        x = x.view(-1, 400)
        x = self.classfier(x)

        return x


def train(train_loader):
    model.train()

    running_loss = 0.

    cur_epoch = 1

    print("Epoch:", cur_epoch)
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
model = Cap_Net()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)
loss_f = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=2e-3, momentum=0.95)
for i in range(0,50):
    train(train_data)