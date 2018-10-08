# 用于对下载的验证码进行二值化、降噪、切分
from PIL import Image
from pylab import *
import os
import math


fromDir = r'D:\\pic'  # 存放原始图片文件的文件夹
destDir = r'D:\\pic\\切分\\1'  # 处理后的图片存放位置


def Thresholding(imgName, colorflag):  # 二值化，取出想要的文字部分
    
    if not os.path.exists(fromDir):
        os.makedirs(fromDir)  
        
    if not os.path.exists(destDir):
        os.makedirs(destDir) 

    imgPath = fromDir + '\\' + imgName
    img = Image.open(imgPath)
    imgArray = img.load()
    x, y = img.size
    if colorflag == 'redWanted':
        for i in range(y):
            for j in range(x):
                if (imgArray[j, i][0] > 200 and imgArray[j, i][1] < 110 and imgArray[j, i][2] < 100
                        and (imgArray[j, i][2] + imgArray[j, i][1]) < imgArray[j,i][0]):
                    img.putpixel((j, i), (0, 0, 0, 0))
                else:
                    img.putpixel((j, i), (255, 255, 255, 255))

    elif colorflag == 'blueWanted':
        for i in range(y):
            for j in range(x):
                if (imgArray[j, i][0] < 100 and imgArray[j, i][1] < 100 and imgArray[j, i][2] > 200 and (
                        imgArray[j, i][0] + imgArray[j, i][1]) < imgArray[j, i][2]):
                    img.putpixel((j, i), (0, 0, 0, 0))
                else:
                    img.putpixel((j, i), (255, 255, 255, 255))

    elif colorflag == 'yellowWanted':
        for i in range(y):
            for j in range(x):
                if (imgArray[j, i][0]
                        > 200 and imgArray[j, i][1] > 200 and imgArray[j, i][2] < 110):
                    img.putpixel((j, i), (0, 0, 0, 0))
                else:
                    img.putpixel((j, i), (255, 255, 255, 255))

    elif colorflag == 'allWanted':  # 暂时不用，因为找不到好的二值化方法
        pass

    return img


def Denoise(img):   # 去除噪点
    imgArray = img.load()
    w, h = img.size
    for i in range(1, h-1):
        for j in range(1, w-1):
            count = 0
            if  (imgArray[j,i-1][0] == 255 and imgArray[j,i-1][1] == 255 and imgArray[j,i-1][2] == 255):
                count = count + 1
            if (imgArray[j,i+1][0] == 255 and imgArray[j,i+1][1]==255 and imgArray[j,i+1][2]==255):
                count = count + 1
            if (imgArray[j-1,i][0]==255 and imgArray[j-1,i][1]==255 and imgArray[j-1,i][2]==255):
                count = count + 1
            if  (imgArray[j+1,i][0]==255 and imgArray[j+1,i][1]==255 and imgArray[j+1,i][2]==255):
                count = count + 1
            if (imgArray[j+1,i+1][0]==255 and imgArray[j+1,i+1][1]==255 and imgArray[j+1,i+1][2]==255):
                count = count + 1
            if (imgArray[j+1,i-1][0]==255 and imgArray[j+1,i-1][1]==255 and imgArray[j+1,i-1][2]==255):
                count = count + 1
            if (imgArray[j-1,i-1][0]==255 and imgArray[j-1,i-1][1]==255 and imgArray[j-1,i-1][2]==255):
                count = count + 1
            if (imgArray[j-1,i+1][0]==255 and imgArray[j-1,i+1][1]==255 and imgArray[j-1,i+1][2]==255):
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


