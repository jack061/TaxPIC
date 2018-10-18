from checker import Checker
import torch.nn as nn
import torch.nn.functional as F
import time

from settings import YZM_SAVEFOLDER ,MODE
import tkinter as tk
from tkinter import messagebox
from check_response_parser import *
import  threading


# pytorch的bug，自定义class保存后，如果在新的文件里load，还需要重新定义class
class Cap_Net(nn.Module):

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


class Checker_Gui(object):
    def __init__(self, master, func):

        self.mainWindow = master
        self.mainWindow.title('发票查验')  # 窗口标题
        self.mainWindow.geometry('600x600')  # 窗口大小

        self.fpdm_label = tk.Label(self.mainWindow, text="发票代码")
        self.fpdm_label.grid(row=0, )
        self.fphm_label= tk.Label(self.mainWindow, text="发票号码")
        self.fphm_label.grid(row=1)
        self.kprq_label = tk.Label(self.mainWindow, text="开票日期")
        self.kprq_label.grid(row=2)
        self.kjje_label = tk.Label(self.mainWindow, text="开具金额/校验码")
        self.kjje_label.grid(row=3)

        self.input_fpdm = tk.Entry(self.mainWindow, )
        self.input_fpdm.grid(row=0, column=1)
        self.input_fphm = tk.Entry(self.mainWindow, )
        self.input_fphm.grid(row=1, column=1)
        self.input_kprq = tk.Entry(self.mainWindow, )
        self.input_kprq.grid(row=2, column=1)
        self.input_kjje = tk.Entry(self.mainWindow, )
        self.input_kjje.grid(row=3, column=1)

        self.result_box = tk.Text(self.mainWindow, height=10)
        self.result_box.grid(columnspan=2)

        self.check_button = tk.Button(self.mainWindow, text="查验发票", width=15, height=2, command=func)
        self.check_button.grid(columnspan=2)  # 放置按钮


    def Gui_Run(self):
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainWindow.mainloop()  # 显示窗口

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)


class ThreadClient(object):

    def __init__(self, master):
        self.master = master
        self.gui = Checker_Gui(master, self.starting)  # 将我们定义的GUI类赋给服务类的属性，将执行的功能函数作为参数传入

    def start_checker(self, fpinfo):
        bOK = False
        while bOK is False:
            time.sleep(5)
            c = Checker()

            bOK, ret = c.CheckFp(fpinfo['fpdm'], fpinfo['fphm'], fpinfo['kprq'], fpinfo['kjje'])
        return ret

    def click_check_button(self,):
        self.gui.result_box.delete(0.0, tk.END)
        fpdm = self.gui.input_fpdm.get()
        fphm = self.gui.input_fphm.get()
        kprq = self.gui.input_kprq.get()
        kjje = self.gui.input_kjje.get()
        if MODE == 'test':
            fpinfo = {'fpdm': '044031700111', 'fphm': '28477743', 'kprq': '20171129', 'kjje': '227858'}
        else:
            fpinfo = {'fpdm': fpdm, 'fphm': fphm, 'kprq': kprq, 'kjje': kjje}

        res = self.start_checker(fpinfo)
        ret = response_parser(res)

        self.gui.result_box.insert('current', str(ret))

    def starting(self):
        self.thread = threading.Thread(target=self.click_check_button)
        self.thread.start()


if __name__ == '__main__':

    root = tk.Tk()
    tool = ThreadClient(root)
    root.mainloop()
