from PIL import Image
import os
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
def choose_threshold(img):
    # img = img.convert("L")
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
    # for j, k in sorted(values.items(), key=lambda x: x[1], reverse=True)[:10]:
    #     print(j, k)
    for j, k in sorted(values.items(), key=lambda x: x[1], reverse=True)[:10]:
        sum = sum + j * k
        ever = ever + k
    threshold1=sum/ever
# 计算平均灰度值
# 计算最小阈值
#     imgry = img.convert("L")
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
        # print(threshold2)
        for i in range(256):
            values[i] = his[i]
            # print(i)
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
c=1
for filename in os.listdir(r'C:\Users\邹盛\Desktop\验证码\黄色'): #listdir的参数是文件夹的路径
 f2 = r'G:\验证码\100.5' + '\\' + filename  # 保存地址
 filename=r'C:\Users\邹盛\Desktop\验证码\黄色'+'\\'+filename#打开地址
 image= Image.open(filename)
 imgry = image.convert("L")
 his = imgry.histogram()
 values = {}
 sum=0
 ever=0
 a=[]
 b=[]
 for i in range(256):
    values[i] = his[i]
 for j,k in sorted(values.items(),key=lambda x:x[1],reverse = True)[:2]:
    # print ("灰度："+str(j),"个数:"+str(k))
    sum=sum+k
    a.append(j)#灰度
    b.append(k)#个数
 ever = a[0] * (b[0] / sum) + a[1] * (b[1] / sum)
 if ever < 200:
     if b[0]>2000 and (b[0]/ever)<11:
         table = get_bin_table(ever)
         out = imgry.point(table, '1')
         his = out.histogram()
         values = {}
         for i in range(256):
             values[i] = his[i]
         while (values[0] > values[1]):
             ever = ever + 0.1
             table = get_bin_table(ever)
             out = imgry.point(table, '1')
             his = out.histogram()
             for i in range(256):
                 values[i] = his[i]
     elif 1700<b[0]<2000 and ever>185 and (a[1]-a[0])<35:
         his = imgry.histogram()
         values = {}
         for i in range(256):
             values[i] = his[i]
         while (values[0] > values[1]):
             ever = ever + 0.1
             table = get_bin_table(ever)
             out = imgry.point(table, '1')
             his = out.histogram()
             for i in range(256):
                 values[i] = his[i]
     else:
       ever=ever-4
 else:
     if a[0]>a[1] and (a[0]-a[1])<(ever-200):
         ever = 100
         table = get_bin_table(ever)
         out = imgry.point(table, '1')
         his = out.histogram()
         values = {}
         for i in range(256):
             values[i] = his[i]
         while (values[0] > values[1]):
             ever = ever + 0.1
             table = get_bin_table(ever)
             out = imgry.point(table, '1')
             his = out.histogram()
             for i in range(256):
                 values[i] = his[i]
     elif a[0]<a[1] and (a[1]-a[0])>15:
         ever=a[0]
         table = get_bin_table(ever)
         out = imgry.point(table, '1')
         his = out.histogram()
         values = {}
         for i in range(256):
             values[i] = his[i]
         while (values[0] > values[1]):
             ever = ever + 0.1
             table = get_bin_table(ever)
             out = imgry.point(table, '1')
             his = out.histogram()
             for i in range(256):
                 values[i] = his[i]
     table = get_bin_table(ever)
     out = imgry.point(table, '1')
     his = imgry.histogram()
     values = {}
     for i in range(256):
         values[i] = his[i]
     while (values[0] > values[1]):
         ever = ever + 0.1
         table = get_bin_table(ever)
         out = imgry.point(table, '1')
         his = out.histogram()
         for i in range(256):
             values[i] = his[i]
     print("文件名" + filename)
     for i in range(256):
         values[i] = his[i]
     for j, k in sorted(values.items(), key=lambda x: x[1], reverse=True)[:2]:
      print ("灰度："+str(j),"个数:"+str(k))
     table = get_bin_table(ever)
     out = imgry.point(table, '1')
     print(ever)
     out.save(f2)
     values.clear()
     his.clear()

