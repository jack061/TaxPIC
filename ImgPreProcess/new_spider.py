from checker import Checker
import random
import torch
from torch.utils.data.dataloader import DataLoader
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
import time

class Cap_Net(nn.Module):
    # pytorch的bug，自定义class保存后，如果在新的文件里load，还需要重新定义class

    def __init__(self):
        super(Cap_Net, self).__init__()

        self.conv1 = nn.Conv2d(1, 16, 5)

        self.pooling = nn.MaxPool2d(2)

        self.conv2 = nn.Conv2d(16, 16, 5)

        self.pooling2 = nn.MaxPool2d(2)

        self.classfier = nn.Sequential(
            nn.Linear(400, 120),
            nn.ReLU(inplace=True),
            nn.Linear(120, 36),
        )

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x, inplace=True)
        x = self.pooling(x)

        x = self.conv2(x)
        x = F.relu(x, inplace=True)
        x = self.pooling2(x)
        x = x.view(-1, 400)
        x = self.classfier(x)

        return x


if __name__ == '__main__':
    success = 0
    total = 50
    for i in range(total):
        time.sleep(30)
        c = Checker()
        fpinfo = [
            {'fpdm': '044031700111', 'fphm': '28477743', 'kprq': '20171129', 'kjje': '227858'},
            {'fpdm': '033001700211', 'fphm': '58089105', 'kprq': '20180410', 'kjje': '604420'},
            {'fpdm': '033001700211', 'fphm': '17099263', 'kprq': '20171201', 'kjje': '336134'},
            {'fpdm': '044031700111', 'fphm': '28478760', 'kprq': '20171129', 'kjje': '737421'},
        ]
        fpinfo = random.choice(fpinfo)
        bOK, ret = c.CheckFp(fpinfo['fpdm'], fpinfo['fphm'], fpinfo['kprq'], fpinfo['kjje'])
        if bOK:
            success += 1
        print(ret)
    print('成功率: ', float(success / total), '%')
    print(success)