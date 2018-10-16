from my_random import *
import time
from js_caller import *
import re
import  json
from  downloader import Downloader

def test():
    while True:
        try:
            yzm_version = 'V1.0.06_001' # 还没变

            nowtime = str(int(time.time() * 1000))
            head_url = 'https://zjfpcyweb.bjsat.gov.cn:443'
            fpdm = '044031700111'
            fphm = '28478760'
            url = '%s/WebQuery/yzmQuery?callback=jQuery1%s_1%s&fpdm=%s&fphm=%s&r=0.%s&_=1%s&v=%s&nowtime=%s&area=%s&publickey=%s' % \
                  (head_url, getNumRandomStr(21), getNumRandomStr(12), fpdm, fphm, getNumRandomStr(16),getNumRandomStr(12),
                yzm_version, nowtime, '1100', ckYZM(fpdm, nowtime))
            print(url)
            d  = Downloader()
            data = d.request_data_from_url(url)
            data = re.findall('\(({.*})\)$', data)[0]
            ret = json.loads(data)

            # 我们的网络暂时无法对随机底色黑色字符的验证码图片做较好的二值化，所以重来，直到请求到
            if ret['key4'] == '00':
                print('all')
                continue

            return (ret)

        except Exception as e:
            pass
        # 验证码图片类型
yzm_info = {
    '00': {'info': u'请输入验证码文字', 'img': 'yzm_all.png', 'typecode': 0},
    '01': {'info': u'请输入验证码图片中红色文字', 'img': 'yzm_red.png', 'typecode': 1},
    '02': {'info': u'请输入验证码图片中黄色文字', 'img': 'yzm_yellow.png', 'typecode': 2},
    '03': {'info': u'请输入验证码图片中蓝色文字', 'img': 'yzm_blue.png', 'typecode': 3}
}
ret = test()
ret['type'] = yzm_info[ret['key4']]

print(ret)