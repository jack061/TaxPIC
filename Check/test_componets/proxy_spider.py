import requests
import re
from selenium import webdriver
from pyquery import PyQuery as pq
from settings import PROXY_PATH , PHANTOMJS_PATH


def getProxies(proxy_websites):
    proxies = []
    for url in proxy_websites:
        driver = webdriver.PhantomJS(executable_path = PHANTOMJS_PATH)
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
            with open(PROXY_PATH,'a') as f:
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

    proxy_websites = ['http://www.xicidaili.com/nn/1']

    proxies = getProxies(proxy_websites)

    print(len(proxies))
    print(proxies)

    testProxy(proxies)

