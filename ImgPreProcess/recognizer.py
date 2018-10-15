import torch
from torch.utils.data.dataloader import DataLoader
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
import re
import os


class Cap_Net(nn.Module):
    # pytorch的bug，自定义class保存后，如果在新的文件里load，还需要重新定义class

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


class Recongnizer(object):
    '''
    用于识别验证码的类
    '''
    def _recongnie(self, networkPath, ImageFolder):
        '''
        识别验证码的方法
        :param networkPath:保存的网络位置
        :param ImageFolder:要识别的若干切分后验证码图片的位置
        :return:预测结果字符串
        '''
        net = Cap_Net()  # 初始化

        net = torch.load(networkPath,)

        my_tranforms = transforms.Compose([

            transforms.Grayscale(1),
            transforms.Resize((32, 32)),
            transforms.ToTensor(),

        ])

        dataset = torchvision.datasets.ImageFolder("D:\pic\切分", transform=my_tranforms)
        datas = DataLoader(dataset, batch_size=8, shuffle=True)

        result = ''
        for data in datas:
            images, labels = data
            outputs = net(images)

            # 取得分最高的那个类
            _, predicted = torch.max(outputs.data, 1)

            result = result + str(predicted)

        return result


    def find_classes(self, dataset_dir):
        # 这个方法将来可以放在训练过程中
        # pytorch的DatasetFolder方法在读取数据集文件时会对标签做索引以输入网络
        # 我们需要根据索引找到其对应的label，这里对原数据集文件做反向的“索引：标签”映射，便于后续查找
        classes = [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]
        classes.sort()
        idx_to_classes = {i: classes[i] for i in range(len(classes))}
        return idx_to_classes


    def parseResult(self, result, idx_to_class):
        # 最小匹配
        p1 = re.compile(r'[[](.*?)[]]', re.S)
        results = re.findall(p1, result)
        results = results[0].split(',')
        r = []
        for i in results:
            r.append(idx_to_class[int(i)])
        return  r


    def recongnize(self, networkPath, ImageFolder, dataset_dir,):
        result = self._recongnie(networkPath, ImageFolder)
        idx_to_classes = self.find_classes(dataset_dir)
        result = ''.join(self.parseResult(result, idx_to_classes))
        return result
