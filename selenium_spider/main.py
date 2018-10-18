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
from lxml import etree
import re
import os
from random import choice

import shutil
from ImgPreProcess import *

errormessage = {
    '验证码请求次数过于频繁，请1分钟后再试！':0,
    '验证码错误!':1,
}

# 初始化一个selenium的webdriver传入，利用phantomjs，自动在当前页面填写发票信息，获取验证码图片信息
# 验证码URL： https://fpcy.szgs.gov.cn/WebQuery/yzmQuery?callback=jQuery1102077129486062673_1538982596672&fpdm=044031700111&fphm=28477743&r=0.7576049859494576&v=V1.0.06_001&nowtime=1539049984487&area=4403&publickey=21BC9BFA288CF801B66C26801BF16E5E&_=1538982596677
# baseURL是根据发票的税务机关，产生不同的，后面的结构都一样
def inputToGetPic(driver, fpInfo = None):

    fpinfo = [
        {'fpdm': '044031700111', 'fphm': '28477743', 'kprq': '20171129', 'kjje': '227858'},
        {'fpdm': '033001700211', 'fphm': '58089105', 'kprq': '20180410', 'kjje': '604420'},
        {'fpdm': '033001700211', 'fphm': '17099263', 'kprq': '20171201', 'kjje': '336134'},
        {'fpdm': '044031700111', 'fphm': '28478760', 'kprq': '20171129', 'kjje': '737421'},
    ]

    if fpInfo is None:
        fpInfo = fpinfo[0]

    inputFpdm = driver.find_element_by_xpath('//*[@id="fpdm"]')
    inputFpdm.send_keys(fpInfo['fpdm'])

    inputFphm = driver.find_element_by_xpath('//*[@id="fphm"]')
    inputFphm.send_keys(fpInfo['fphm'])

    # 不输入以下两个值也能加载验证码,但是验证码会多等待3秒左右才能加载
    inputKprq = driver.find_element_by_xpath('//*[@id="kprq"]')
    inputKprq.send_keys(fpInfo['kprq'])

    # 校验码/金额都是这个xpath
    inputKjje = driver.find_element_by_xpath('//*[@id="kjje"]')
    inputKjje.send_keys(fpInfo['kjje'])

    time.sleep(6)  # 这时候就会出现校验码，然后就可以进行下载识别

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

    return ("结果： " + result)


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

def main(driver, networkPath = None, ImageFolder = None, dataset_dir = None):

    if  os.path.exists("D:\pic\切分\\1"):
        shutil.rmtree("D:\pic\切分\\1")

    # networkPath = r'D:\Code\TaxPIC\model\(69)-net.pkl'
    # ImageFolder = r'D:\pic\切分'  # 切分后的图片的存放地址
    # dataset_dir = 'D:\Code\TaxPIC\PIC\预处理'

    imgdata, filename = inputToGetPic(driver)

    while filename == '请输入验证码文字.png':  # 跳过要输入图中所有文字的验证码，因为找不到好的方法二值化
        print(filename)
        driver.refresh()
        imgdata, filename = inputToGetPic(driver)

    saveImg(imgdata, filename)  # 已保存要识别的验证码，下面开始优化、切分
    ImgPreProcesser.ImgPreProcess(filename)


    result = identity(networkPath, ImageFolder)
    idx_to_classes = find_classes(dataset_dir)
    result =''.join(parseResult(result,idx_to_classes))
    print('验证码'+ result)

    yzm = driver.find_element_by_xpath('//*[@id="yzm"]')
    yzm.send_keys(result)
    # 验证码识别成功后就进行填写提交，获取查验信息
    clickCheckButton = driver.find_element_by_xpath('//*[@id="checkfp"]')
    clickCheckButton.click()
    # 原平台使用的是构造请求url的方式直接获取相应json，这个方法虽然繁琐但在网络上比较有效率

    return driver

# class browser(object):
#
#     def __init__(self, driverpath = None, url = None ):
#
#         if driverpath is None:
#             # 调试时用可视化的chrome webdriver或者edge webdriver
#
#
#         self.driver = webdriver.Chrome(executable_path= self.driverPath)
#
#     def Visit(self, url = None):
#         if url = None:
#
#         self.driver.get("https://inv-veri.chinatax.gov.cn/")
#

if __name__ == '__main__':

    total = 0
    wrong = 0

    networkPath = 'D:\Code\TaxPIC\model\(69)-net.pkl'
    ImageFolder = 'D:\pic\切分'  # 切分后的图片的存放地址
    dataset_dir = 'D:\Code\TaxPIC\PIC\预处理'

    url = "https://inv-veri.chinatax.gov.cn/"

    # driverPath = r'D:\webdrivers\phantomjs-2.1.1-windows\bin\phantomjs.exe'
    # driverPath = r'D:/webdrivers/MicrosoftWebDriver.exe'
    driverPath = r'D:/webdrivers/chromedriver.exe'

    driver = webdriver.Chrome(executable_path= driverPath)

    driver.get(url)  # Load page
    driver = main(driver, networkPath, ImageFolder, dataset_dir)
    total = total + 1

    driver.switch_to_default_content()
    selector = etree.HTML(driver.page_source)
    flag = selector.xpath('//*[@id="popup_message"]/text()')
    if len(flag) > 0:
        flag = str(flag[0])
    print('flag:', flag)

    while flag is None:
        try:
            if errormessage[flag] == 0:
                time.sleep(100)

            wrong = wrong + 1
            driver.refresh()
            driver = main(driver, networkPath, ImageFolder, dataset_dir)
            time.sleep(10)
            total = total + 1

            driver.switch_to_default_content()
            selector = etree.HTML(driver.page_source)
            flag = selector.xpath('//*[@id="popup_message"]/text()')
            if len(flag) > 0:
                flag = str(flag[0])
            print(flag)

        except Exception as e:
            break

    driver.switch_to_default_content()
    print(driver.page_source)
    print('正确率: ' + str(float((1 - float(wrong/total))*100)) + '%' , wrong, total)
    # driver.close()