def Cut(img, filename):
    child_img_list = []
    w, h = img.size
    startEdge = []
    endEdge = []
    blackdotsEachColumn = []
    count0 = 0
    imgArray = img.load()
    for x in range(w):
        for y in range(h):
            if (imgArray[x, y] == (0, 0, 0)):
                count0 = count0 + 1
        blackdotsEachColumn.append(count0)  # 变量blackDotsEachColumn记录下来每一列的黑点数量
        count0 = 0

    for x in range(1, w - 1):  # 选定除了边框外的每一列，遍历查找字符的边缘列，每一个起始边缘都有一个对应的结束边缘
        if (blackdotsEachColumn[x - 1] == 0 and blackdotsEachColumn[x] != 0):  # 从左到右，遍历查找起始边缘
            startEdge.append(x)
        if (blackdotsEachColumn[x] != 0 and blackdotsEachColumn[x + 1] == 0):  # 从左到右，遍历查找结束边缘
            endEdge.append(x)

    for i in range(len(startEdge)):  # 归并本该在一起的部分
        # 如果一个块太小，可以认为它属于前一个或后一个块
        if ((i < (len(startEdge) - 1)) and len(startEdge) >= 1):  # 如果只有一个起始边缘，就不需要归并了

            # 第一个块没有前一个块，所以如果横向纵向都太小的话，认为跟后一个块是一体的
            if (i == 0 and ((endEdge[i] - startEdge[i]) <= 3) and (blackdotsEachColumn[startEdge[i]] <= 2) and (blackdotsEachColumn[endEdge[i]] <= 2)):
                startEdge.pop(i + 1)
                endEdge.pop(i)
                continue

            if (i != 0 and ((endEdge[i] - startEdge[i]) <= 3) and (blackdotsEachColumn[startEdge[i]] <= 2) and (blackdotsEachColumn[endEdge[i]] <= 2)):

                # 可以认为这个小块是属于前面或者后面的一个块，根据前后距离判断是属于哪个
                if ((startEdge[i + 1] - endEdge[i]) < (startEdge[i] - endEdge[i - 1])):
                    startEdge.pop(i + 1)
                    endEdge.pop(i)
                    continue

                else:
                    startEdge.pop(i)
                    endEdge.pop(i - 1)
                    continue


    tmp1 = startEdge
    tmp2 = endEdge

    for i in range(len(startEdge)):  # 同样颜色的字符可能粘连，按平均宽度15切开
        blockWidth = endEdge[i] - startEdge[i]  # 取每一个块的宽度
        if (blockWidth > 15):  # 如果一个字符块宽度大于15列
            p = math.ceil(blockWidth / 15)  # 向上取整
            for j in range(1, p):
                k = int(startEdge[i] + j * blockWidth / p)
                tmp1.append(k)
                tmp2.append(k)

    # 从小到大排序
    tmp1.sort()  # 开始
    tmp2.sort()  # 结束

    startEdge = tmp1
    endEdge = tmp2

    # 切分图片并保存
    for i in range(len(startEdge)):

        child_img = img.crop((startEdge[i], 0, endEdge[i], h - 1))  # 切割, crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
        child_img_list.append(child_img)

    for i in range(len(child_img_list)):  # 调整大小并保存

        new_image = child_img_list[i].resize((16, h), Image.BILINEAR)
        saveDir = destDir + '\\' + str(i) + filename
        new_image.save(saveDir)


def whatyYouWant(filename):
    if '红色' in str(filename):
        colorflag = 'redWanted'
    elif '蓝色' in str(filename):
        colorflag = 'blueWanted'
    elif '黄色' in str(filename):
        colorflag = 'yellowWanted'
    else:
        colorflag = 'allWanted'
    return colorflag


def imgPreProcess(CAPTCHAFileImgName):
    CAPTCHAFileImgName = CAPTCHAFileImgName
    colorflag = whatyYouWant(CAPTCHAFileImgName)
    img = Thresholding(CAPTCHAFileImgName, colorflag)  #先将需要识别与不需要识别的字符二值化
    img = Denoise(img)  #去噪点
    # print(CAPTCHAFileImgName)

    Cut(img, CAPTCHAFileImgName)
    os.remove((fromDir + '\\' + CAPTCHAFileImgName))

    print(CAPTCHAFileImgName, 'Done')


if __name__ == '__main__':
    pass