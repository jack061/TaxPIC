import cv2
import numpy as np

"""
功能：读取一张图片，显示出来，转化为HSV色彩空间
     并通过滑块调节HSV阈值，实时显示
     便于调整阈值
"""

def test(imgPath):

    img = cv2.imread(imgPath)
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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
    cv2.createTrackbar('H low', 'image', 108, 124, h_low)
    cv2.createTrackbar('H high', 'image', 108, 124, h_high)
    cv2.createTrackbar('S low', 'image', 43, 255, s_low)
    cv2.createTrackbar('S high', 'image', 43, 255, s_high)
    cv2.createTrackbar('V low', 'image', 46, 255, v_low)
    cv2.createTrackbar('V high', 'image', 46, 255, v_high)

    while True:
        dst = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # BGR转HSV
        dst = cv2.inRange(dst, hsv_low, hsv_high) # 通过HSV的高低阈值，提取图像部分区域
        cv2.imshow('dst', dst)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    imgPath = 'D:\AliTest\\wrong\\blue_T.png'
    test(imgPath)