from ImgPreProcess.checker import Checker
import random
c = Checker()
fpinfo = [
        {'fpdm': '044031700111', 'fphm': '28477743', 'kprq': '20171129', 'kjje': '227858'},
        {'fpdm': '033001700211', 'fphm': '58089105', 'kprq': '20180410', 'kjje': '604420'},
        {'fpdm': '033001700211', 'fphm': '17099263', 'kprq': '20171201', 'kjje': '336134'},
        {'fpdm': '044031700111', 'fphm': '28478760', 'kprq': '20171129', 'kjje': '737421'},
    ]
fpinfo = random.choice(fpinfo)
r1, r2 = c._get_yzm_image(fpinfo.get('fpdm'), fpinfo.get('fphm'))
print(r1)
print(r2)