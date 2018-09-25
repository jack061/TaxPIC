from PIL import Image
import PIL.ImageOps
from PIL import ImageEnhance
import numpy as np
red = Image.open(r'C:\Users\邹盛\Desktop\验证码\img\yzm_red.png')
blue = Image.open(r'C:\Users\邹盛\Desktop\验证码\img\yzm_blue.png')
yellow = Image.open(r'C:\Users\邹盛\Desktop\验证码\img\yzm_yellow.png')

red = red.convert("P")
blue = blue.convert("P")
yellow = yellow.convert("P")
img = Image.open(r'C:\Users\邹盛\Desktop\验证码\img\yzm_blue.png')
# img = ImageEnhance.Sharpness(img).enhance(3)
# red = red.histogram()
# blue = blue.histogram()
# yellow = yellow.histogram()
# valuesr = {}
# valuesb = {}
# valuesy = {}
# for i in range(256):
#     valuesr[i] = red[i]
#     valuesb[i] = blue[i]
#     valuesy[i] = yellow[i]
# for j,k in sorted(valuesy.items(),key=lambda x:x[1],reverse = True)[:10]:
#     print('yellow',j,k)
def depoint(img):   #input: gray image去除噪点
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    return img
# img = ImageEnhance.Sharpness(img).enhance(3)
def binarizing(img,threshold): #input: gray image二值化
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img
def get_grey(img):
    l = img.size[0]
    w = img.size[1]
    img1 = img.convert("YCbCr")
    info = []
    for x in range(l):
        for y in range(w):
            light,cb,cr = img1.getpixel((x,y))
            if light < 127:
                r,g,b = img.getpixel((x,y))
                info.append('0,0,0')
            else:
                info.append('255,255,255')
    c = Image.new("RGB",(l,w))
    for i in range(l):
        for j in range(w):
            rgb = info[i * w + j].split(",")
            c.putpixel([i,j],(int(rgb[0]),int(rgb[1]),int(rgb[2])))
    c.show()
# img = img.convert("L")
# img2 = binarizing(img,120)
img = img.convert("P")
his = img.histogram()
values = {}
for i in range(256):
    values[i] = his[i]
for j,k in sorted(values.items(),key=lambda x:x[1],reverse = True)[:10]:
    print (j,k)
#C:\Users\邹盛\Desktop\验证码\img\yzm_blue.png
# img2 = Image.new("L",yellow.size,255)
# for x in range(img.size[1]):
#     for y in range(img.size[0]):
#         pix = img.getpixel((y,x))
#         if pix == 183 or pix == 139 or pix == 138 : # these are the numbers to get
#             img2.putpixel((y,x),0)
#
# img2 = PIL.ImageOps.invert(img2)
# img2.show()
# img2 = ImageEnhance.Sharpness(img2).enhance(3)
# img2 = depoint(img2)
# img2.show()
