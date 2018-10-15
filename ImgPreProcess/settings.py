root_url = 'https://inv-veri.chinatax.gov.cn/' # 国税局发票查验平台的网址

yzm_version = 'V1.0.06_001' # 还没变

tax_citys={ #不同城市查验机关有不同的网址，根据这个去构造验证码图片和查验信息请求URL
        '1100':{'code':'1100','sfmc':'北京','Ip':'https://zjfpcyweb.bjsat.gov.cn:443','address':'https://zjfpcyweb.bjsat.gov.cn:443'},
        '1200':{'code':'1200','sfmc':'天津','Ip':'https://fpcy.tjsat.gov.cn:443','address':'https://fpcy.tjsat.gov.cn:443'},
        '1300':{'code':'1300','sfmc':'河北','Ip':'https://fpcy.he-n-tax.gov.cn:82','address':'https://fpcy.he-n-tax.gov.cn:82'},
        '1400':{'code':'1400','sfmc':'山西','Ip':'https://fpcy.tax.sx.cn:443','address':'https://fpcy.tax.sx.cn:443'},
        '1500':{'code':'1500','sfmc':'内蒙古','Ip':'https://fpcy.nm-n-tax.gov.cn:443','address':'https://fpcy.nm-n-tax.gov.cn:443'},
        '2100':{'code':'2100','sfmc':'辽宁','Ip':'https://fpcy.tax.ln.cn:443','address':'https://fpcy.tax.ln.cn:443'},
        '2102':{'code':'2102','sfmc':'大连','Ip':'https://fpcy.dlntax.gov.cn:443','address':'https://fpcy.dlntax.gov.cn:443'},
        '2200':{'code':'2200','sfmc':'吉林','Ip':'https://fpcy.jl-n-tax.gov.cn:4432','address':'https://fpcy.jl-n-tax.gov.cn:4432'},
        '2300':{'code':'2300','sfmc':'黑龙江','Ip':'https://fpcy.hl-n-tax.gov.cn:443','address':'https://fpcy.hl-n-tax.gov.cn:443'},
        '3100':{'code':'3100','sfmc':'上海','Ip':'https://fpcyweb.tax.sh.gov.cn:1001','address':'https://fpcyweb.tax.sh.gov.cn:1001'},
        '3200':{'code':'3200','sfmc':'江苏','Ip':'https://fpdk.jsgs.gov.cn:80','address':'https://fpdk.jsgs.gov.cn:80'},
        '3300':{'code':'3300','sfmc':'浙江','Ip':'https://fpcyweb.zjtax.gov.cn:443','address':'https://fpcyweb.zjtax.gov.cn:443'},
        '3302':{'code':'3302','sfmc':'宁波','Ip':'https://fpcy.nb-n-tax.gov.cn:443','address':'https://fpcy.nb-n-tax.gov.cn:443'},
        '3400':{'code':'3400','sfmc':'安徽','Ip':'https://fpcy.ah-n-tax.gov.cn:443','address':'https://fpcy.ah-n-tax.gov.cn:443'},
        '3500':{'code':'3500','sfmc':'福建','Ip':'https://fpcyweb.fj-n-tax.gov.cn:443','address':'https://fpcyweb.fj-n-tax.gov.cn:443'},
        '3502':{'code':'3502','sfmc':'厦门','Ip':'https://fpcy.xm-n-tax.gov.cn','address':'https://fpcy.xm-n-tax.gov.cn'},
        '3600':{'code':'3600','sfmc':'江西','Ip':'https://fpcy.jxgs.gov.cn:82','address':'https://fpcy.jxgs.gov.cn:82'},
        '3700':{'code':'3700','sfmc':'山东','Ip':'https://fpcy.sd-n-tax.gov.cn:443','address':'https://fpcy.sd-n-tax.gov.cn:443'},
        '3702':{'code':'3702','sfmc':'青岛','Ip':'https://fpcy.qd-n-tax.gov.cn:443','address':'https://fpcy.qd-n-tax.gov.cn:443'},
        '4100':{'code':'4100','sfmc':'河南','Ip':'https://fpcy.ha-n-tax.gov.cn','address':'https://fpcy.ha-n-tax.gov.cn'},
        '4200':{'code':'4200','sfmc':'湖北','Ip':'https://fpcy.hb-n-tax.gov.cn:443','address':'https://fpcy.hb-n-tax.gov.cn:443'},
        '4300':{'code':'4300','sfmc':'湖南','Ip':'https://fpcy.hntax.gov.cn:8083','address':'https://fpcy.hntax.gov.cn:8083'},
        '4400':{'code':'4400','sfmc':'广东','Ip':'https://fpcy.gd-n-tax.gov.cn:443','address':'https://fpcy.gd-n-tax.gov.cn:443'},
        '4403':{'code':'4403','sfmc':'深圳','Ip':'https://fpcy.szgs.gov.cn:443','address':'https://fpcy.szgs.gov.cn:443'},
        '4500':{'code':'4500','sfmc':'广西','Ip':'https://fpcy.gxgs.gov.cn:8200','address':'https://fpcy.gxgs.gov.cn:8200'},
        '4600':{'code':'4600','sfmc':'海南','Ip':'https://fpcy.hitax.gov.cn:443','address':'https://fpcy.hitax.gov.cn:443'},
        '5000':{'code':'5000','sfmc':'重庆','Ip':'https://fpcy.cqsw.gov.cn:80','address':'https://fpcy.cqsw.gov.cn:80'},
        '5100':{'code':'5100','sfmc':'四川','Ip':'https://fpcy.sc-n-tax.gov.cn:443','address':'https://fpcy.sc-n-tax.gov.cn:443'},
        '5200':{'code':'5200','sfmc':'贵州','Ip':'https://fpcy.gz-n-tax.gov.cn:80','address':'https://fpcy.gz-n-tax.gov.cn:80'},
        '5300':{'code':'5300','sfmc':'云南','Ip':'https://fpcy.yngs.gov.cn:443','address':'https://fpcy.yngs.gov.cn:443'},
        '5400':{'code':'5400','sfmc':'西藏','Ip':'https://fpcy.xztax.gov.cn:81','address':'https://fpcy.xztax.gov.cn:81'},
        '6100':{'code':'6100','sfmc':'陕西','Ip':'https://fpcyweb.sn-n-tax.gov.cn:443','address':'https://fpcyweb.sn-n-tax.gov.cn:443'},
        '6200':{'code':'6200','sfmc':'甘肃','Ip':'https://fpcy.gs-n-tax.gov.cn:443','address':'https://fpcy.gs-n-tax.gov.cn:443'},
        '6300':{'code':'6300','sfmc':'青海','Ip':'https://fpcy.qh-n-tax.gov.cn:443','address':'https://fpcy.qh-n-tax.gov.cn:443'},
        '6400':{'code':'6400','sfmc':'宁夏','Ip':'https://fpcy.nxgs.gov.cn:443','address':'https://fpcy.nxgs.gov.cn:443'},
        '6500':{'code':'6500','sfmc':'新疆','Ip':'https://fpcy.xj-n-tax.gov.cn:443','address':'https://fpcy.xj-n-tax.gov.cn:443'}
        }

networkPath = 'D:\Code\TaxPIC\model\(69)-net.pkl'
ImageFolder = 'D:\pic\切分'  # 切分后的图片的存放地址
dataset_dir = 'D:\Code\TaxPIC\PIC\预处理'
yzm_SaveDir = r'D:\\pic'  # 存放原始图片文件的文件夹
yzm_CutDir = r'D:\\pic\\切分\\1'  # 处理后的图片存放位置
