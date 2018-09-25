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

import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片



from ImgPreProcess import *


# 初始化一个selenium的webdriver传入，利用phantomjs，自动在当前页面填写发票信息，获取验证码图片信息
def inputToGetPic(driver):

    inputFpdm = driver.find_element_by_xpath('//*[@id="fpdm"]')
    inputFpdm.send_keys('033001700211')

    inputFphm = driver.find_element_by_xpath('//*[@id="fphm"]')
    inputFphm.send_keys('58089105')

    # 不输入以下两个值也能加载验证码,但是验证码会等待3秒左右才能加载
    inputKprq = driver.find_element_by_xpath('//*[@id="kprq"]')
    inputKprq.send_keys('20180410')

    inputKjje = driver.find_element_by_xpath('//*[@id="kjje"]')  # 校验码/金额都是这个xpath
    inputKjje.send_keys('123456')

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


def identity(networkPath, ImageFolder):
    net = Cap_Net()  # 初始化

    # net = torch.load_state_dict(torch.load(networkPath))
    net = torch.load(networkPath, )

    tranforms_test = transforms.Compose([  # 预定义图片转换规则

        transforms.ToTensor(),

    ])
    test_dataset = torchvision.datasets.ImageFolder(ImageFolder, transform=tranforms_test)
    test_data = DataLoader(test_dataset, )

    net.eval()

    outputs = net(test_data)  # net直接前向传播然后输出

    _, predicted = torch.max(outputs.data, 1)  # 返回的是交叉熵函数的最大概率预测。

    print("结果：" + str(predicted))


if __name__ == '__main__':

    driver = webdriver.PhantomJS(executable_path=r'D:\webdrivers\phantomjs-2.1.1-windows\bin\phantomjs.exe')

    # 调试用可视化的chrome webdriver或者edge webdriver
    # browser = webdriver.Edge(executable_path='D:/webdrivers/MicrosoftWebDriver.exe')
    # browser = webdriver.Chrome(executable_path='D:/webdrivers/chromedriver.exe')

    driver.get("https://inv-veri.chinatax.gov.cn/")  # Load page
    imgdata, filename = inputToGetPic(driver)

    while filename == '请输入验证码文字.png':  # 跳过要输入图中所有文字的验证码，因为找不到好的方法二值化
        driver.refresh()
        imgdata, filename = inputToGetPic(driver)

    saveImg(imgdata, filename)  # 已保存要识别的验证码，下面开始优化、切分
    imgPreProcess(filename)


    networkPath = r'D:\Code\TaxPIC\model\(69)-net.pkl'
    ImageFolder = r'D:\pic\切分'
    result = identity(networkPath, ImageFolder)


    clickCheckButton = driver.find_element_by_xpath('//*[@id="checkfp"]')

    driver.close()