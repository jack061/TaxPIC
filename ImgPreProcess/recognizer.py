import torch
from torch.utils.data.dataloader import DataLoader
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from ImgPreProcess import ImgPreProcesser
import re
import os
from settings import *
import base64


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
    def __init__(self):

        self.ImgPreProcesser = ImgPreProcesser()
        if MODE == 'test':
            self.networkPath = NETWORK_PATH
            self.ImageFolder = IMAGE_FOLDER   # 保存的网络
            self.dataset_dir = DATASET_FOLDER  # 存放神经网络训练数据集
            self.yzm_SaveDir = YZM_CUTFOLDER  # 存放原始验证码图片文件的文件夹
            self.yzm_CutDir = YZM_CUTFOLDER  # 处理后切分的图片存放位置


    def yzmSaver(self, imgtype, imgbase64):
        '''
        把获得的验证码保存到特定的文件夹
        :param imgtype: dict  {'info': u'请输入验证码文字', 'img': 'yzm_all.png', 'typecode': 0},
        :param imgbase64:
        :return:
        '''
        imgdata = base64.b64decode(imgbase64)
        filename = imgtype['img']
        filepath = self.yzm_SaveDir + '\\' + filename
        with open(filepath, 'wb') as f:
            f.write(imgdata)
            f.close()


    def _recongnie(self, networkPath, ImageFolder):
        '''
        识别验证码的方法
        :param networkPath:保存网络的位置
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

        dataset = torchvision.datasets.ImageFolder(ImageFolder, transform=my_tranforms)
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
        # 我们需要根据索引找到其对应的label，这里对原数据集文件做反向的“索引：标签”映射，便于后续查找\
        classes = [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]
        classes.sort()
        idx_to_classes = {i: classes[i] for i in range(len(classes))}
        return idx_to_classes


    def parseResult(self, result, dataset_dir):
        '''
        将输出的标签由数字映射成我们数据集的类别
        :param result:
        :return:
        '''
        idx_to_classes = self.find_classes(dataset_dir)
        # 最小匹配
        p1 = re.compile(r'[[](.*?)[]]', re.S)
        results = re.findall(p1, result)
        results = results[0].split(',')
        r = []
        for i in results:
            r.append(idx_to_classes[int(i)])
        return  r


    def recongnize(self, imgtype, imgbase64, networkPath=None, ImageFolder=None, dataset_dir=None,):

        self.yzmSaver(imgtype, imgbase64)

        if MODE == 'test':
            networkPath = self.networkPath
            ImageFolder = self.ImageFolder
            dataset_dir = self.dataset_dir

        result = self._recongnie(networkPath, ImageFolder)
        # print(result)
        result = ''.join(self.parseResult(result, dataset_dir))
        # print('2' , result)
        return result


if __name__ == '__main__':
    c = Recongnizer()
    imgtype = {'key1': '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', 'key2': '2018-10-16 11:10:21', 'key3': '7e4256d72e26933fb1d11e2c2731de57', 'key4': '03', 'key5': '2', 'type': {'info': '请输入验证码图片中蓝色文字', 'img': 'yzm_blue.png', 'typecode': 3}}

    result = c.recongnize(imgtype['type'], imgtype['key1'], )
    print(result)