#!/usr/bin/python
#coding=utf-8


__author__ = 'groundlee'

import io
# from InvoiceCloud.settings_runmode import RUN_MODE
RUN_MODE = ''
import logging
logger = logging.getLogger('invoice_job')
# import sys
# sys.path.append('/home/fapiao/Desktop/InvoiceCloud')
# RUN_MODE = 'product'
def log_yzm(imgtype,img,result = ''):
    if RUN_MODE != 'product':
        f = open('/Users/groundlee/Downloads/test1_img.html','r')
        data = f.read()
        f.close()

        f = open('/Users/groundlee/Downloads/test1_img.html','w+')
        if type(result) is str :
            result = result.decode('utf-8')
        html = u'<img src="data:image/jpg;base64,%s" />  result: %s type: %s <br>' % (img,result,imgtype['info'])
        # f.seek(0,io.SEEK_END)
        # x = f.tell()
        f.write(html.encode('utf-8'))
        f.write(data)
        f.close()
        print ('write file ok!')



class YzmBase:
    def get(self,type,img):
        return ('这里是验证码')

    def report(self,bOK):
        pass


class ConsoleYzmPlugin(YzmBase):

    def get(self,type,img):
        log_yzm(type,img)
        yzm = input("Enter your input yzm: ");
        print ("Received input yzm is : ", yzm)
        log_yzm(type,img,yzm)
        return yzm



from donwloader import Downloader
import json
import base64
from PIL import Image
import StringIO
import os


class JsdmYzmPlugin(YzmBase):

    def __init__(self):
        self.getdmResult = None

    jsdm_info = {
        "softwareId":7706,
        "softwareSecret":"VWWWyHAu2kXHJ0g1YvPiYUQSDgIDYsjyVjemC5vh",
        "username":"bigbencat",
        "password":"Windows7878",
    }

    def __createYzmImage(self,base64Img,imgtype):
        data = base64.b64decode(base64Img)
        input = StringIO.StringIO(data)
        image = Image.open(input)

        file_name = os.path.split(os.path.realpath(__file__))[0]+ "/img/" + imgtype['img']
        toImage = Image.open(file_name)
        toImage.paste(image,((toImage.width - image.width)/2,toImage.height - image.height ))

        output = StringIO.StringIO()
        toImage.save(output,'PNG')
        contents = output.getvalue()
        output.close()

        return base64.b64encode(contents)

    def get(self,type,img):
        retImg = self.__createYzmImage(img,type)
        d = Downloader()
        data = dict(JsdmYzmPlugin.jsdm_info,**{
            "captchaData":retImg,
            "captchaType":1023,
            "captchaMinLength":0,
            "captchaMaxLength":0
            })
        dataPost = json.dumps(data)
        ret = d.down_date_from_url('https://v2-api.jsdama.com/upload','post',dataPost,timeout= -1)
        # str '{"code":0,"data":{"recognition":"JBCZGJ","captchaId":"20170911:000000000009323211884"},"message":""}'
        logger.info('获取验证码返回信息：%s',str(ret))
        j_ret = json.loads(ret)
        dataret = j_ret.get('data', None)
        if dataret:
            recognition = dataret['recognition']
        else:
            recognition = None

        self.getdmResult = ret
        print( '验证码自动识别：[' ,recognition,']')
        return recognition


    def report(self,bOK):
        if bOK: return
        if not self.getdmResult: return

        # str '{"code":0,"data":{"recognition":"JBCZGJ","captchaId":"20170911:000000000009323211884"},"message":""}'
        j_ret = json.loads(self.getdmResult)
        if not j_ret['data']:
            return
        captchaId = j_ret['data']['captchaId']

        d = Downloader()
        data = dict(JsdmYzmPlugin.jsdm_info,**{"captchaId":captchaId})
        dataPost = json.dumps(data)
        ret = d.down_date_from_url('https://v2-api.jsdama.com/report-error','post',dataPost,timeout= -1)
        print (ret)

if __name__ == '__main__':
    #img = '''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'''
    #jsdama({ 'info' : u'请输入验证码图片中蓝色文字', 'img':'yzm_blue.png'},img)
    img = '''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'''

    jsdm = JsdmYzmPlugin()
    jsdm.get({ 'info' : u'请输入验证码图片中蓝色文字', 'img':'yzm_blue.png'},img)