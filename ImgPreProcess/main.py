# 神经网络使用
import torch
from torch.utils.data.dataloader import DataLoader
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms

# 爬虫部分使用
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import base64

import re
import os

import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片


from ImgPreProcess import *


# 初始化一个selenium的webdriver传入，利用phantomjs，自动在当前页面填写发票信息，获取验证码图片信息
def inputToGetPic(driver, fpInfo = None):
    
    fpInfo = dict({'fpdm':'033001700211','fphm':'58089105','kprq':'20180410','kjje':'123456'})

    inputFpdm = driver.find_element_by_xpath('//*[@id="fpdm"]')
    inputFpdm.send_keys(fpInfo['fpdm'])

    inputFphm = driver.find_element_by_xpath('//*[@id="fphm"]')
    inputFphm.send_keys(fpInfo['fphm'])

    # 不输入以下两个值也能加载验证码,但是验证码会等待3秒左右才能加载
    inputKprq = driver.find_element_by_xpath('//*[@id="kprq"]')
    inputKprq.send_keys(fpInfo['kprq'])

    inputKjje = driver.find_element_by_xpath('//*[@id="kjje"]')  # 校验码/金额都是这个xpath
    inputKjje.send_keys(fpInfo['kjje'])

    time.sleep(0.5)  # 这时候就会出现校验码，然后就可以进行下载识别

    pageSource = driver.page_source
    bsObj = bs(pageSource, 'lxml')
    yzminfo = bsObj.find(id = "yzminfo")
    filename = (yzminfo.text.replace(' ', '').replace('\n', '')) + '.png'

    imgBase64 = bsObj.find(id="yzm_img").get('src')[22:]
    imgdata = base64.b64decode(imgBase64)

    return imgdata, filename


def saveImg(imgdata, filename):
    if '中' in filename:  # 除去 识别所有文字 的情况，因为无法二值化
        file = open('D:/pic/' + filename, 'wb')  # 其实png、jpg都行
        file.write(imgdata)
        file.close()


class Cap_Net(nn.Module):  # pytorch的bug，自定义class保存后，如果在新的文件里load，还需要重新定义class

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


def find_classes(dataset_dir):  
    # pytorch的DatasetFolder方法在读取数据集文件时会对标签做索引以输入网络
    # 我们需要根据索引找到其对应的label，这里对原数据集文件做反向的“索引：标签”映射，便于后续查找
    classes = [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]
    classes.sort()
    idx_to_classes = {i: classes[i] for i in range(len(classes))}
    return idx_to_classes


def parseResult(result, idx_to_class):
    p1 = re.compile(r'[[](.*?)[]]', re.S)  #最小匹配
    results = re.findall(p1, result)
    results = results[0].split(',')
    r = []
    for i in results:
        r.append(idx_to_class[int(i)])
    return  r


def identity(networkPath, ImageFolder):
    net = Cap_Net()  # 初始化

    net = torch.load(networkPath, )

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

    return ("结果：" + result)


if __name__ == '__main__':
    
    dataset_dir = 'D:\Code\TaxPIC\PIC\预处理'

    driver = webdriver.PhantomJS(executable_path=r'D:\webdrivers\phantomjs-2.1.1-windows\bin\phantomjs.exe')

    # 调试时用可视化的chrome webdriver或者edge webdriver
    # browser = webdriver.Edge(executable_path='D:/webdrivers/MicrosoftWebDriver.exe')
    # browser = webdriver.Chrome(executable_path='D:/webdrivers/chromedriver.exe')

    driver.get("https://inv-veri.chinatax.gov.cn/")  # Load page
    imgdata, filename = inputToGetPic(driver)

    while filename == '请输入验证码文字.png':  # 跳过要输入图中所有文字的验证码，因为找不到好的方法二值化
        print(filename)
        driver.refresh()
        imgdata, filename = inputToGetPic(driver)

    saveImg(imgdata, filename)  # 已保存要识别的验证码，下面开始优化、切分
    imgPreProcess(filename)


    networkPath = r'D:\Code\TaxPIC\model\(69)-net.pkl'
    ImageFolder = r'D:\pic\切分'
    result = identity(networkPath, ImageFolder)
    idx_to_classes = find_classes(dataset_dir)
    result = (parseResult(result,idx_to_classes))
    print(result)

    driver.close()