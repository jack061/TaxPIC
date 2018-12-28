# 从标注好的图片中随机选取五张作为测试集
import os
import shutil
import random

training_data_folder = r'D:\Code\TaxPIC\PIC\训练集'
test_data_folder = r'D:\Code\TaxPIC\PIC\测试集'
data_folders = os.listdir(training_data_folder)
for folder in data_folders:
    img_list = os.listdir(training_data_folder+ '\\'+ folder)
    if len(img_list) > 10:
        selected = random.sample(img_list, 5)
        dest = test_data_folder+'\\' + folder
        if not os.path.exists(dest):
            os.mkdir(dest)
        for each in selected:
            shutil.move(training_data_folder + '\\' + folder +'\\'+ each, dest)
    # print(str(folder ), str(len(img_list)), img_list)
