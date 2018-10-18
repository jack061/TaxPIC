import requests
import re
from selenium import webdriver
from pyquery import PyQuery as pq


def getProxies(proxy_websites):
    proxies = []
    for url in proxy_websites:
        driver = webdriver.PhantomJS(executable_path = r'D:\phantomjs\bin\phantomjs.exe' )
        driver.get(url)
        pqObj = pq(driver.page_source)
        trs = pqObj('tr').items()

        for tr in trs:
            for td in pq(tr)('td').items():
                ip = re.findall(r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)', td.text())
                if len(ip) >0:
                    port = td.next().text()
                    proxies.append('http://'+ str(ip[0]) + ':' + str(port))
    driver.close()
    return (proxies)

def testProxy(proxies, target ='https://www.baidu.com'):
    for proxy in proxies:
        res = requests.get(target, proxies = {'http' : proxy})
        if str(res) == '<Response [200]>':
            print('success with : ', proxy)
            with open(r'D:\Code\TaxPIC\ImgPreProcess\proxies.txt','a') as f:
                f.write(proxy + '\n')
        else:
            print('failed with : ', proxy)




if __name__ == '__main__':
    # proxy_website = 'http://www.xicidaili.com/nn/'
    # proxy_websites = []
    # for i in range(1,100):
    #     url = proxy_website + str(i)
    #     proxy_websites.append(url)
    #
    # print(proxy_websites)

    proxy_websites = ['http://www.xicidaili.com/nn/1', 'http://www.xicidaili.com/nn/2', 'http://www.xicidaili.com/nn/3',
     'http://www.xicidaili.com/nn/4', 'http://www.xicidaili.com/nn/5', 'http://www.xicidaili.com/nn/6',
     'http://www.xicidaili.com/nn/7', 'http://www.xicidaili.com/nn/8', 'http://www.xicidaili.com/nn/9',
     'http://www.xicidaili.com/nn/10', 'http://www.xicidaili.com/nn/11', 'http://www.xicidaili.com/nn/12',
     'http://www.xicidaili.com/nn/13', 'http://www.xicidaili.com/nn/14', 'http://www.xicidaili.com/nn/15',
     'http://www.xicidaili.com/nn/16', 'http://www.xicidaili.com/nn/17', 'http://www.xicidaili.com/nn/18',
     'http://www.xicidaili.com/nn/19', 'http://www.xicidaili.com/nn/20', 'http://www.xicidaili.com/nn/21',
     'http://www.xicidaili.com/nn/22', 'http://www.xicidaili.com/nn/23', 'http://www.xicidaili.com/nn/24',
     'http://www.xicidaili.com/nn/25', 'http://www.xicidaili.com/nn/26', 'http://www.xicidaili.com/nn/27',
     'http://www.xicidaili.com/nn/28', 'http://www.xicidaili.com/nn/29', 'http://www.xicidaili.com/nn/30',
     'http://www.xicidaili.com/nn/31', 'http://www.xicidaili.com/nn/32', 'http://www.xicidaili.com/nn/33',
     'http://www.xicidaili.com/nn/34', 'http://www.xicidaili.com/nn/35', 'http://www.xicidaili.com/nn/36',
     'http://www.xicidaili.com/nn/37', 'http://www.xicidaili.com/nn/38', 'http://www.xicidaili.com/nn/39',
     'http://www.xicidaili.com/nn/40', 'http://www.xicidaili.com/nn/41', 'http://www.xicidaili.com/nn/42',
     'http://www.xicidaili.com/nn/43', 'http://www.xicidaili.com/nn/44', 'http://www.xicidaili.com/nn/45',
     'http://www.xicidaili.com/nn/46', 'http://www.xicidaili.com/nn/47', 'http://www.xicidaili.com/nn/48',
     'http://www.xicidaili.com/nn/49', 'http://www.xicidaili.com/nn/50', 'http://www.xicidaili.com/nn/51',
     'http://www.xicidaili.com/nn/52', 'http://www.xicidaili.com/nn/53', 'http://www.xicidaili.com/nn/54',
     'http://www.xicidaili.com/nn/55', 'http://www.xicidaili.com/nn/56', 'http://www.xicidaili.com/nn/57',
     'http://www.xicidaili.com/nn/58', 'http://www.xicidaili.com/nn/59', 'http://www.xicidaili.com/nn/60',
     'http://www.xicidaili.com/nn/61', 'http://www.xicidaili.com/nn/62', 'http://www.xicidaili.com/nn/63',
     'http://www.xicidaili.com/nn/64', 'http://www.xicidaili.com/nn/65', 'http://www.xicidaili.com/nn/66',
     'http://www.xicidaili.com/nn/67', 'http://www.xicidaili.com/nn/68', 'http://www.xicidaili.com/nn/69',
     'http://www.xicidaili.com/nn/70', 'http://www.xicidaili.com/nn/71', 'http://www.xicidaili.com/nn/72',
     'http://www.xicidaili.com/nn/73', 'http://www.xicidaili.com/nn/74', 'http://www.xicidaili.com/nn/75',
     'http://www.xicidaili.com/nn/76', 'http://www.xicidaili.com/nn/77', 'http://www.xicidaili.com/nn/78',
     'http://www.xicidaili.com/nn/79', 'http://www.xicidaili.com/nn/80', 'http://www.xicidaili.com/nn/81',
     'http://www.xicidaili.com/nn/82', 'http://www.xicidaili.com/nn/83', 'http://www.xicidaili.com/nn/84',
     'http://www.xicidaili.com/nn/85', 'http://www.xicidaili.com/nn/86', 'http://www.xicidaili.com/nn/87',
     'http://www.xicidaili.com/nn/88', 'http://www.xicidaili.com/nn/89', 'http://www.xicidaili.com/nn/90',
     'http://www.xicidaili.com/nn/91', 'http://www.xicidaili.com/nn/92', 'http://www.xicidaili.com/nn/93',
     'http://www.xicidaili.com/nn/94', 'http://www.xicidaili.com/nn/95', 'http://www.xicidaili.com/nn/96',
     'http://www.xicidaili.com/nn/97', 'http://www.xicidaili.com/nn/98', 'http://www.xicidaili.com/nn/99']

    proxies = getProxies(proxy_websites)

    print(len(proxies))
    print(proxies)

    testProxy(proxies)

