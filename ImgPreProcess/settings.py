root_url = 'https://inv-veri.chinatax.gov.cn/' # 国税局发票查验平台的网址

yzm_version = 'V1.0.06_001' # 还没变

tax_citys={ #不同城市查验机关有不同的网址，根据这个去构造验证码图片和查验信息请求URL
        '1100':{'code':'1100','sfmc':'北京','Url':'https://zjfpcyweb.bjsat.gov.cn:443','address':'https://zjfpcyweb.bjsat.gov.cn:443'},
        '1200':{'code':'1200','sfmc':'天津','Url':'https://fpcy.tjsat.gov.cn:443','address':'https://fpcy.tjsat.gov.cn:443'},
        '1300':{'code':'1300','sfmc':'河北','Url':'https://fpcy.he-n-tax.gov.cn:82','address':'https://fpcy.he-n-tax.gov.cn:82'},
        '1400':{'code':'1400','sfmc':'山西','Url':'https://fpcy.tax.sx.cn:443','address':'https://fpcy.tax.sx.cn:443'},
        '1500':{'code':'1500','sfmc':'内蒙古','Url':'https://fpcy.nm-n-tax.gov.cn:443','address':'https://fpcy.nm-n-tax.gov.cn:443'},
        '2100':{'code':'2100','sfmc':'辽宁','Url':'https://fpcy.tax.ln.cn:443','address':'https://fpcy.tax.ln.cn:443'},
        '2102':{'code':'2102','sfmc':'大连','Url':'https://fpcy.dlntax.gov.cn:443','address':'https://fpcy.dlntax.gov.cn:443'},
        '2200':{'code':'2200','sfmc':'吉林','Url':'https://fpcy.jl-n-tax.gov.cn:4432','address':'https://fpcy.jl-n-tax.gov.cn:4432'},
        '2300':{'code':'2300','sfmc':'黑龙江','Url':'https://fpcy.hl-n-tax.gov.cn:443','address':'https://fpcy.hl-n-tax.gov.cn:443'},
        '3100':{'code':'3100','sfmc':'上海','Url':'https://fpcyweb.tax.sh.gov.cn:1001','address':'https://fpcyweb.tax.sh.gov.cn:1001'},
        '3200':{'code':'3200','sfmc':'江苏','Url':'https://fpdk.jsgs.gov.cn:80','address':'https://fpdk.jsgs.gov.cn:80'},
        '3300':{'code':'3300','sfmc':'浙江','Url':'https://fpcyweb.zjtax.gov.cn:443','address':'https://fpcyweb.zjtax.gov.cn:443'},
        '3302':{'code':'3302','sfmc':'宁波','Url':'https://fpcy.nb-n-tax.gov.cn:443','address':'https://fpcy.nb-n-tax.gov.cn:443'},
        '3400':{'code':'3400','sfmc':'安徽','Url':'https://fpcy.ah-n-tax.gov.cn:443','address':'https://fpcy.ah-n-tax.gov.cn:443'},
        '3500':{'code':'3500','sfmc':'福建','Url':'https://fpcyweb.fj-n-tax.gov.cn:443','address':'https://fpcyweb.fj-n-tax.gov.cn:443'},
        '3502':{'code':'3502','sfmc':'厦门','Url':'https://fpcy.xm-n-tax.gov.cn','address':'https://fpcy.xm-n-tax.gov.cn'},
        '3600':{'code':'3600','sfmc':'江西','Url':'https://fpcy.jxgs.gov.cn:82','address':'https://fpcy.jxgs.gov.cn:82'},
        '3700':{'code':'3700','sfmc':'山东','Url':'https://fpcy.sd-n-tax.gov.cn:443','address':'https://fpcy.sd-n-tax.gov.cn:443'},
        '3702':{'code':'3702','sfmc':'青岛','Url':'https://fpcy.qd-n-tax.gov.cn:443','address':'https://fpcy.qd-n-tax.gov.cn:443'},
        '4100':{'code':'4100','sfmc':'河南','Url':'https://fpcy.ha-n-tax.gov.cn','address':'https://fpcy.ha-n-tax.gov.cn'},
        '4200':{'code':'4200','sfmc':'湖北','Url':'https://fpcy.hb-n-tax.gov.cn:443','address':'https://fpcy.hb-n-tax.gov.cn:443'},
        '4300':{'code':'4300','sfmc':'湖南','Url':'https://fpcy.hntax.gov.cn:8083','address':'https://fpcy.hntax.gov.cn:8083'},
        '4400':{'code':'4400','sfmc':'广东','Url':'https://fpcy.gd-n-tax.gov.cn:443','address':'https://fpcy.gd-n-tax.gov.cn:443'},
        '4403':{'code':'4403','sfmc':'深圳','Url':'https://fpcy.szgs.gov.cn:443','address':'https://fpcy.szgs.gov.cn:443'},
        '4500':{'code':'4500','sfmc':'广西','Url':'https://fpcy.gxgs.gov.cn:8200','address':'https://fpcy.gxgs.gov.cn:8200'},
        '4600':{'code':'4600','sfmc':'海南','Url':'https://fpcy.hitax.gov.cn:443','address':'https://fpcy.hitax.gov.cn:443'},
        '5000':{'code':'5000','sfmc':'重庆','Url':'https://fpcy.cqsw.gov.cn:80','address':'https://fpcy.cqsw.gov.cn:80'},
        '5100':{'code':'5100','sfmc':'四川','Url':'https://fpcy.sc-n-tax.gov.cn:443','address':'https://fpcy.sc-n-tax.gov.cn:443'},
        '5200':{'code':'5200','sfmc':'贵州','Url':'https://fpcy.gz-n-tax.gov.cn:80','address':'https://fpcy.gz-n-tax.gov.cn:80'},
        '5300':{'code':'5300','sfmc':'云南','Url':'https://fpcy.yngs.gov.cn:443','address':'https://fpcy.yngs.gov.cn:443'},
        '5400':{'code':'5400','sfmc':'西藏','Url':'https://fpcy.xztax.gov.cn:81','address':'https://fpcy.xztax.gov.cn:81'},
        '6100':{'code':'6100','sfmc':'陕西','Url':'https://fpcyweb.sn-n-tax.gov.cn:443','address':'https://fpcyweb.sn-n-tax.gov.cn:443'},
        '6200':{'code':'6200','sfmc':'甘肃','Url':'https://fpcy.gs-n-tax.gov.cn:443','address':'https://fpcy.gs-n-tax.gov.cn:443'},
        '6300':{'code':'6300','sfmc':'青海','Url':'https://fpcy.qh-n-tax.gov.cn:443','address':'https://fpcy.qh-n-tax.gov.cn:443'},
        '6400':{'code':'6400','sfmc':'宁夏','Url':'https://fpcy.nxgs.gov.cn:443','address':'https://fpcy.nxgs.gov.cn:443'},
        '6500':{'code':'6500','sfmc':'新疆','Url':'https://fpcy.xj-n-tax.gov.cn:443','address':'https://fpcy.xj-n-tax.gov.cn:443'}
        }

NETWORK_PATH = r'D:\Code\TaxPIC\model\(69)-net.pkl'  # 保存的网络
IMAGE_FOLDER = r'D:\pic\切分'  # 存放切分后的图片
DATASET_FOLDER = r'D:\Code\TaxPIC\PIC\预处理'  # 存放神经网络训练数据集
YZM_SAVEFOLDER = r'D:\pic'  # 存放下载的原始验证码图片
YZM_CUTFOLDER = r'D:\pic\切分\1'  # 存放处理后切分的图片

MODE = 'test'
