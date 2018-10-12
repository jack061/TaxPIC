from my_random import *
from js_caller import *
from yzm_plugin import *
from fp_parser import FpParser
import requests
from urllib.parse import urlencode
import random
import time
import json
import re
import traceback
from fake_useragent import UserAgent
ua = UserAgent()

yzm_version = 'V1.0.06_001' # 还没变

tax_citys = { #不同城市查验机关有不同的网址，根据这个去构造验证码图片和查验信息请求URL
        '1100':{'code':'1100','sfmc':'北京','Ip':'https://zjfpcyweb.bjsat.gov.cn:443','address':'https://zjfpcyweb.bjsat.gov.cn:443'},
        '1200':{'code':'1200','sfmc':'天津','Ip':'https://fpcy.tjsat.gov.cn:443','address':'https://fpcy.tjsat.gov.cn:443'},
        '1300':{'code':'1300','sfmc':'河北','Ip':'https://fpcy.he-n-tax.gov.cn:82','address':'https://fpcy.he-n-tax.gov.cn:82'},
        '1400':{'code':'1400','sfmc':'山西','Ip':'https://fpcy.tax.sx.cn:443','address':'https://fpcy.tax.sx.cn:443'},
        '1500':{'code':'1500','sfmc':'内蒙古','Ip':'https://fpcy.nm-n-tax.gov.cn:443','address':'https://fpcy.nm-n-tax.gov.cn:443'},
        '2100':{'code':'2100','sfmc':'辽宁','Ip':'https://fpcy.tax.ln.cn:443','address':'https://fpcy.tax.ln.cn:443'},
        '2102':{'code':'2102','sfmc':'大连','Ip':'https://fpcy.dlntax.gov.cn:443','address':'https://fpcy.dlntax.gov.cn:443'},
        '2200':{'code':'2200','sfmc':'吉林','Ip':'https://fpcy.jl-n-tax.gov.cn:4432','address':'https://fpcy.jl-n-tax.gov.cn:4432'},
        '2300':{'code':'2300','sfmc':'黑龙江','Ip':'https://fpcy.hl-n-tax.gov.cn:443','address':'https://fpcy.hl-n-tax.gov.cn:443'},
        '3100':{'code':'3100','sfmc':'上海','Ip':'https://fpcyweb.tax.sh.gov.cn:1001','address':'https://fpcyweb.tax.sh.gov.cn:1001'},
        '3200':{'code':'3200','sfmc':'江苏','Ip':'https://fpdk.jsgs.gov.cn:80','address':'https://fpdk.jsgs.gov.cn:80'},
        '3300':{'code':'3300','sfmc':'浙江','Ip':'https://fpcyweb.zjtax.gov.cn:443','address':'https://fpcyweb.zjtax.gov.cn:443'},
        '3302':{'code':'3302','sfmc':'宁波','Ip':'https://fpcy.nb-n-tax.gov.cn:443','address':'https://fpcy.nb-n-tax.gov.cn:443'},
        '3400':{'code':'3400','sfmc':'安徽','Ip':'https://fpcy.ah-n-tax.gov.cn:443','address':'https://fpcy.ah-n-tax.gov.cn:443'},
        '3500':{'code':'3500','sfmc':'福建','Ip':'https://fpcyweb.fj-n-tax.gov.cn:443','address':'https://fpcyweb.fj-n-tax.gov.cn:443'},
        '3502':{'code':'3502','sfmc':'厦门','Ip':'https://fpcy.xm-n-tax.gov.cn','address':'https://fpcy.xm-n-tax.gov.cn'},
        '3600':{'code':'3600','sfmc':'江西','Ip':'https://fpcy.jxgs.gov.cn:82','address':'https://fpcy.jxgs.gov.cn:82'},
        '3700':{'code':'3700','sfmc':'山东','Ip':'https://fpcy.sd-n-tax.gov.cn:443','address':'https://fpcy.sd-n-tax.gov.cn:443'},
        '3702':{'code':'3702','sfmc':'青岛','Ip':'https://fpcy.qd-n-tax.gov.cn:443','address':'https://fpcy.qd-n-tax.gov.cn:443'},
        '4100':{'code':'4100','sfmc':'河南','Ip':'https://fpcy.ha-n-tax.gov.cn','address':'https://fpcy.ha-n-tax.gov.cn'},
        '4200':{'code':'4200','sfmc':'湖北','Ip':'https://fpcy.hb-n-tax.gov.cn:443','address':'https://fpcy.hb-n-tax.gov.cn:443'},
        '4300':{'code':'4300','sfmc':'湖南','Ip':'https://fpcy.hntax.gov.cn:8083','address':'https://fpcy.hntax.gov.cn:8083'},
        '4400':{'code':'4400','sfmc':'广东','Ip':'https://fpcy.gd-n-tax.gov.cn:443','address':'https://fpcy.gd-n-tax.gov.cn:443'},
        '4403':{'code':'4403','sfmc':'深圳','Ip':'https://fpcy.szgs.gov.cn:443','address':'https://fpcy.szgs.gov.cn:443'},
        '4500':{'code':'4500','sfmc':'广西','Ip':'https://fpcy.gxgs.gov.cn:8200','address':'https://fpcy.gxgs.gov.cn:8200'},
        '4600':{'code':'4600','sfmc':'海南','Ip':'https://fpcy.hitax.gov.cn:443','address':'https://fpcy.hitax.gov.cn:443'},
        '5000':{'code':'5000','sfmc':'重庆','Ip':'https://fpcy.cqsw.gov.cn:80','address':'https://fpcy.cqsw.gov.cn:80'},
        '5100':{'code':'5100','sfmc':'四川','Ip':'https://fpcy.sc-n-tax.gov.cn:443','address':'https://fpcy.sc-n-tax.gov.cn:443'},
        '5200':{'code':'5200','sfmc':'贵州','Ip':'https://fpcy.gz-n-tax.gov.cn:80','address':'https://fpcy.gz-n-tax.gov.cn:80'},
        '5300':{'code':'5300','sfmc':'云南','Ip':'https://fpcy.yngs.gov.cn:443','address':'https://fpcy.yngs.gov.cn:443'},
        '5400':{'code':'5400','sfmc':'西藏','Ip':'https://fpcy.xztax.gov.cn:81','address':'https://fpcy.xztax.gov.cn:81'},
        '6100':{'code':'6100','sfmc':'陕西','Ip':'https://fpcyweb.sn-n-tax.gov.cn:443','address':'https://fpcyweb.sn-n-tax.gov.cn:443'},
        '6200':{'code':'6200','sfmc':'甘肃','Ip':'https://fpcy.gs-n-tax.gov.cn:443','address':'https://fpcy.gs-n-tax.gov.cn:443'},
        '6300':{'code':'6300','sfmc':'青海','Ip':'https://fpcy.qh-n-tax.gov.cn:443','address':'https://fpcy.qh-n-tax.gov.cn:443'},
        '6400':{'code':'6400','sfmc':'宁夏','Ip':'https://fpcy.nxgs.gov.cn:443','address':'https://fpcy.nxgs.gov.cn:443'},
        '6500':{'code':'6500','sfmc':'新疆','Ip':'https://fpcy.xj-n-tax.gov.cn:443','address':'https://fpcy.xj-n-tax.gov.cn:443'}
        };





