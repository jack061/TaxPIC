from fp_parser import FpParser
from downloader import Downloader
from recognizer import Recongnizer
from my_random import *
from settings import yzm_version, tax_citys
import re
import traceback
from js_caller import *
from urllib.parse import urlencode
from yzm_plugin import *


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
              (swjg['Url'], getNumRandomStr(21), getNumRandomStr(12), fpdm, fphm, getNumRandomStr(16),
               getNumRandomStr(12),
               yzm_version, nowtime, swjg['code'], ckYZM(fpdm, nowtime))

        while True:
            try:
                print('get yzm url:', url)
                # 根据请求URL，下载验证码图片
                data = self.downloader.request_data_from_url(url)
                # 取出返回的json字符串
                data = re.findall('\(({.*})\)$', data)[0]
                ret = json.loads(data)
                ret['swjg'] = swjg
                if ret['key1'] in Checker.yzm_err_info:
                    # key1 如果是这些，就说明发生了错误。否则应当是base64形式的图片数据
                    ret['errorinfo'] = Checker.yzm_err_info[ret['key1']]
                    ret['errorcode'] = ret['key1']
                    print(fpdm, url, ret['errorinfo'])
                    return False, ret

                # 我们的网络暂时无法对随机底色黑色字符的验证码图片做较好的二值化，所以重来，直到请求到
                if ret['key4'] == '00':
                    continue

                ret['type'] = Checker.yzm_info[ret['key4']]
                return True, ret

            except Exception as e:
                # 输出详细的错误信息，便于调试
                print(str(e))
                print(traceback.format_exc())
                return (False, {'errorinfo': str(e), 'errorcode': -999, 'swjg': swjg})

    # 发票查验错误代码
    fp_err_info = {
        '002': u'超过该张发票当日查验次数(请于次日再次查验)!',
        '003': u'发票查验请求太频繁，请稍后再试！',
        '004': u'超过服务器最大请求数，请稍后访问!',
        '005': u'请求不合法!',
        '006': u'发票信息不一致',
        '007': u'验证码失效',
        '008': u'验证码错误',
        '009': u'查无此票',
        '010': u'网络超时，请重试！',
        '010_': u'网络超时，请重试！',
        '020': u'由于查验行为异常，涉嫌违规，当前无法使用查验服务！',
        'rqerr': u'当日开具发票可于次日进行查验'
    }

    def _checkFp(self, fpdm, fphm, kprq, fpje_or_jym, yzm, index_yzm_key3, yzmsj_key2):
        """
        识别了验证码以后，根据以上信息构造发票查验url，返回查验结果
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
            "publickey": ckFP(fpdm, fphm, fpje_or_jym, kprq, yzmsj_key2, yzm),  # 这个加密他是怎么看出来的？
            "yzm": yzm,
            "yzmSj": yzmsj_key2,
        }

        swjg = self._get_swjg_from_fpdm(fpdm)
        if not swjg:
            return False, None

        params = urlencode(request_info)

        url = u'%s/WebQuery/vatQuery?callback=jQuery1%s_1530868658752&%s&area=%s&_=15%s' \
              % (swjg['Url'], getNumRandomStr(21), params, swjg['code'], getNumRandomStr(11))

        response = {}
        raw_data = ''
        try:
            data = self.downloader.request_data_from_url(url, timeout= 500)
            # print len(data),data
            if data == '':
                return False, {'errorinfo': '核验返回为空', 'swjg': swjg['sfmc'], 'errorcode': '-999'}

            data = re.findall('\(({.*})\)$', data)[0]

            raw_data = data

            # data = data.decode('gbk')
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

    def CheckFp(self, fpdm, fphm, kprq, jym_or_kjje, yzm_plugin=Recongnizer()):
        '''
        发票查验入口
        1.输入发票信息与验证码信息，获取验证码
        2.
        :param fpdm:
        :param fphm:
        :param kprq:
        :param jym_or_kjje:
        :param yzm_plugin: 专门处理识别验证码的类，这里用的函数负责下载验证码图片并在命令行获取人手动验证的验证码
        :return:
        '''
        bOK, ret_img = self._get_yzm_image(fpdm, fphm)
        if not bOK:
            # print(str(ret_img))
            # 标示在获取验证码环节出现错误
            ret_img['err_type'] = 'yzm'
            return bOK, ret_img

        yzm = yzm_plugin.recongnize(ret_img['type'], ret_img['key1'])
        # 传入yzm_type, yzm_base64，识别验证码并返回

        bOK, ret = self._checkFp(fpdm, fphm, kprq, jym_or_kjje, yzm, ret_img['key3'], ret_img['key2'])
        if not bOK:
            # 标示是在发票验证环节出现错误
            ret['err_type'] = 'fp'

        # yzm_plugin.report(False if ('errorcode' in ret and (ret['errorcode'] == '008')) else True)
        # print(str(ret))
        return bOK, ret

    def printFpxx(self, fpxx):
        '''
        输出发票信息
        :param fpxx:
        :return:
        '''
        if not fpxx[0]:
            for x in fpxx[1]:
                print(fpxx[1][x])
            return
        FpParser().printFpxx(fpxx[1])


if __name__=='__main__':
    success = 0
    total = 50
    for i in range(total):
        time.sleep(10)
        c = Checker()
        fpinfo = [
            {'fpdm': '044031700111', 'fphm': '28477743', 'kprq': '20171129', 'kjje': '227858'},
            {'fpdm': '033001700211', 'fphm': '58089105', 'kprq': '20180410', 'kjje': '604420'},
            {'fpdm': '033001700211', 'fphm': '17099263', 'kprq': '20171201', 'kjje': '336134'},
            {'fpdm': '044031700111', 'fphm': '28478760', 'kprq': '20171129', 'kjje': '737421'},
        ]
        fpinfo = random.choice(fpinfo)
        bOK, ret = c.CheckFp(fpinfo['fpdm'], fpinfo['fphm'],fpinfo['kprq'], fpinfo['kjje'])
        if bOK:
            success += 1
        print(ret)
    print('成功率: ',float(success/total) , '%')
