from PIL import Image
import PIL.ImageOps
from PIL import ImageEnhance
def get_bin_table(threshold):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if 0<i < (threshold):
            table.append(0)#白色
        else:
            table.append(1)#黑色

    return table
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
    if ever > 200:
        return (ever - 1)
    else:
        return (ever - 4)
image= Image.open(r'C:\Users\邹盛\Desktop\验证码\蓝色\8.png')
imgry = image.convert("L")
# his = imgry.histogram()
# values = {}
# sum=0
# ever1=0
# a=[]
# b=[]
# for i in range(256):
#     values[i] = his[i]
# for j,k in sorted(values.items(),key=lambda x:x[1],reverse = True)[:2]:
#     print (j,k)
#     sum=sum+k
#     a.append(j)
#     b.append(k)
# ever1=a[0]*(b[0]/sum)+a[1]*(b[1]/sum)
# if ever1 > 200:
#     ever1=ever1 - 1
# else:
#     ever1=ever1 - 6
# ever=choose_threshold2(imgry)
ever=100
table = get_bin_table(ever)
out = imgry.point(table, '1')
his = imgry.histogram()
values = {}
sum = 0
a = []
b = []
# for i in range(256):
#     values[i] = his[i]
# for j, k in sorted(values.items(), key=lambda x: x[1], reverse=True)[:2]:
#     print ("灰度："+str(j),"个数:"+str(k))
#     sum = sum + k
#     a.append(j)  # 灰度
#     b.append(k)  # 个数
# ever1 = a[0] * (b[0] / sum) + a[1] * (b[1] / sum)
# print(ever1)
for i in range(256):
        values[i] = his[i]
while (values[0] > values[1]):
        ever = ever + 0.1
        table = get_bin_table(ever)
        out = imgry.point(table, '1')
        his = out.histogram()
        for i in range(256):
            values[i] = his[i]
out=out.convert("L")

print(ever)
out.show()
