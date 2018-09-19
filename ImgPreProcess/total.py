from selenium import webdriver
import torch
from DownloadCAPTCHA import *
from ImgPreProcess import *
from torch.utils.data.dataloader import DataLoader
import torchvision
from torchvision import transforms
from Identity import identity

browser = webdriver.PhantomJS(executable_path=r'D:\webdrivers\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    
# browser = webdriver.Edge(executable_path='D:/webdrivers/MicrosoftWebDriver.exe')
# browser = webdriver.Chrome(executable_path='D:/webdrivers/chromedriver.exe')

browser.get("https://inv-veri.chinatax.gov.cn/")  # Load page
inputToGetPic(browser)

filename = '请输入验证码文字.png'
while filename == '请输入验证码文字.png':  # 跳过要输入图中所有文字的验证码，因为找不到好的方法二值化
    browser.refresh()
    imgdata, filename = inputToGetPic(browser)
saveImg(imgdata, filename)
# 已保存要识别的验证码，下面开始优化、切分
imgPreProcess(filename)


networkPath = r'D:\Code\TaxPIC\model\(60)-net.pkl'
ImageFolder = r'D:\pic\切分'
identity(networkPath, ImageFolder)

browser.close()