# 找出所有红色字母，切割出来
from PIL import Image
import os
import cv2
import PIL.ImageOps
from PIL import ImageEnhance
import numpy as np
#r'C:\Users\邹盛\Desktop\验证码\黄色\2.png'
#r'C:\Users\邹盛\Desktop\自己\13毕业\柯柯(柯18）\正.jpg'
#178
#210
#184
c=0
def choose_threshold2(img):
    his = img.histogram()
    values = {}
    sum = 0
    ever = 0
    a = []
    b = []
    for i in range(256):
        values[i] = his[i]
    for j, k in sorted(values.items(), key=lambda x: x[1], reverse=True)[:2]:
        print(j, k)
        sum = sum + k
        a.append(j)
        b.append(k)
    ever = a[0] * (b[0] / sum) + a[1] * (b[1] / sum)
    if ever>200:
     return ever+3
    else:
        return ever-4
def choose_threshold(img):
    his = img.histogram()
    th=100.0
    values = {}
    threshold1=0
    threshold2=th
    sum = 0
    ever = 0
    table = []
# 做好table
    table=get_bin_table(th)
# 做好table
# 计算平均灰度值
    for i in range(256):
        values[i] = his[i]
    for j, k in sorted(values.items(), key=lambda x: x[1], reverse=True)[:10]:
        sum = sum + j * k
        ever = ever + k
    threshold1=sum/ever
# 计算平均灰度值
# 计算最小阈值
    out = img.point(table, '1')
    his = out.histogram()
    values = {}
    for i in range(256):
        values[i] = his[i]
    while (values[0] > values[1]):
        threshold2 = threshold2 + 0.1
        table=get_bin_table(threshold2)
        out = img.point(table, '1')
        his = out.histogram()
        for i in range(256):
            values[i] = his[i]

# 计算最小阈值
    if threshold1>=200:
        return threshold2
    elif 180<=threshold1<200:
        return 178
    elif threshold1<180:
        if (threshold1-threshold2)>15:
            return threshold2+0.5*(threshold1-threshold2)
        else:
            return threshold1
def get_bin_table(threshold):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(1)#白色
        else:
            table.append(0)#黑色

    return table
def depoint(img):   #input: gray image去除噪点
    pixdata = img.load()
    w,h = img.size
    # print(pixdata[10,12])
    for y in range(1,h-1):
        for x in range(1,w-1):
            count=0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if pixdata[x+1,y+1] > 245:
                count = count + 1
            if pixdata[x+1,y-1] > 245:
                count = count + 1
            if pixdata[x-1,y-1] > 245:
                count = count + 1
            if pixdata[x-1,y+1] > 245:
                count = count + 1
            if count > 6:
                pixdata[x,y] = 255
    return img
def deline(img):
    pixdata = out.load()
    w, h = out.size
    for i in range(h):
        pixdata[0,i]=255
    for i in range(w):
        pixdata[i,0]=255
    for i in range(h):
        pixdata[w-1,i]=255
    for i in range(w):
        pixdata[i,h-1]=255
    return img
def depointheng1(img):   #input: gray image去除噪点
 pixdata = img.load()
 w,h = img.size
 x=1
 y=1
 while(y<35):
    count=0
    while(x<w-1):
     # print(123)
         if pixdata[x,y]>245:
                  count=count+1
         else :count=0
         x=x+1
         if count==2or x==w-2:
            if x!=2:
                 # print(x-2)
                 for i in range(x-2):
                    pixdata[i,y]=255
            y=y+1
            x=1
            break
 return img
def depointheng2(img):   #input: gray image去除噪点
 pixdata = img.load()
 w,h = img.size
 if(pixdata[88,1]<245 or pixdata[88,2]<245):
  x=88
  y=1
  while (y < 35):
     count = 0
     while (x >  1):
         # print(123)
         if pixdata[x, y] > 245:
             count = count + 1
         else:
             count = 0
         x = x - 1
         if count == 2 or x==1:
             if x != 2:
                 # print(x-2)
                 i=88
                 while(x+2<=i):
                 # for i in range(x - 2):
                 #     print(x)
                     pixdata[i, y] = 255
                     i=i-1
             y = y + 1
             x = 88
             break
 return img
def depointshu1(img):   #input: gray image去除噪点

 pixdata = img.load()
 w,h = img.size
 x=88
 y=33
 while(1<x):
    count=0
    while(y<h-1):
         # print(123)
         if pixdata[x,y]>245:
                  # print("here")
                  count=count+1
         else :count=0
         y=y-1
         if count==2 or y==1:
            if y!=31:
                 # print(y+2)
                 i=34
                 while(y+2<=i):
                 # for i in range(x-2):
                    pixdata[x,i]=255
                    i=i-1
                    # print(x)
            x=x-1
            y=33
            break
 return img
def depointshu2(img):
    pixdata = img.load()
    w, h = img.size
    x = 1
    y = 1
    while (x<89):
        count = 0
        while (y < h - 1):
            # print(123)
            if pixdata[x, y] > 245:
                # print("here")
                count = count + 1
            else:
                count = 0
            y = y + 1
            if count == 2 and y != 33:
                    # print(y+2)
                    i = 1
                    while (i<=y-2):
                        # for i in range(x-2):
                        pixdata[x, i] = 255
                        i = i + 1
                    x = x + 1
                    y = 1
                    break
    return img
def readheibai(img):
    his = img.histogram()
    values = {}
    for i in range(256):
        values[i] = his[i]
    print(values[0])
    print(values[255])
for filename in os.listdir(r'C:\Users\邹盛\Desktop\验证码\黄色'): #listdir的参数是文件夹的路径
 # sum=0
 # ever=0
 f2=r'G:\验证码\黄色2'+'\\'+filename#保存地址
 filename=r'C:\Users\邹盛\Desktop\验证码\黄色'+'\\'+filename#打开地址
 image= Image.open(filename)
 imgry = image.convert("L")
 threshold=choose_threshold2(imgry)
 table = get_bin_table(threshold)
 out = imgry.point(table, '1')
 # table = get_bin_table(threshold)
 # out = imgry.point(table, '1')
 # his = imgry.histogram()
 # values = {}
 # for i in range(256):
 #     values[i] = his[i]
 # # for j, k in sorted(values.items(), key=lambda x: x[1], reverse=True)[:10]:
 # #     print(j, k)
 # for j, k in sorted(values.items(), key=lambda x: x[1], reverse=True)[:10]:
 #     sum = sum + j * k
 #     ever = ever + k
 # threshold=sum/ever/1.03
 # table = get_bin_table(threshold)
 # out = imgry.point(table, '1')
 # for i in range(256):
 #    values[i] = his[i]
 # while(values[0]>values[1]):
 #    threshold=threshold+0.1
 #    table = get_bin_table(threshold)
 #    out = imgry.point(table, '1')
 #    his = out.histogram()
 #    for i in range(256):
 #        values[i] = his[i]
 out=out.convert("L")
 out=deline(out)
 out=depoint(out)
# readheibai(out)
 out=depointheng1(out)
# readheibai(out)
 out=depointshu1(out)
 out=depointheng2(out)
 # out=depointshu2(out)
 out=depoint(out)
# readheibai(out)
# pixdata = out.load()
# w,h = out.size
# print(w)
# print(h)
# out=depointbig(out)
 print(threshold)
# out.show()
 c=c+1
 print(c)
 print(filename)
 out.save(f2)

# print (values[0])#黑
# print (values[1])#白
# out.show()
#print(table)
# out=out.convert("L")