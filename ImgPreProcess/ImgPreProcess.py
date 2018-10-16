# 用于对下载的验证码进行二值化、降噪、切分
from PIL import Image
from pylab import *
import os
import math
from settings import YZM_SAVEFOLDER, YZM_CUTFOLDER


class ImgPreProcesser:
    '''
    处理下载的验证码，以便输入网络
    '''

    def Thresholding(self, imgFileName,):
        '''
        二值化，取出想要的文字部分
        :param imgFileName: 验证码图片的文件名
        :return:
        '''

        if not os.path.exists(YZM_SAVEFOLDER):
            os.makedirs(YZM_SAVEFOLDER)

        if not os.path.exists(YZM_CUTFOLDER):
            os.makedirs(YZM_CUTFOLDER)

        imgPath = YZM_SAVEFOLDER + '\\' + imgFileName
        img = Image.open(imgPath)
        imgArray = img.load()
        x, y = img.size

        if 'red' in str(imgFileName):
            for i in range(y):
                for j in range(x):
                    if (imgArray[j, i][0] > 200 and imgArray[j, i][1] < 110 and imgArray[j, i][2] < 100
                            and (imgArray[j, i][2] + imgArray[j, i][1]) < imgArray[j,i][0]):
                        img.putpixel((j, i), (0, 0, 0, 0))
                    else:
                        img.putpixel((j, i), (255, 255, 255, 255))

        elif 'blue' in str(imgFileName):
            for i in range(y):
                for j in range(x):
                    if (imgArray[j, i][0] < 100 and imgArray[j, i][1] < 100 and imgArray[j, i][2] > 200 and (
                            imgArray[j, i][0] + imgArray[j, i][1]) < imgArray[j, i][2]):
                        img.putpixel((j, i), (0, 0, 0, 0))
                    else:
                        img.putpixel((j, i), (255, 255, 255, 255))


        elif 'yellow' in str(imgFileName):
            for i in range(y):
                for j in range(x):
                    if (imgArray[j, i][0]
                            > 200 and imgArray[j, i][1] > 200 and imgArray[j, i][2] < 110):
                        img.putpixel((j, i), (0, 0, 0, 0))
                    else:
                        img.putpixel((j, i), (255, 255, 255, 255))

        return img


    # 去除噪点
    def Denoise(self, img):
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
                    # 如果一个点周围八个点有七个是空白，认为该点也应该是空白
                    img.putpixel((j, i), (255, 255, 255, 255))

        # 下面两个循环将图片最边缘一圈全部涂白
        for i in range(w):
                    img.putpixel((i, 0), (255, 255, 255, 255))
                    img.putpixel((i, h-1), (255, 255, 255, 255))

        for i in range(h):
                    img.putpixel((0, i), (255, 255, 255, 255))
                    img.putpixel((w-1, i), (255, 255, 255, 255))

        return img


    def Cut(self, filename, imgdata = None, ):
        '''
        将图片按字符切开
        :param img:
        :param filename:
        :return:
        '''
        if imgdata is None:
            img = Image.open(filename)

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
            # 变量blackDotsEachColumn记录下来每一列的黑点数量
            blackdotsEachColumn.append(count0)
            count0 = 0

        # 选定除了边框外的每一列，遍历查找字符的边缘列，每一个起始边缘都有一个对应的结束边缘
        for x in range(1, w - 1):
            # 从左到右，遍历查找起始边缘
            if (blackdotsEachColumn[x - 1] == 0 and blackdotsEachColumn[x] != 0):
                startEdge.append(x)
            # 从左到右，遍历查找结束边缘
            if (blackdotsEachColumn[x] != 0 and blackdotsEachColumn[x + 1] == 0):
                endEdge.append(x)

        # 归并本该在一起的部分
        for i in range(len(startEdge)):
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

        # 同样颜色的字符可能粘连，按平均宽度15切开
        for i in range(len(startEdge)):
            # 取每一个块的宽度
            blockWidth = endEdge[i] - startEdge[i]
            if (blockWidth > 15):
                p = math.ceil(blockWidth / 15)  # 向上取整
                for j in range(1, p):
                    k = int(startEdge[i] + j * blockWidth / p)
                    tmp1.append(k)
                    tmp2.append(k)

        # 从小到大排序
        tmp1.sort()
        tmp2.sort()

        startEdge = tmp1
        endEdge = tmp2

        # 切分图片
        for i in range(len(startEdge)):
            # 切割, crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
            child_img = img.crop((startEdge[i], 0, endEdge[i], h - 1))
            child_img_list.append(child_img)

        # 调整切分部分的大小并保存
        for i in range(len(child_img_list)):

            new_image = child_img_list[i].resize((16, h), Image.BILINEAR)
            saveDir = YZM_CUTFOLDER + '\\' + str(i) + filename
            new_image.save(saveDir)

        # 切分后删除原图片
        os.remove((YZM_SAVEFOLDER + '\\' + filename))


    def ImgPreProcess(self, CAPTCHAFileImgName):
        CAPTCHAFileImgName = CAPTCHAFileImgName
        # 先将需要识别与不需要识别的字符二值化
        img = self.Thresholding(CAPTCHAFileImgName,)
        # 去噪点
        img = self.Denoise(img)

        self.Cut(CAPTCHAFileImgName, img)

        print(CAPTCHAFileImgName, 'Done')


if __name__ == '__main__':
    pass