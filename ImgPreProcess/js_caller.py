import os
import execjs
import time

os.environ["EXECJS_RUNTIME"] = "Node"


def getJsData(js_file):
    '''
    读取js 文件内容
    :param js_file:
    :return: js文件内容
    '''
    paths=os.path.dirname(__file__)
    #print paths
    dir=paths+"/js/" + js_file
    return open(dir,'r').read()


def ckYZM(fpdmyzm,nowtime):
    '''
    获取验证码的时候，构造publickey
    :param fpdmyzm:
    :param nowtime:
    :return: 加密后的数据
    '''
    js_data = getJsData('encrypt.js')
    caller = execjs.compile(js_data)
    return caller.call('ck',fpdmyzm,nowtime)


def ckFP(fpdm, fphm,kjje, kprq, yzmSj, yzm):
    '''
    获取发票信息的时候，构造publickey
    :param fpdm:
    :param fphm:
    :param kjje:
    :param kprq:
    :param yzmSj:
    :param yzm:
    :return: 加密后的数据
    '''
    js_data = getJsData('encrypt.js')
    caller = execjs.compile(js_data)
    return caller.call('ck', fpdm, fphm, kjje, kprq, yzmSj, yzm)


if __name__ == '__main__':
    nowtime = str(int(time.time() * 1000))
    a = ckYZM( '044031700111', nowtime)
    print(a)   
