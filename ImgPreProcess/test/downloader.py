import requests
import random
import re
from fake_useragent import UserAgent

'''
﻿Accept:*/*
Accept-Encoding:gzip, deflate, sdch, br
Accept-Language:zh-CN,zh;q=0.8
Connection:keep-alive
Cookie:JSESSIONID=2FxITeC1WlsU7QMGVNb9YtJsnkHRgIMc9GmkVvUJA8Q7B-8myOD6!224442884
Host:fpcy.sc-n-tax.gov.cn
Referer:https://inv-veri.chinatax.gov.cn/index.html
User-Agent:Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36


﻿Accept:*/*
Accept-Encoding:gzip, deflate, sdch, br
Accept-Language:zh-CN,zh;q=0.8
Connection:keep-alive
Cookie:_Jo0OQK=2D328867E4F20538B88BED04675F0B8719050D4BD338265E0A01ABA2801AC06EC54D29B61C08EB60A2A49125CD5B429D0EB8C77757FC322628093111D7D2E79C9B26C651370D49D584975E3F7BF535CAACC75E3F7BF535CAACC77ACC40F1DDABB60GJ1Z1OQ==
Host:inv-veri.chinatax.gov.cn
Referer:https://inv-veri.chinatax.gov.cn/cyjg10.html
User-Agent:Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
'''


class Downloader:
    '''
    下载器, 输入请求url,下载器进行请求，返回请求的数据
    '''

    def request_data_from_url(self, url, method='get', post_data={}, referer=None, user_agent=None, other_headers={}, timeout=-1):

        if user_agent is None:
            ua = UserAgent()
            user_agent = ua.random

        ip = '%d.%d.%d.%d' % (
        random.choice(range(100, 244)), random.choice(range(100, 244)), random.choice(range(100, 244)),
        random.choice(range(100, 244)))

        if url.find("//") == 0:
            # 没有标识协议，加http 协议标识
            url = 'http:' + url

        # 开始构造headers
        headers = {'X-Forwarded-For': ip}
        if user_agent: headers['User-Agent'] = user_agent
        if referer: headers['RefererAgent'] = referer
        headers.update(other_headers)

        req = requests.get(url, headers=headers, verify=False, timeout=timeout if timeout > 0 else 1)

        data = req.text
        return data


if __name__ == '__main__':
    url = 'https://fpcy.szgs.gov.cn/WebQuery/yzmQuery?callback=jQuery1102040826791579157495_1539162990824&fpdm=044031700111&fphm=28477743&r=0.5666531826434975&v=V1.0.06_001&nowtime=1539162996518&area=4403&publickey=73ADCEB1BBCFEDE788A12E4706A42014&_=1539162990826'
    data = Downloader().request_data_from_url(url)
    data = re.findall('\(({.*})\)$',data)[0]
    print (len(data),data)