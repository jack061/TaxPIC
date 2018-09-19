from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import base64


def inputToGetPic(browser):
    inputFpdm = browser.find_element_by_xpath('//*[@id="fpdm"]')
    inputFpdm.send_keys('033001700211')

    inputFphm = browser.find_element_by_xpath('//*[@id="fphm"]')
    inputFphm.send_keys('58089105')

    #  不输入以下两个值也能加载验证码,但是验证码会等待3秒左右才能加载
    inputKprq = browser.find_element_by_xpath('//*[@id="kprq"]')
    inputKprq.send_keys('20180410')

    inputKjje = browser.find_element_by_xpath('//*[@id="kjje"]')  # 校验码/金额都是这个xpath
    inputKjje.send_keys('123456')

    time.sleep(0.2)  # 这时候就会出现校验码，然后就可以进行下载识别

    pageSource = browser.page_source
    bsObj = bs(pageSource, 'lxml')

    yzminfo = bsObj.find(id = "yzminfo")
    filename = (yzminfo.text.replace(' ', '')) + '.png'
    filename = filename.replace('\n', '')

    # print('pagesource', pageSource)
    imgBase64 = bsObj.find(id="yzm_img").get('src')[22:]

    # print(imgBase64)
    imgdata = base64.b64decode(imgBase64)

    return imgdata, filename


def saveImg(imgdata, filename):
    if '中' in filename:  # 除去 识别所有文字 的情况，因为无法二值化
        file = open('D:/pic/' + filename, 'wb')  # 其实png、jpg都行
        file.write(imgdata)
        file.close()


if __name__ == '__main__':
    #
    # webdriverExecutablePath = r'D:\webdrivers\phantomjs-2.1.1-windows\bin\phantomjs.exe'
    # browser = webdriver.PhantomJS(executable_path=webdriverExecutablePath)

    # browser = webdriver.Edge(executable_path = 'D:/MicrosoftWebDriver.exe')
    browser = webdriver.Chrome(executable_path='D:/webdrivers/chromedriver.exe')

    browser.get("https://inv-veri.chinatax.gov.cn/")  # Load page
    inputToGetPic(browser)
    filename = '请输入验证码文字.png'
    while filename == '请输入验证码文字.png':
        browser.refresh()
        imgdata, filename = inputToGetPic(browser)

    # saveImg(imgdata, filename)

    # 已保存要识别的验证码，下面开始优化切分



    # browser.close()