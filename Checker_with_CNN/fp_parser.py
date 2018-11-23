import datetime
import math
import json
from settings import root_url
from downloader import Downloader

rulers = {
    'dc1de': u'▽☺4>2_8>6☺467☺-4☺□'
}


class FpParser:
    # 处理发票信息，申请发票的验证、详情获取等
    # 收到响应中，有关发票信息的处理与输出

    def __FormatDate(self, time, add):
        '''
        根据时间和时间差，构造时间
        比如time是‘20180411’，add=10
        输出是ret= ‘20180401’
        :param time: str 时间
        :param add: int 与真实时间的差值
        :return:
        '''
        a = datetime.datetime.strptime(time, '%Y%m%d')
        b = datetime.timedelta(days=0 - int(add))
        a += b
        ret = a.strftime('%Y%m%d')
        return ret


    def __chgchar(self, nsrsbh, ss):
        a = ss[2]
        b = ss[0]  # 反向替换，所以和java中是相反的
        nsrsbh = nsrsbh.replace(a, '#')
        nsrsbh = nsrsbh.replace(b, '%')
        nsrsbh = nsrsbh.replace('#', b)
        nsrsbh = nsrsbh.replace('%', a)
        return nsrsbh


    def __FormatSBH(self, sbh, str):
        s1 = str.split("_")
        for s in s1:  # i in range(0,len(s1)):
            sbh = self.__chgchar(sbh, s)
        return sbh


    def __accAdd(self, arg1, arg2):
        """
        加法函数，用来得到精确的加法结果
        javascript的加法结果会有误差，在两个浮点数相加的时候会比较明显。这个函数返回较为精确的加法结果。
        :param arg1:
        :param arg2:
        :return:
        """
        r1 = r2 = m = 0
        if arg1.replace(u' ', '') == "":
            return arg1
        if not (abs(float(arg1) - int(float(arg1))) > 0):
            r1 = 0
        else:
            r1 = len(str(arg1).split(".")[1])

        if not (abs(float(arg2) - int(float(arg2))) > 0):
            r2 = 0
        else:
            len(r2 = str(arg2).split(".")[1])

        m = math.pow(10, max(r1, r2))
        r = (float(arg1) * m + float(arg2) * m) / m
        return round(r, 2)


    def __getje(self, je, ss):
        if je:
            return str(self.__accAdd(je, ss))
        else:
            return je


    def __GetJeToDot(self, je):
        if (je and je.replace(u' ', '') != ""):
            if je.replace(u' ', '') == '-':
                return je
            je = je.replace(u' ', '')
            if je[0:1] == '.':
                je = '0' + '.' + je[1:len(je)]
                return je
            index = je.find(".")

            if index < 0:
                je += ".00"
            elif len(je.split(".")[1]) == 1:
                je += "0"
            if je[0:2] == '-.':
                je = '-0.' + je[2, len(je)]
            return je
        else:
            return je


    def __getzeroDot(self, je):
        if je[0: 2] == "-.":
            je = "-0." + je[2:]
        elif je[0:1] == ".":
            je = "0." + je[1:]
        return je


    def __FormatHwmc(self, mc, str):
        ss = mc.replace(str, "")
        return ss


    def __FormatSl(self, data):
        data = data.replace(' ', '')
        if data[0:1] == ".":
            data = str(float("0" + data) * 100)

        return data


    def __GetDzHwxx(self, hwxxs, hwstr, je, fplx):

        hwinfo = hwxxs.split(u'≡')
        retHwxxs = []
        for i in range(0, len(hwinfo)):
            hw = hwinfo[i].split(u'█')
            if fplx[0] in ('10', '14'):
                hwxx = {
                    'mc': ('名称', self.__FormatHwmc(hw[0], hwstr)),
                    'gg': ('规格', hw[1].replace(' ', '')),
                    'dw': ('单位', hw[2].replace(' ', '')),
                    'sl': ('税率', self.__FormatSl(hw[3])),
                    'dj': ('单价', self.__GetJeToDot(hw[4].replace(' ', ''))),
                    'je': ('金额', self.__GetJeToDot(hw[5].replace(' ', ''))),
                    'num': ('数量', self.__getzeroDot(hw[6])),
                    'se': ('税额', self.__GetJeToDot(hw[7].replace(' ', ''))),
                }
            elif fplx[0] in ('01', '04'):  # 一样吗？
                hwxx = {
                    'mc': ('名称', self.__FormatHwmc(hw[0], hwstr)),
                    'gg': ('规格', hw[1].replace(' ', '')),
                    'dw': ('单位', hw[2].replace(' ', '')),
                    'num': ('数量', self.__getzeroDot(hw[3])),
                    'dj': ('单价', self.__GetJeToDot(hw[4].replace(' ', ''))),
                    'je': ('金额', self.__GetJeToDot(hw[5].replace(' ', ''))),
                    'sl': ('税率', self.__FormatSl(hw[6])),
                    'se': ('税额', self.__GetJeToDot(hw[7].replace(' ', ''))),
                }
            elif fplx[0] == '03':  # 机动车
                hwxx = {}  # 机动车就没有货物信息啦
            else:  # 其他发票类型搞到再说
                hwxx = {
                    'mc': ('名称', self.__FormatHwmc(hw[0], hwstr)),
                    'gg': ('规格', hw[1].replace(' ', '')),
                    'dw': ('单位', hw[2].replace(' ', '')),
                    'num': ('数量', self.__getzeroDot(hw[3])),
                    'dj': ('单价', self.__GetJeToDot(hw[4].replace(' ', ''))),
                    'je': ('金额', self.__GetJeToDot(hw[5].replace(' ', ''))),
                    'sl': ('税率', self.__FormatSl(hw[6])),
                    'se': ('税额', self.__GetJeToDot(hw[7].replace(' ', ''))),
                }
            retHwxxs.append(hwxx)
        return retHwxxs


    def __GetDzHwxx_new(self, hwxxs, fplx):
        hwinfo = hwxxs.split(u'≡')
        retHwxxs = []
        for i in range(0, len(hwinfo)):
            hw = hwinfo[i].split(u'█')
            if fplx[0] == '10':
                hwxx = {
                    'mc': ('名称', hw[0]),
                    'gg': ('规格', hw[1].replace(' ', '')),
                    'dw': ('单位', hw[2].replace(' ', '')),
                    'sl': ('税率', hw[3]),
                    'dj': ('单价', hw[4]),
                    'je': ('金额', hw[5]),
                    'num': ('数量', hw[6]),
                    'se': ('税额', hw[7]),
                }
            elif fplx[0] in ('01', '04'):  # 一样吗？
                hwxx = {
                    'mc': ('名称', hw[0]),
                    'gg': ('规格', hw[1].replace(' ', '')),
                    'dw': ('单位', hw[2].replace(' ', '')),
                    'num': ('数量', hw[3]),
                    'dj': ('单价', hw[4]),
                    'je': ('金额', hw[5]),
                    'sl': ('税率', hw[6]),
                    'se': ('税额', hw[7]),
                }
            elif fplx[0] == '03':  # 机动车
                hwxx = {}  # 机动车就没有货物信息啦
            else:  # 其他发票类型搞到再说
                hwxx = {
                    'mc': ('名称', hw[0]),
                    'gg': ('规格', hw[1].replace(' ', '')),
                    'dw': ('单位', hw[2].replace(' ', '')),
                    'sl': ('税率', hw[3]),
                    'dj': ('单价', hw[4]),
                    'je': ('金额', hw[5]),
                    'num': ('数量', hw[6]),
                    'se': ('税额', hw[7]),
                }
            retHwxxs.append(hwxx)
        return retHwxxs


    def __get_rulers(self, key11):
        if key11 in rulers:
            return rulers[key11]
        # 'var rule="▽☺4>2_8>6☺467☺-4☺□"'
        ret = Downloader().request_data_from_url('%sjs/%s.js' % (root_url, key11))
        ret = ret.decode('utf8')
        rulers[key11] = ret.split(u'"')[1]
        return rulers[key11]


    def get_fplx_from_fpdm(self, fpdm):

        fplx = ("99", "未知")
        if len(fpdm) == 12:
            b = fpdm[7:8]
            if fplx[0] == "99":  # 增加判断，判断是否为新版电子票
                if fpdm[0] == '0' and fpdm[10:12] == '11':
                    fplx = ("10", u"增值税普通发票（电子）")
                if fpdm[0] == '0' and fpdm[10:12] == '12':
                    fplx = ("14", u"增值税电子普通发票（通行费）")  # 官网是14
                if fpdm[0] == '0' and (fpdm[10:12] == '06' or fpdm[10:12] == '07'):  # 判断是否为卷式发票  第1位为0且第11-12位为06或07
                    fplx = ("11", u"增值税普通发票（卷票)")
                if fpdm[0] == '0' and fpdm[10:12] == '04':
                    fplx = ("04", u"增值税普通发票")
            if fplx[0] == "99":  # 如果还是99，且第8位是2，则是机动车发票
                if b == '2' and (fpdm[0] != '0'):
                    fplx = ("03", u"机动车销售统一发票")

        elif len(fpdm) == 10:
            b = fpdm[7:8]
            if b == '1' or b == '5':
                fplx = ("01", u"增值税专用发票")
            elif b == '6' or b == '3':
                fplx = ("04", u"增值税普通发票")
            elif b == '7' or b == '2':
                fplx = ("02", u"货物运输业增值税专用发票")
        return fplx

    def __get_fpxx_from_fpxxlist_new(self, fpxxs, fplx, key4_bz):
        fpxx = fpxxs.split(u"≡")

        if fplx[0] == '10':
            retFpxx = {
                'fpdm': ('发票代码', fpxx[0]),
                'fphm': ('发票号码', fpxx[1]),
                'fpmc': ('发票名称', fplx[1]),
                'fpszd': ('发票所在地', fpxx[2]),
                'cycs': ('查验次数', int(fpxx[3]) + 1),
                'kprq': ('开票日期', fpxx[4]),
                'xfmc': ('销方名称', fpxx[5]),
                'xfsbh': ('销方识别号', fpxx[6]),
                'xfdzdh': ('销方地址电话', fpxx[7]),
                'xfyhzh': ('销方银行账号', fpxx[8]),
                'gfmc': ('购方名称', fpxx[9]),
                'gfsbh': ('购方识别号', fpxx[10]),
                'gfdzdh': ('购方地址电话', fpxx[11]),
                'gfyhzh': ('购方银行账号', fpxx[12]),
                'jym': ('校验码', fpxx[13]),
                'se': ('税额', fpxx[14]),
                'jshj': ('价税合计', fpxx[15]),
                'bz': ('备注', key4_bz),  # fpxx[16]), 在电子发票里面，key4放的是备注哦
                'jqbh': ('机器编号', fpxx[17]),
                'je': ('金额(不含税)', fpxx[18]),
                'zfbz': ('作废标志', fpxx[19]),
                'cysj': ('查验时间', fpxx[20]),
            }
        elif fplx[0] == '14':
            retFpxx = {
                'fpdm': ('发票代码', fpxx[0]),
                'fphm': ('发票号码', fpxx[1]),
                'fpmc': ('发票名称', fplx[1]),
                'fpszd': ('发票所在地', fpxx[2]),
                'cycs': ('查验次数', int(fpxx[3]) + 1),
                'kprq': ('开票日期', fpxx[4]),
                'xfmc': ('销方名称', fpxx[5]),
                'xfsbh': ('销方识别号', fpxx[6]),
                'xfdzdh': ('销方地址电话', fpxx[7]),
                'xfyhzh': ('销方银行账号', fpxx[8]),
                'gfmc': ('购方名称', fpxx[9]),
                'gfsbh': ('购方识别号', fpxx[10]),
                'gfdzdh': ('购方地址电话', fpxx[11]),
                'gfyhzh': ('购方银行账号', fpxx[12]),
                'jym': ('校验码', fpxx[13]),
                'se': ('税额', fpxx[14]),
                'jshj': ('价税合计', fpxx[15]),
                'bz': ('备注', key4_bz),  # fpxx[16]), 在电子发票里面，key4放的是备注哦
                'jqbh': ('机器编号', fpxx[17]),
                'je': ('金额(不含税)', fpxx[18]),
                'zfbz': ('作废标志', fpxx[19]),
                'cysj': ('查验时间', fpxx[20]),
            }
        elif fplx[0] == '01':
            retFpxx = {
                'fpdm': ('发票代码', fpxx[0]),
                'fphm': ('发票号码', fpxx[1]),
                'fpmc': ('发票名称', fplx[1]),
                'fpszd': ('发票所在地', fpxx[2]),
                'cycs': ('查验次数', int(fpxx[3]) + 1),
                'kprq': ('开票日期', fpxx[4]),
                'gfmc': ('购方名称', fpxx[5]),
                'gfsbh': ('购方识别号', fpxx[6]),
                'gfdzdh': ('购方地址电话', fpxx[7]),
                'gfyhzh': ('购方银行账号', fpxx[8]),

                'xfmc': ('销方名称', fpxx[9]),
                'xfsbh': ('销方识别号', fpxx[10]),
                'xfdzdh': ('销方地址电话', fpxx[11]),
                'xfyhzh': ('销方银行账号', fpxx[12]),
                'je': ('金额(不含税)', fpxx[13]),
                'se': ('税额', fpxx[14]),
                'jshj': ('价税合计', fpxx[15]),
                'bz': ('备注', key4_bz),  # fpxx[16]), 在电子发票里面，key4放的是备注哦
                'jqbh': ('机器编号', fpxx[17]),
                'jym': ('校验码', fpxx[19]),
                'zfbz': ('作废标志', fpxx[20]),
                'cysj': ('查验时间', fpxx[21])
            }
        elif fplx[0] == '04':
            retFpxx = {
                'fpdm': ('发票代码', fpxx[0]),
                'fphm': ('发票号码', fpxx[1]),
                'fpmc': ('发票名称', fplx[1]),
                'fpszd': ('发票所在地', fpxx[2]),
                'cycs': ('查验次数', int(fpxx[3]) + 1),
                'kprq': ('开票日期', fpxx[4]),
                'xfmc': ('销方名称', fpxx[5]),
                'xfsbh': ('销方识别号', fpxx[6]),
                'xfdzdh': ('销方地址电话', fpxx[7]),
                'xfyhzh': ('销方银行账号', fpxx[8]),

                'gfmc': ('购方名称', fpxx[9]),
                'gfsbh': ('购方识别号', fpxx[10]),
                'gfdzdh': ('购方地址电话', fpxx[11]),
                'gfyhzh': ('购方银行账号', fpxx[12]),
                'je': ('金额(不含税)', fpxx[19]),
                'se': ('税额', fpxx[14]),
                'jshj': ('价税合计', fpxx[15]),
                'bz': ('备注', key4_bz),  # fpxx[16]), 在电子发票里面，key4放的是备注哦
                'jqbh': ('机器编号', fpxx[17]),
                'jym': ('校验码', fpxx[13]),
                'zfbz': ('作废标志', fpxx[20]),
                'cysj': ('查验时间', fpxx[21])
            }
        elif fplx[0] == '03':  # 机动车
            retFpxx = {
                'fpdm': ('发票代码', fpxx[0]),
                'fphm': ('发票号码', fpxx[1]),
                'fpmc': ('发票名称', fplx[1]),
                'fpszd': ('发票所在地', fpxx[2]),
                'cycs': ('查验次数', int(fpxx[3]) + 1),
                'kprq': ('开票日期', fpxx[4]),

                'jqbh': ('机器编号', fpxx[5]),

                'gfmc': ('购买方名称', fpxx[6]),
                'gfsfzhm': ('购方身份证号码', fpxx[7]),
                'gfsbh': ('购方识别号', fpxx[8]),

                'cllx': ('车辆类型', fpxx[9]),
                'cpxh': ('厂牌型号', fpxx[10]),
                'cd': ('产地', fpxx[11]),
                'hgzs': ('合格证号', fpxx[12]),

                'je': ('不含税价', fpxx[13]),

                'sjdh': ('商检单号', fpxx[14]),
                'fdjhm': ('发动机号码', fpxx[15]),
                'cjhm': ('车辆识别代号/车架号码', fpxx[16]),
                'jkzmsh': ('进口证明书号', fpxx[17]),

                'xfmc': ('销方名称', fpxx[18]),
                'xfdzdh': ('销货单位电话', fpxx[19]),
                'xfsbh': ('销方纳税人识别号', fpxx[20]),
                'xfyhzh': ('销方账号', fpxx[21]),
                'xfdzdh': ('销方地址', fpxx[22]),

                'xfkhyh': ('销方开户银行', fpxx[23]),
                'sl': ('税率', fpxx[24].replace('%', '')),
                'se': ('税额', fpxx[25]),

                'swjg': ('税务机构', fpxx[32]),
                'swjg_dm': ('税务机构代码', fpxx[26]),

                'jshj': ('价税合计', fpxx[27]),
                'wspzhm': ('完税凭证号码', fpxx[28]),
                'dw': ('吨位', fpxx[29]),
                'xcrs': ('限乘人数', fpxx[30]),
                'zfbz': ('作废标志', fpxx[31]),
                'cysj': ('查验时间', '')
            }
        elif fplx[0] == '11':  # 卷票
            retFpxx = {
                'fpdm': ('发票代码', fpxx[0]),
                'fphm': ('发票号码', fpxx[1]),
                'fpmc': ('发票名称', fplx[1]),
                'fpszd': ('发票所在地', fpxx[2]),
                'cycs': ('查验次数', int(fpxx[3]) + 1),
                'kprq': ('开票日期', fpxx[4]),

                'cysj': ('查验时间', fpxx[17]),

                'xfmc': ('销方名称', fpxx[5]),
                'xfsbh': ('销方纳税人识别号', fpxx[6]),

                'gfmc': ('购买方名称', fpxx[7]),
                'gfsbh': ('购方识别号', fpxx[8]),

                'jqbh': ('机器编号', fpxx[9]),

                'jshj': ('含税价', fpxx[11]),
                'se': ('税额', ''),

                'jym': ('校验码', fpxx[13]),
                'shy': ('收货员', fpxx[15]),
                'zfbz': ('作废标志', fpxx[15]),
            }
        else:  # 以后再说
            retFpxx = {
                'fpdm': ('发票代码', fpxx[0]),
                'fphm': ('发票号码', fpxx[1]),
                'fpmc': ('发票名称', fplx[1]),
                'fpszd': ('发票所在地', fpxx[2]),
                'cycs': ('查验次数', int(fpxx[3]) + 1),
                'kprq': ('开票日期', fpxx[4]),
                'xfmc': ('销方名称', fpxx[5]),
                'xfsbh': ('销方识别号', fpxx[6]),
                'xfdzdh': ('销方地址电话', fpxx[7]),
                'xfyhzh': ('销方银行账号', fpxx[8]),
                'gfmc': ('购方名称', fpxx[9]),
                'gfsbh': ('购方识别号', fpxx[10]),
                'gfdzdh': ('购方地址电话', fpxx[11]),
                'gfyhzh': ('购方银行账号', fpxx[12]),
                'jym': ('校验码', fpxx[13]),
                'se': ('税额', fpxx[14]),
                'jshjxx': ('价税合计', fpxx[15]),
                'bz': ('备注', fpxx[16]),
                'jqbh': ('机器编号', fpxx[17]),
                'je': ('金额(不含税)', fpxx[18]),
                'zfbz': ('作废标志', fpxx[19]),
                'cysj': ('查验时间', fpxx[20]),
            }
        return retFpxx


    # 处理服务器传回的发票数据
    def ParserFpinfo(self, data, fpdm, fphm, swjgmc, yzmSj):

        fplx = self.get_fplx_from_fpdm(fpdm)
        j = json.loads(data)

        fpxxs_str = '%s≡%s≡%s≡' % (fpdm, fphm, swjgmc)
        # fpxxs_str = fpxxs_str.decode('utf8')
        fpxxs_str += j['key2'] + u'≡'
        # fpxxs = fpxxs.split(u"≡")
        # key4是复数发票对应的正数发票代码和号码
        key4_bz = j.get('key4', '')  # 在电子发票里面存的是备注，其他不知道哦
        # 传入fpxxs_str
        retFpxx = self.__get_fpxx_from_fpxxlist_new(fpxxs_str, fplx, key4_bz)
        # 开票明细
        hwxxs = j['key3']  # █
        retHhxxs = self.__GetDzHwxx_new(hwxxs, fplx)

        retFpxx['hwxx'] = retHhxxs

        return retFpxx

    def printFpxx(self, fpxx):
        print('================================', fpxx['fpmc'][1], '==================================')
        for xx in fpxx:
            if xx == 'hwxx': continue
            print(fpxx[xx][0], )
            print(' ' * (10 - (len(fpxx[xx][0]) / 2)), )
            print(':  ', fpxx[xx][1])
        print('================================货物信息==================================')
        if 'hwxx' in fpxx:
            for hw in fpxx['hwxx']:
                for info in hw:
                    # print hw[info][0],hw[info][1],'\t',
                    print(hw[info][0], )
                    print(' ' * (10 - (len(hw[info][0]) / 2)), )
                    print(':  ', hw[info][1])
        print('\n')
        print('==========================================================================')


if __name__ == '__main__':

    c = FpParser()

