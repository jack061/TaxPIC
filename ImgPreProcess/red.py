# 找出所有红色字母，切割出来
from PIL import Image
from pylab import *
import os
import math

fromDir = r'D:\csy\验证码识别\验证码\红色'  # 存放原始图片文件的文件夹
destDir = r'D:\csy\验证码识别\验证码\红色'  # 处理后的图片存放位置

def depoint(img):   #input: gray image去除噪点
    img_array = img.load()
    w, h = img.size
    for i in range(1, h-1):
        for j in range(1, w-1):
            count = 0
            if (img_array[j,i-1][0] == 255 and img_array[j,i-1][1] == 255 and img_array[j,i-1][2] == 255):
                count = count + 1
            if (img_array[j,i+1][0] == 255 and img_array[j,i+1][1]==255 and img_array[j,i+1][2]==255):
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
                img.putpixel((j, i), (255, 255, 255, 255))  # 如果一个点周围八个点有七个是空白，认为该点也应该是空白

    # 下面两个循环将图片最边缘一圈全部涂白
    for i in range(w):
                img.putpixel((i, 0), (255, 255, 255, 255))
                img.putpixel((i, h-1), (255, 255, 255, 255))

    for i in range(h):
                img.putpixel((0, i), (255, 255, 255, 255))
                img.putpixel((w-1, i), (255, 255, 255, 255))

    return img


def cut(img, filename):
    child_img_list = []
    w, h = img.size
    startEdge = []
    endEdge = []
    blackdotsEachColumn = []
    count0 = 0
    img_array = img.load()
    for x in range(w):
        for y in range(h):
            if (img_array[x, y] == (0, 0, 0)):
                count0 = count0 + 1
        blackdotsEachColumn.append(count0)  # 变量blackDotsEachColumn记录下来每一列的黑点数量
        count0 = 0

    for x in range(1, w - 1):  # 选定除了边框外的每一列，遍历查找图像的边缘列，每一个起始边缘都有一个对应的结束边缘
        if (blackdotsEachColumn[x - 1] == 0 and blackdotsEachColumn[x] != 0):  # 从左到右，遍历查找起始边缘
            startEdge.append(x)
        if (blackdotsEachColumn[x] != 0 and blackdotsEachColumn[x + 1] == 0):  # 从左到右，遍历查找结束边缘
            endEdge.append(x)

    for i in range(len(startEdge)):  # 归并本该在一起的部分
        # 如果一个块太小，可以认为它属于前一个或后一个块
        if ((i < (len(startEdge) - 1)) and len(startEdge) >= 1):  # 如果存在起始边缘，且没有遍历到最后一个边缘
            
            # 第一个块没有前一个块，所以如果太小的话，肯定跟后一个块是一体的
            if (i == 0 and ((endEdge[i] - startEdge[i]) <= 3) and (blackdotsEachColumn[startEdge[i]] <= 2) and (blackdotsEachColumn[endEdge[i]] <= 2)):
                startEdge.pop(i + 1)
                endEdge.pop(i)
                continue

            if (i != 0 and ((endEdge[i] - startEdge[i]) <= 3) and (blackdotsEachColumn[startEdge[i]] <= 2) and (blackdotsEachColumn[endEdge[i]] <= 2)):
                if ((startEdge[i + 1] - endEdge[i]) < (startEdge[i] - endEdge[i - 1])):  # 当该块与它后面的块距离更近，可以认为这个块是属于后面的一个块，他们之间的边缘可以去掉
                    startEdge.pop(i + 1)
                    endEdge.pop(i)
                    continue

                else:  # 距离前面近
                    startEdge.pop(i)
                    endEdge.pop(i - 1)
                    continue

    tmp1 = startEdge 
    tmp2 = endEdge

    for i in range(len(startEdge)):
        blockWidth = endEdge[i] - startEdge[i]
        if (blockWidth > 15):  # 如果一个字符块宽度大于15列
            p = math.ceil(blockWidth / 15)  # 向上取整，
            for l in range(1, p):
                k = int(startEdge[i] + l * blockWidth / p)
                tmp1.append(k)
                tmp2.append(k)
                
    # 从小到大排序
    tmp1.sort()  # 开始
    tmp2.sort()  # 结束
    # d.pop((len(d)-1))
    # e.pop(0)
    startEdge = tmp1
    endEdge = tmp2
    # print("修改后：")
    # for i in range(len(d)):
    #     print(startEdge[i])
    #     print(endEdge[i])
    for i in range(len(startEdge)):
        child_img = img.crop((startEdge[i], 0, endEdge[i], h - 1))
        child_img_list.append(child_img)
    for i in range(len(child_img_list)):
        new_image = child_img_list[i].resize((16, h), Image.BILINEAR)
    address = fromDir + '\\' + str(i) + filename
    new_image.save(address)


for filename in os.listdir(fromDir):
    f2 = filename  # 保存地址
    filename = destDir+'\\'+filename  # 打开地址
    img = Image.open(filename)
    # img=Image.open(r'C:\Users\邹盛\Desktop\验证码\蓝色\265.png')
    img_array = img.load()
    x,y = img.size

for i in range(y):
    for j in range(x):
        if (img_array[j, i][0] > 200 and img_array[j, i][1] < 110 and img_array[j, i][2] < 100
                and (img_array[j, i][2] + img_array[j, i][1]) < img_array[j,i][0]):
            img.putpixel((j, i), (0, 0, 0, 0))
        else:
            img.putpixel((j, i), (255, 255, 255, 255))

img = depoint(img)
cut(img, f2)