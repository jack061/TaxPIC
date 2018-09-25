from PIL import Image
from pylab import *
import math
def depoint(img):   #input: gray image去除噪点
    img_array= img.load()
    w,h = img.size
    for i in range(1,h-1):
        for j in range(1,w-1):
            count=0
            if (img_array[j,i][0]==255 and img_array[j,i][1]==255 and img_array[j,i][2]==255):
                count = count + 1
            if (img_array[j,i+1][0]==255 and img_array[j,i+1][1]==255 and img_array[j,i+1][2]==255):
                count = count + 1
            if (img_array[j-1,i][0]==255 and img_array[j-1,i][1]==255 and img_array[j-1,i][2]==255):
                count = count + 1
            if  (img_array[j+1,i][0]==255 and img_array[j+1,i][1]==255 and img_array[j+1,i][2]==255):
                count = count + 1
            if (img_array[j+1,i+1][0]==255 and img_array[j+1,i+1][1]==255 and img_array[j+1,i+1][2]==255):
                count = count + 1
            if (img_array[j+1,i-1][0]==255 and img_array[j+1,i-1][1]==255 and img_array[j+1,i-1][2]==255):
                count = count + 1
            if (img_array[j-1,i-1][0]==255 and img_array[j-1,i-1][1]==255 and img_array[j-1,i-1][2]==255):
                count = count + 1
            if (img_array[j-1,i+1][0]==255 and img_array[j-1,i+1][1]==255 and img_array[j-1,i+1][2]==255):
                count = count + 1
            if count > 6:
                img.putpixel((j , i), (255,255,255, 255))
    for i in range(w):
                img.putpixel((i, 0), (255, 255, 255, 255))
                img.putpixel((i, h-1), (255, 255, 255, 255))
    for i in range(h):
                img.putpixel((0, i), (255, 255, 255, 255))
                img.putpixel((w-1, i), (255, 255, 255, 255))
    return img
def cut(img):
 child_img_list = []
 w,h=img.size
 a=[]
 b=[]
 c=[]
 d=[]
 e=[]
 q=0
 count0=0
 img_array=img.load()
 for x in range(w):
    for y in range(h):
        if(img_array[x,y]==(0,0,0)):
            count0=count0+1
    c.append(count0)
    count0=0
 for x in range(1,w-1):
    if(c[x-1]==0 and c[x]!=0 ):
        a.append(x)
    if(c[x]!=0 and c[x+1]==0):
        b.append(x)
 print("修改前：")
 for i in range(len(a)):
     print(a[i])
     print(b[i])
 for i in range(len(a)):#归并孤立部分,i从0来
  if((i<(len(a)-1))and len(a)>=1):
   if(i==0 and ((b[i]-a[i])<=3) and (c[a[i]]<=2)and (c[b[i]]<=2)):
       a.pop(i+1)
       b.pop(i)
       continue
   if(i!=0and((b[i]-a[i])<=3) and (c[a[i]]<=2)and (c[b[i]]<=2)):
        if((a[i+1]-b[i])<(a[i]-b[i-1])):#距离后面近
            a.pop(i+1)
            b.pop(i)
            continue
        else:#距离前面近
            a.pop(i)
            b.pop(i-1)
            continue
 d=a
 e=b
 for i in range(len(a)):
  if((b[i]-a[i])>15):
    p = math.ceil((b[i]-a[i])/15)
    for l in range(1,p):
      k= int(a[i]+l*(b[i]-a[i])/p)
      d.append(k)
      e.append(k)
 d.sort()#开始
 e.sort()#结束
  # d.pop((len(d)-1))
  # e.pop(0)
 a=d
 b=e
 print("修改后：")
 for i in range(len(d)):
     print(a[i])
     print(b[i])
 for i in range(len(a)):
    child_img = img.crop((a[i], 0, b[i], h-1))
    child_img_list.append(child_img)
 for i in range(len(child_img_list)):
    new_image = child_img_list[i].resize((16, h), Image.BILINEAR)
    new_image.show()
# img= Image.open(r'G:\验证码\蓝色\140.png')
# f2=filename#保存地址
# filename=r'C:\Users\邹盛\Desktop\验证码\蓝色'+'\\'+filename#打开地址
 # a=[]
 # b=[]
img= Image.open(r'C:\Users\邹盛\Desktop\验证码\蓝色\1381.png')
 # img=Image.open(r'C:\Users\邹盛\Desktop\验证码\蓝色\265.png')
img_array=img.load()
x,y=img.size
for i in range(y):
    for j in range(x):
        if (img_array[j,i][0]<100 and img_array[j,i][1]<100 and img_array[j,i][2]>200 and (img_array[j,i][0]+img_array[j,i][1])<img_array[j,i][2]):
            img.putpixel((j, i), (0, 0, 0, 255))#黑
        else:
            img.putpixel((j, i), (255, 255, 255,255))#白
img=depoint(img)
cut(img)