from PreProcesser import *

target_dir = 'D:\AliTest\wrong'
file = 'red_m.png'


def test_PreProcesser():
    # img = cv2.imread(target_dir + '\\' + file)
    imgPath = 'D:\\AliTest\\wrong\\red_u.png'
    i = ImgPreProcesser()
    img = i.thresholder('red', imgPath)
    cv2.imshow('thresholder',img)
    cv2.waitKey(0)
    print('threesholder：')
    print(i.img2base64(img))
    img = i.denoise(img)
    cv2.imshow('denoise', img)
    cv2.waitKey(0)
    print('denoise：')
    print(i.img2base64(img))


def thresholder(flag, imgPath):

    img = cv2.imread(imgPath)
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # RGB 转为 HSV

    if flag == 'yellow':
        Loweryellow = np.array([26, 43, 46])
        Upperyellow = np.array([34, 255, 255])
        img = cv2.inRange(HSV, Loweryellow, Upperyellow)
    elif flag == 'blue':
        Lowerblue = np.array([108, 43, 46])
        Upperblue = np.array([124, 255, 255])
        img = cv2.inRange(HSV, Lowerblue, Upperblue)
    elif flag == 'red':
        Lowerred0 = np.array([178, 140, 114])
        Upperred0 = np.array([180, 255, 255])
        img1 = cv2.inRange(HSV, Lowerred0, Upperred0)
        Lowerred1 = np.array([0, 140, 114])
        Upperred1 = np.array([11, 255, 255])
        img2 = cv2.inRange(HSV, Lowerred1, Upperred1)
        img = img1 + img2  # 红颜色在HSV空间上H值有两个范围
    elif flag == 'all':
        Lowerblack = np.array([0, 0, 0])
        Upperblack = np.array([180, 255, 46])
        img = cv2.inRange(HSV, Lowerblack, Upperblack)

    img2 = img.copy()
    height, width = img.shape

    for i in range(height):
        for j in range(width):
            img2[i, j] = (255 - img[i, j])

    img2 = cv2.medianBlur(img2, 1)
    cv2.imshow('lalal', img2)
    cv2.waitKey(0)

# if __name__ == '__main__':
#     imgPath = 'D:\AliTest\\wrong\\blue_bzf.png'
#     thresholder('blue', imgPath)


def test_TraceBar():
    img= cv2.imread(target_dir + '\\' + file)

    cv2.imshow("BGR", img) # 显示图片

    hsv_low = np.array([0, 0, 0])
    hsv_high = np.array([0, 0, 0])

    # 下面几个函数，写得有点冗余

    def h_low(value):
        hsv_low[0] = value

    def h_high(value):
        hsv_high[0] = value

    def s_low(value):
        hsv_low[1] = value

    def s_high(value):
        hsv_high[1] = value

    def v_low(value):
        hsv_low[2] = value

    def v_high(value):
        hsv_high[2] = value

    cv2.namedWindow('image')
    cv2.createTrackbar('H low', 'image', 0, 255, h_low)
    cv2.createTrackbar('H high', 'image', 0, 255, h_high)
    cv2.createTrackbar('S low', 'image', 0, 255, s_low)
    cv2.createTrackbar('S high', 'image', 0, 255, s_high)
    cv2.createTrackbar('V low', 'image', 0, 255, v_low)
    cv2.createTrackbar('V high', 'image', 0, 255, v_high)

    while True:
        dst = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # BGR转HSV
        dst = cv2.inRange(dst, hsv_low, hsv_high) # 通过HSV的高低阈值，提取图像部分区域
        cv2.imshow('dst', dst)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ =='__main__':
    imageBase64 = '''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'''
    print(base64.b64decode(imageBase64))