class Downloader:
    '''
    下载器, 输入请求url,下载器进行请求，返回请求的数据
    '''

    def request_data_from_url(self, url,method='get', post_data= {}, referer = None, user_agent = None, other_headers = {}, timeout = -1):

        ip = '%d.%d.%d.%d' % (random.choice(range(100,244)),random.choice(range(100,244)),random.choice(range(100,244)),random.choice(range(100,244)))

        if url.find("//") == 0:
            #没有标识协议，加http 协议标识
            url = 'http:' + url

        # 开始构造headers
        headers = {'X-Forwarded-For':ip}
        if user_agent: headers['User-Agent'] = user_agent
        if referer: headers['RefererAgent'] = referer
        headers.update(other_headers)

        req = requests.get(url, headers=headers, verify=False ,timeout = timeout if timeout > 0 else 1)

        data = req.text
        return data


class Checker:

        # 填写完了发票信息后前端后向后端发送请求，
        # {"key1":验证码图片base64码,
        # "key2":"2018-10-10 17:04:48",
        # "key3":"f30186fd85d4b2535890c182c3d3c1f4",
        # "key4":"00", 验证码类型
        # "key5":"2"}

        # 验证码的 key1 数据。如果属于这些内容，就是错误啦。最后一个999999 是异常捕获的。
        yzm_err_info = {
            '003': u'验证码请求次数过于频繁，请1分钟后再试！',
            '005': u"非法请求!",
            '010': u'网络超时，请重试！(01)',
            '024': u'24小时内验证码请求太频繁，请稍后再试',
            '016': u'服务器接收的请求太频繁，请稍后再试',
            '020': u'由于查验行为异常，涉嫌违规，当前无法使用查验服务',
            'fpdmerr': u'请输入合法发票代码',
            }

        # 验证码图片类型
        yzm_info = {
            '00': {'info': u'请输入验证码文字', 'img': 'yzm_all.png', 'typecode': 0},
            '01': {'info': u'请输入验证码图片中红色文字', 'img': 'yzm_red.png', 'typecode': 1},
            '02': {'info': u'请输入验证码图片中黄色文字', 'img': 'yzm_yellow.png', 'typecode': 2},
            '03': {'info': u'请输入验证码图片中蓝色文字', 'img': 'yzm_blue.png', 'typecode': 3}
            }


        def __init__(self):
            # 保持cookies # 怎么做？
            self.downloader = Downloader()
            pass


        def _get_swjg_from_fpdm(self, fpdm):
            '''
            根据 fpdm 获取其所属税务机关的信息，用于构造请求url
            :param fpdm: 发票代码
            :return:对应的税务机关信息
            '''
            if len(fpdm) == 12:
                dqdm = fpdm[1:5]
            else:
                dqdm = fpdm[0:4]
            if (dqdm != "2102" and dqdm != "3302" and dqdm != "3502" and dqdm != "3702" and dqdm != "4403"):
                dqdm = dqdm[0:2] + "00"
            return tax_citys.get(dqdm)


        def checkFpdmIsOK(self, fpdm):
            '''
            检查fpdm是否符合对应的格式
            :param fpdm: 发票代码
            :return: Boolean : true or false
            '''
            if not fpdm: return False
            if len(fpdm) != 10 and len(fpdm) != 12: return False
            if not fpdm.isdecimal(): return False
            if not self._get_swjg_from_fpdm(fpdm): return False
            if FpParser().get_fplx_from_fpdm(fpdm)[0] == '99': return False
            return True


        def _get_yzm_image(self, fpdm, fphm):
            """
            构造请求url, 获取验证码图片
            :param fpdm:
            :param fphm:
            :return:
            """
            swjg = self._get_swjg_from_fpdm(fpdm)
            # 根据发票代码查询发票机关
            if not swjg:
                # 如果查不到对应的税务机关，就认为发票代码有误
                return False, {'err': '错误的发票代码！001'}

            nowtime = str(int(time.time() * 1000))

            # 观察规律，构造请求验证码图片的url
            url = '%s/WebQuery/yzmQuery?callback=jQuery1%s_1%s&fpdm=%s&fphm=%s&r=0.%s&_=1%s&v=%s&nowtime=%s&area=%s&publickey=%s' % \
                (swjg['Ip'], getNumRandomStr(21), getNumRandomStr(12), fpdm, fphm, getNumRandomStr(16),
                getNumRandomStr(12),
                yzm_version, nowtime, swjg['code'], ckYZM(fpdm, nowtime))

            response = {}
            try:
                print('get yzm url:', url)
                # 根据请求URL，下载验证码图片
                data = self.downloader.down_date_from_url(url)
                # 取出返回的json字符串
                data = re.findall('\(({.*})\)$', data)[0]
                response = json.loads(data)
                response['swjg'] = swjg
                if response['key1'] in Checker.yzm_err_info:
                    # key1 如果是这些，就说明发生了错误。否则应当是base64形式的图片数据
                    response['errorinfo'] = Checker.yzm_err_info[response['key1']]
                    response['errorcode'] = response['key1']
                    print(fpdm, url, response['errorinfo'])
                    return False, response

                response['type'] = Checker.yzm_info[response['key4']]
                return True, response

            except Exception as e:
                # 输出详细的错误信息，便于调试
                print(str(e))
                print(traceback.format_exc())
                return (False, {'errorinfo': str(e), 'errorcode': -999, 'swjg': swjg})



        def _checkFp(self, fpdm, fphm, kprq, fpje_or_jym, yzm, index_yzm_key3, yzmsj_key2):
            """
            识别了验证码以后，根据以上信息构造发票查验url，返回查验信息
            # https://fpcy.szgs.gov.cn/WebQuery/query?callback=jQuery110206557166752159265_1504944292710
            #   &fpdm=4403172130&fphm=11868624&kprq=20170906&fpje=296.23
            #   &fplx=01&yzm=mm&yzmSj=2017-09-09+15%3A55%3A52&
            #   index=e4d2a91819b291b0266616bd4c951fd4&iv=345cd6318f18df6452f7a24a35187f4b&salt=9d02356d63bae18abbb8b583258161a1&_=1504944292712
            :param fpdm:
            :param fphm:
            :param kprq:
            :param fpje_or_jym:
            :param yzm:
            :param index_yzm_key3:
            :param yzmsj_key2:
            :return:
            """
            parser = FpParser()

            # 用于解析返回的加密数据
            iv = getLittleHexRandomStr(32)
            salt = getLittleHexRandomStr(32)  # 盐

            fplx = parser.get_fplx_from_fpdm(fpdm)

            if fplx[0] == '10' or fplx[0] == '12':
                # 电子发票使用校验码后六位，其他发票使用开票金额
                if len(fpje_or_jym) > 6: fpje_or_jym = fpje_or_jym[-6:]
            if len(fpje_or_jym) == 20: fpje_or_jym = fpje_or_jym[-6:]

            request_info = {
                "key1": fpdm,
                "key2": fphm,
                "key3": kprq,
                "key4": fpje_or_jym,
                "fplx": fplx[0],
                "index": index_yzm_key3,
                "publickey": ckFP(fpdm, fphm, fpje_or_jym, kprq, yzmsj_key2, yzm), # 这个加密他是怎么看出来的？
                "yzm": yzm,
                "yzmSj": yzmsj_key2,
            }


            swjg = self._get_swjg_from_fpdm(fpdm)
            if not swjg:
                return False, None

            params = urlencode(request_info)


            url = u'%s/WebQuery/vatQuery?callback=jQuery1%s_1530868658752&%s&area=%s&_=15%s' \
                % (swjg['Ip'], getNumRandomStr(21), params, swjg['code'], getNumRandomStr(11))

            response = {}
            raw_data = ''
            try:
                data = self.downloader.down_date_from_url(url)
                # print len(data),data
                if data == '':
                    return False, {'errorinfo': '核验返回为空', 'swjg': swjg['sfmc'], 'errorcode': '-999'}

                data = re.findall('\(({.*})\)$', data)[0]

                raw_data = data

                data = data.decode('gbk')
                response = json.loads(data)
                response['swjg'] = swjg
                bOK = False

                cyjgdm = response['key1']
                # 查验结果代码

                if cyjgdm == "001":
                    bOK = True
                elif cyjgdm in Checker.fp_err_info:
                    response['errorinfo'] = Checker.fp_err_info[cyjgdm]
                else:
                    response['errorinfo'] = '其他错误!'
                if not bOK:
                    return False, {'errorinfo': response['errorinfo'], 'swjg': swjg['sfmc'], 'errorcode': cyjgdm}
                if bOK:
                    ret = parser.ParserFpinfo(data, fpdm, fphm, swjg['sfmc'], yzmsj_key2)
                    ret['fplx'] = fplx
                    ret['rawdata'] = raw_data

                    return bOK, ret

            except Exception as e:
                print(str(e))
                print(traceback.format_exc())
                return (False, {'errorinfo': str(e), 'swjg': swjg['sfmc'], 'errorcode': '-999'})

        def CheckFp(self, fpdm, fphm, kprq, jym_or_kjje, yzm_plugin = ConsoleYzmPlugin()):
            '''
            发票查验入口
            :param fpdm:
            :param fphm:
            :param kprq:
            :param jym_or_kjje:
            :param yzm_plugin: 专门处理识别验证码的类
            :return:
            '''
            bOK, ret_img = self._get_yzm_image(fpdm, fphm)
            if not bOK:
                print(str(ret_img))
                # 标示在验证码环节出现错误
                ret_img['err_type'] = 'yzm'
                return bOK, ret_img

            yzm = yzm_plugin.get(ret_img['type'], ret_img['key1'])

            bOK, ret = self._checkFp(fpdm, fphm, kprq, jym_or_kjje, yzm, ret_img['key3'], ret_img['key2'])
            if not bOK:
                # 标示在发票验证环节出现错误
                ret['err_type'] = 'fp'
            yzm_plugin.report(False if ('errorcode' in ret and (ret['errorcode'] == '008')) else True)
            print(str(ret))
            return bOK, ret

        def printFpxx(self, fpxx):
            if not fpxx[0]:
                for x in fpxx[1]:
                    print(fpxx[1][x])
                return
            FpParser().printFpxx(fpxx[1])
