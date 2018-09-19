import torch
from torch.utils.data.dataloader import DataLoader
import torchvision
from torchvision import transforms
from network import *


def identity(networkPath,ImageFolder):
    # net = Cap_Net()
    net = torch.load_state_dict(torch.load(networkPath))

    tranforms_test = transforms.Compose([  # 预定义图片转换规则

        transforms.ToTensor(),

    ])
    test_dataset = torchvision.datasets.ImageFolder(ImageFolder, transform=tranforms_test)
    test_data = DataLoader(test_dataset,)
    
    to_pil_image = transforms.ToPILImage()


    img = to_pil_image(image[0])

    net.eval()

  
    outputs = net(img)  # net直接前向传播然后输出

    _, predicted = torch.max(outputs.data, 1)  # 返回的是交叉熵函数的最大概率预测。

    print("结果：" + str(predicted))

    # print('识别准确率为：%d%%' % (100 * correct / total))

if __name__ == '__main__':
    identity()