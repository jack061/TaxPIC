from PIL import Image
import os
#r'C:\Users\邹盛\Desktop\验证码\黄色\2.png'
def get_bin_table(threshold):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)#白色
        else:
            table.append(1)#黑色

    return table
def depoint(img):   #input: gray image去除噪点
    pixdata = img.load()
    p=pixdata
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
            if count >=1:
                p[x,y] = 1
    for y in range(1,h-1):
        for x in range(1,w-1):
            if p[x,y]==1:
                pixdata[x,y]=255
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
         if count==2or x>=w-2:
            if x!=2:
                 # print(x-2)
                 for i in range(x-2):
                    pixdata[i,y]=255
                    # print(i)
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
         if count == 2:
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
         if count==2:
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
threshold = 220
# f2=r'G:\验证码\黄色'+'\\'+filename#保存地址
# filename=r'C:\Users\邹盛\Desktop\验证码\黄色'+'\\'+filename#打开地址
image= Image.open(r'C:\Users\邹盛\Desktop\model.png')
imgry = image.convert("L")
table = get_bin_table(threshold)
out = imgry.point(table, '1')
# his = out.histogram()
# values = {}
# for i in range(256):
#     values[i] = his[i]
#
# while(values[0]>values[1]):
#     threshold=threshold+0.1
#     table = get_bin_table(threshold)
#     out = imgry.point(table, '1')
#     his = out.histogram()
#     for i in range(256):
#         values[i] = his[i]

# threshold=threshold+18
# table = get_bin_table(threshold)
# out = imgry.point(table, '1')
out=out.convert("L")

# out=deline(out)

# out=depoint(out)
print(threshold)
# out.show()
# readheibai(out)
# out=depointheng1(out)
# # print(5)
# # readheibai(out)
#
# out=depointshu1(out)
#
# out=depointheng2(out)
#
out=depoint(out)

# readheibai(out)
# pixdata = out.load()
# w,h = out.size
# print(w)
# print(h)
# out=depointbig(out)
# print(threshold)
out.show()