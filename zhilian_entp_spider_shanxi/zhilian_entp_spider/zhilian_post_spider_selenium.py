# _*_ coding=utf-8 _*_

import selenium.webdriver as webdriver
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import random
import pymysql

# https://sou.zhaopin.com/?jl=736&re=2059&in=10100&sf=0&st=0
# https://sou.zhaopin.com/?jl=736&re=2367&in=10100&sf=0&st=0
class ZhilianSpider(object):
    firefoxPath = "D:\\software\\Firefox\\geckodriver.exe"
    lvliang = "https://www.zhaopin.com/lvliang"
    sou = "https://sou.zhaopin.com/?jl=586&in={}&sf=0&st=0"

    keyword = ""

    # 领域
    # indentrys= [{'parentKey':'10100','value':'互联网/电子商务','key':'210500'[{'parentKey':'10100','value':'互联网/电子商务','key':'210500'},{'parentKey':'10100','value':'计算机软件','key':'160400'},{'parentKey':'10100','value':'IT服务(系统/数据/维护)','key':'160000'},{'parentKey':'10100','value':'电子技术/半导体/集成电路','key':'160500'},{'parentKey':'10100','value':'计算机硬件','key':'160200'},{'parentKey':'10100','value':'通信/电信/网络设备','key':'300100'},{'parentKey':'10100','value':'通信/电信运营、增值服务','key':'160100'},{'parentKey':'10100','value':'网络游戏','key':'160600'},{'parentKey':'10200','value':'基金/证券/期货/投资','key':'180000'},{'parentKey':'10200','value':'保险','key':'180100'},{'parentKey':'0','value':'IT|通信|电子|互联网','key':'10100'},{'parentKey':'10200','value':'银行','key':'300500'},{'parentKey':'0','value':'金融业','key':'10200'},{'parentKey':'10200','value':'信托/担保/拍卖/典当','key':'300900'},{'parentKey':'0','value':'房地产|建筑业','key':'10800'},{'parentKey':'10800','value':'房地产/建筑/建材/工程','key':'140000'},{'parentKey':'0','value':'商业服务','key':'10900'},{'parentKey':'10800','value':'家居/室内设计/装饰装潢','key':'140100'},{'parentKey':'0','value':'贸易|批发|零售|租赁业','key':'10300'},{'parentKey':'10800','value':'物业管理/商业中心','key':'140200'},{'parentKey':'0','value':'文体教育|工艺美术','key':'10400'},{'parentKey':'10900','value':'专业服务/咨询(财会/法律/人力资源等)','key':'200300'},{'parentKey':'0','value':'生产|加工|制造','key':'10500'},{'parentKey':'10900','value':'广告/会展/公关','key':'200302'},{'parentKey':'0','value':'交通|运输|物流|仓储','key':'11500'},{'parentKey':'10900','value':'中介服务','key':'201400'},{'parentKey':'0','value':'服务业','key':'10000'},{'parentKey':'10900','value':'检验/检测/认证','key':'201300'},{'parentKey':'0','value':'文化|传媒|娱乐|体育','key':'11300'},{'parentKey':'10900','value':'外包服务','key':'300300'},{'parentKey':'0','value':'能源|矿产|环保','key':'11600'},{'parentKey':'10300','value':'快速消费品（食品/饮料/烟酒/日化）','key':'120400'},{'parentKey':'0','value':'政府|非盈利机构','key':'11100'},{'parentKey':'10300','value':'耐用消费品（服饰/纺织/皮革/家具/家电）','key':'120200'},{'parentKey':'0','value':'农|林|牧|渔|其他','key':'11400'},{'parentKey':'10300','value':'贸易/进出口','key':'170500'},{'parentKey':'10300','value':'零售/批发','key':'170000'},{'parentKey':'10300','value':'租赁服务','key':'300700'},{'parentKey':'10400','value':'教育/培训/院校','key':'201100'},{'parentKey':'10400','value':'礼品/玩具/工艺美术/收藏品/奢侈品','key':'120800'},{'parentKey':'10500','value':'汽车/摩托车','key':'121000'},{'parentKey':'10500','value':'大型设备/机电设备/重工业','key':'129900'},{'parentKey':'10500','value':'加工制造（原料加工/模具）','key':'121100'},{'parentKey':'10500','value':'仪器仪表及工业自动化','key':'121200'},{'parentKey':'10500','value':'印刷/包装/造纸','key':'210600'},{'parentKey':'10500','value':'办公用品及设备','key':'120700'},{'parentKey':'10500','value':'医药/生物工程','key':'121300'},{'parentKey':'10500','value':'医疗设备/器械','key':'121500'},{'parentKey':'10500','value':'航空/航天研究与制造','key':'300000'},{'parentKey':'11500','value':'交通/运输','key':'150000'},{'parentKey':'11500','value':'物流/仓储','key':'301100'},{'parentKey':'10000','value':'医疗/护理/美容/保健/卫生服务','key':'121400'},{'parentKey':'10000','value':'酒店/餐饮','key':'200600'},{'parentKey':'10000','value':'旅游/度假','key':'200800'},{'parentKey':'11300','value':'媒体/出版/影视/文化传播','key':'210300'},{'parentKey':'11300','value':'娱乐/体育/休闲','key':'200700'},{'parentKey':'11600','value':'能源/矿产/采掘/冶炼','key':'130000'},{'parentKey':'11600','value':'石油/石化/化工','key':'120500'},{'parentKey':'11600','value':'电气/电力/水利','key':'130100'},{'parentKey':'11600','value':'环保','key':'201200'},{'parentKey':'11100','value':'政府/公共事业/非盈利机构','key':'200100'},{'parentKey':'11100','value':'学术/科研','key':'120600'},{'parentKey':'11400','value':'农/林/牧/渔','key':'100000'},{'parentKey':'11400','value':'跨领域经营','key':'100100'},{'parentKey':'11400','value':'其他','key':'990000'}]},{'parentKey':'10100','value':'计算机软件','key':'160400'},{'parentKey':'10100','value':'IT服务(系统/数据/维护)','key':'160000'},{'parentKey':'10100','value':'电子技术/半导体/集成电路','key':'160500'},{'parentKey':'10100','value':'计算机硬件','key':'160200'},{'parentKey':'10100','value':'通信/电信/网络设备','key':'300100'},{'parentKey':'10100','value':'通信/电信运营、增值服务','key':'160100'},{'parentKey':'10100','value':'网络游戏','key':'160600'},{'parentKey':'10200','value':'基金/证券/期货/投资','key':'180000'},{'parentKey':'10200','value':'保险','key':'180100'},{'parentKey':'0','value':'IT|通信|电子|互联网','key':'10100'},{'parentKey':'10200','value':'银行','key':'300500'},{'parentKey':'0','value':'金融业','key':'10200'},{'parentKey':'10200','value':'信托/担保/拍卖/典当','key':'300900'},{'parentKey':'0','value':'房地产|建筑业','key':'10800'},{'parentKey':'10800','value':'房地产/建筑/建材/工程','key':'140000'},{'parentKey':'0','value':'商业服务','key':'10900'},{'parentKey':'10800','value':'家居/室内设计/装饰装潢','key':'140100'},{'parentKey':'0','value':'贸易|批发|零售|租赁业','key':'10300'},{'parentKey':'10800','value':'物业管理/商业中心','key':'140200'},{'parentKey':'0','value':'文体教育|工艺美术','key':'10400'},{'parentKey':'10900','value':'专业服务/咨询(财会/法律/人力资源等)','key':'200300'},{'parentKey':'0','value':'生产|加工|制造','key':'10500'},{'parentKey':'10900','value':'广告/会展/公关','key':'200302'},{'parentKey':'0','value':'交通|运输|物流|仓储','key':'11500'},{'parentKey':'10900','value':'中介服务','key':'201400'},{'parentKey':'0','value':'服务业','key':'10000'},{'parentKey':'10900','value':'检验/检测/认证','key':'201300'},{'parentKey':'0','value':'文化|传媒|娱乐|体育','key':'11300'},{'parentKey':'10900','value':'外包服务','key':'300300'},{'parentKey':'0','value':'能源|矿产|环保','key':'11600'},{'parentKey':'10300','value':'快速消费品（食品/饮料/烟酒/日化）','key':'120400'},{'parentKey':'0','value':'政府|非盈利机构','key':'11100'},{'parentKey':'10300','value':'耐用消费品（服饰/纺织/皮革/家具/家电）','key':'120200'},{'parentKey':'0','value':'农|林|牧|渔|其他','key':'11400'},{'parentKey':'10300','value':'贸易/进出口','key':'170500'},{'parentKey':'10300','value':'零售/批发','key':'170000'},{'parentKey':'10300','value':'租赁服务','key':'300700'},{'parentKey':'10400','value':'教育/培训/院校','key':'201100'},{'parentKey':'10400','value':'礼品/玩具/工艺美术/收藏品/奢侈品','key':'120800'},{'parentKey':'10500','value':'汽车/摩托车','key':'121000'},{'parentKey':'10500','value':'大型设备/机电设备/重工业','key':'129900'},{'parentKey':'10500','value':'加工制造（原料加工/模具）','key':'121100'},{'parentKey':'10500','value':'仪器仪表及工业自动化','key':'121200'},{'parentKey':'10500','value':'印刷/包装/造纸','key':'210600'},{'parentKey':'10500','value':'办公用品及设备','key':'120700'},{'parentKey':'10500','value':'医药/生物工程','key':'121300'},{'parentKey':'10500','value':'医疗设备/器械','key':'121500'},{'parentKey':'10500','value':'航空/航天研究与制造','key':'300000'},{'parentKey':'11500','value':'交通/运输','key':'150000'},{'parentKey':'11500','value':'物流/仓储','key':'301100'},{'parentKey':'10000','value':'医疗/护理/美容/保健/卫生服务','key':'121400'},{'parentKey':'10000','value':'酒店/餐饮','key':'200600'},{'parentKey':'10000','value':'旅游/度假','key':'200800'},{'parentKey':'11300','value':'媒体/出版/影视/文化传播','key':'210300'},{'parentKey':'11300','value':'娱乐/体育/休闲','key':'200700'},{'parentKey':'11600','value':'能源/矿产/采掘/冶炼','key':'130000'},{'parentKey':'11600','value':'石油/石化/化工','key':'120500'},{'parentKey':'11600','value':'电气/电力/水利','key':'130100'},{'parentKey':'11600','value':'环保','key':'201200'},{'parentKey':'11100','value':'政府/公共事业/非盈利机构','key':'200100'},{'parentKey':'11100','value':'学术/科研','key':'120600'},{'parentKey':'11400','value':'农/林/牧/渔','key':'100000'},{'parentKey':'11400','value':'跨领域经营','key':'100100'},{'parentKey':'11400','value':'其他','key':'990000'}]
    indentrys = [{
        'parentKey': '100000000',
        'value': '电子商务',
        'key': '100020000'
    }, {
        'parentKey': '100000000',
        'value': '计算机软件',
        'key': '100050000'
    }, {
        'parentKey': '100000000',
        'value': 'IT服务',
        'key': '100040000'
    }, {
        'parentKey': '100000000',
        'value': '电子/半导体/集成电路',
        'key': '100010000'
    }, {
        'parentKey': '100000000',
        'value': '计算机硬件',
        'key': '100060000'
    }, {
        'parentKey': '100000000',
        'value': '网络/信息安全',
        'key': '100100000'
    }, {
        'parentKey': '100000000',
        'value': '通信/网络设备',
        'key': '100090000'
    }, {
        'parentKey': '100000000',
        'value': '互联网',
        'key': '100030000'
    }, {
        'parentKey': '100000000',
        'value': '企业服务',
        'key': '100070000'
    }, {
        'parentKey': '100000000',
        'value': '人工智能',
        'key': '100080000'
    }, {
        'parentKey': '100000000',
        'value': '游戏',
        'key': '100120000'
    }, {
        'parentKey': '100000000',
        'value': '新媒体',
        'key': '100110000'
    }, {
        'parentKey': '100000000',
        'value': '云计算/大数据',
        'key': '100130000'
    }, {
        'parentKey': '100000000',
        'value': '运营商/增值服务',
        'key': '100140000'
    }, {
        'parentKey': '0',
        'value': '互联网/IT/电子/通信',
        'key': '100000000'
    }, {
        'parentKey': '0',
        'value': '房地产',
        'key': '200000000'
    }, {
        'parentKey': '200000000',
        'value': '房地产开发与经营',
        'key': '200010000'
    }, {
        'parentKey': '200000000',
        'value': '房地产中介',
        'key': '200020000'
    }, {
        'parentKey': '200000000',
        'value': '土地与公共设施管理',
        'key': '200040000'
    }, {
        'parentKey': '200000000',
        'value': '物业服务',
        'key': '200050000'
    }, {
        'parentKey': '0',
        'value': '金融业',
        'key': '300000000'
    }, {
        'parentKey': '300000000',
        'value': '保险业',
        'key': '300010000'
    }, {
        'parentKey': '300000000',
        'value': '典当',
        'key': '300020000'
    }, {
        'parentKey': '300000000',
        'value': '互联网金融/小额贷款',
        'key': '300030000'
    }, {
        'parentKey': '300000000',
        'value': '基金/风投',
        'key': '300040000'
    }, {
        'parentKey': '300000000',
        'value': '汽车金融服务',
        'key': '300050000'
    }, {
        'parentKey': '300000000',
        'value': '信托投资',
        'key': '300060000'
    }, {
        'parentKey': '300000000',
        'value': '银行',
        'key': '300070000'
    }, {
        'parentKey': '300000000',
        'value': '证券/期货',
        'key': '300080000'
    }, {
        'parentKey': '0',
        'value': '建筑业',
        'key': '400000000'
    }, {
        'parentKey': '400000000',
        'value': '房屋建筑/建筑设备安装',
        'key': '400010000'
    }, {
        'parentKey': '400000000',
        'value': '公共建筑装饰装修',
        'key': '400020000'
    }, {
        'parentKey': '400000000',
        'value': '土木工程建筑',
        'key': '400030000'
    }, {
        'parentKey': '400000000',
        'value': '住宅装饰装修',
        'key': '400040000'
    }, {
        'parentKey': '0',
        'value': '制造业',
        'key': '500000000'
    }, {
        'parentKey': '500000000',
        'value': '船舶/航空/航天/火车制造',
        'key': '500010000'
    }, {
        'parentKey': '500000000',
        'value': '电气机械/器材制造',
        'key': '500020000'
    },
        {
            'parentKey': '500000000',
            'value': '电子设备制造',
            'key': '500030000'
        },
        {
            'parentKey': '500000000',
            'value': '纺织业/服饰产品加工制造',
            'key': '500040000'
        },
        {
            'parentKey': '500000000',
            'value': '非金属矿物制品业',
            'key': '500050000'
        }, {
            'parentKey': '500000000',
            'value': '钢铁和有色金属冶炼及加工',
            'key': '500060000'
        },
        {
            'parentKey': '500000000',
            'value': '化学纤维制造业',
            'key': '500070000'
        },
        {
            'parentKey': '500000000',
            'value': '化学原料/化学制品',
            'key': '500080000'
        }, {
            'parentKey': '500000000',
            'value': '金属制品业',
            'key': '500090000'
        }, {
            'parentKey': '500000000',
            'value': '农副产品加工制造',
            'key': '500100000'
        }, {
            'parentKey': '500000000',
            'value': '汽车制造',
            'key': '500110000'
        }, {
            'parentKey': '500000000',
            'value': '燃料资源加工制造',
            'key': '500120000'
        }, {
            'parentKey': '500000000',
            'value': '日化产品制造',
            'key': '500130000'
        }, {
            'parentKey': '500000000',
            'value': '通用设备制造',
            'key': '500140000'
        }, {
            'parentKey': '500000000',
            'value': '橡胶和塑料制品',
            'key': '500150000'
        }, {
            'parentKey': '500000000',
            'value': '医药制造',
            'key': '500170000'
        }, {
            'parentKey': '500000000',
            'value': '仪器仪表制造',
            'key': '500180000'
        }, {
            'parentKey': '500000000',
            'value': '印刷/文体用品制造',
            'key': '500190000'
        }, {
            'parentKey': '500000000',
            'value': '造纸/家具制造',
            'key': '500200000'
        }, {
            'parentKey': '500000000',
            'value': '专用设备制造',
            'key': '500220000'
        }, {
            'parentKey': '500000000',
            'value': '医疗设备/器械',
            'key': '500210000'
        }, {
            'parentKey': '0',
            'value': '农林牧渔',
            'key': '600000000'
        }, {
            'parentKey': '600000000',
            'value': '农林牧渔',
            'key': '600010000'
        }, {
            'parentKey': '0',
            'value': '批发/零售/贸易',
            'key': '700000000'
        }, {
            'parentKey': '700000000',
            'value': '快速消费品',
            'key': '700010000'
        }, {
            'parentKey': '700000000',
            'value': '贸易/进出口代理/拍卖',
            'key': '700020000'
        }, {
            'parentKey': '700000000',
            'value': '耐用消费品',
            'key': '700030000'
        }, {
            'parentKey': '700000000',
            'value': '零售/批发',
            'key': '700040000'
        }, {
            'parentKey': '0',
            'value': '专业服务',
            'key': '800000000'
        }, {
            'parentKey': '800000000',
            'value': '财务/审计/税务',
            'key': '800010000'
        }, {
            'parentKey': '800000000',
            'value': '法律服务',
            'key': '800020000'
        }, {
            'parentKey': '800000000',
            'value': '工程技术与设计服务',
            'key': '800030000'
        }, {
            'parentKey': '800000000',
            'value': '广告业',
            'key': '800040000'
        }, {
            'parentKey': '800000000',
            'value': '会议/展览服务',
            'key': '800050000'
        }, {
            'parentKey': '800000000',
            'value': '检测/认证',
            'key': '800060000'
        }, {
            'parentKey': '800000000',
            'value': '景区/商业/市场等综合管理',
            'key': '800070000'
        }, {
            'parentKey': '800000000',
            'value': '人力资源服务',
            'key': '800080000'
        }, {
            'parentKey': '800000000',
            'value': '商业代理服务',
            'key': '800090000'
        }, {
            'parentKey': '800000000',
            'value': '专利/商标/知识产权',
            'key': '800100000'
        }, {
            'parentKey': '800000000',
            'value': '专业技术服务',
            'key': '800110000'
        }, {
            'parentKey': '800000000',
            'value': '咨询服务',
            'key': '800120000'
        }, {
            'parentKey': '800000000',
            'value': '租赁服务',
            'key': '800130000'
        }, {
            'parentKey': '0',
            'value': '文化/体育/娱乐',
            'key': '900000000'
        }, {
            'parentKey': '900000000',
            'value': '广播/电视/电影/录音制作',
            'key': '900010000'
        }, {
            'parentKey': '900000000',
            'value': '体育',
            'key': '900020000'
        }, {
            'parentKey': '900000000',
            'value': '文化艺术/娱乐',
            'key': '900030000'
        }, {
            'parentKey': '900000000',
            'value': '新闻/出版',
            'key': '900040000'
        }, {
            'parentKey': '0',
            'value': '交通运输/仓储/物流',
            'key': '1000000000'
        }, {
            'parentKey': '1000000000',
            'value': '火车站/港口/汽车站/路政',
            'key': '1000010000'
        }, {
            'parentKey': '1000000000',
            'value': '货运/物流仓储',
            'key': '1000020000'
        }, {
            'parentKey': '1000000000',
            'value': '民航/铁路/公路/水路客运',
            'key': '1000030000'
        }, {
            'parentKey': '1000000000',
            'value': '邮政/快递',
            'key': '1000040000'
        }, {
            'parentKey': '0',
            'value': '能源/环保/矿产',
            'key': '1100000000'
        }, {
            'parentKey': '1100000000',
            'value': '电力/水利/热力/燃气',
            'key': '1100010000'
        }, {
            'parentKey': '1100000000',
            'value': '环保',
            'key': '1100020000'
        }, {
            'parentKey': '1100000000',
            'value': '矿产/采掘',
            'key': '1100030000'
        }, {
            'parentKey': '1100000000',
            'value': '石油/石化',
            'key': '1100040000'
        }, {
            'parentKey': '1100000000',
            'value': '新能源',
            'key': '1100050000'
        }, {
            'parentKey': '0',
            'value': '教育培训/科研',
            'key': '1200000000'
        }, {
            'parentKey': '1200010000',
            'value': '科学技术推广服务业',
            'key': '1200000000'
        }, {
            'parentKey': '1200020000',
            'value': '培训/课外教育/教育辅助',
            'key': '1200000000'
        }, {
            'parentKey': '1200030000',
            'value': '学术/科研',
            'key': '1200000000'
        }, {
            'parentKey': '1200040000',
            'value': '学校教育',
            'key': '1200000000'
        }, {
            'parentKey': '0',
            'value': '卫生及社会工作',
            'key': '1300000000'
        }, {
            'parentKey': '1300000000',
            'value': '卫生服务',
            'key': '1300010000'
        }, {
            'parentKey': '1300000000',
            'value': '养老/孤儿/看护等社会服务',
            'key': '1300020000'
        }, {
            'parentKey': '1300000000',
            'value': '医院',
            'key': '1300030000'
        }, {
            'parentKey': '0',
            'value': '公共管理/社会保障',
            'key': '1400000000'
        }, {
            'parentKey': '1400000000',
            'value': '国家机构',
            'key': '1400010000'
        }, {
            'parentKey': '1400000000',
            'value': '社团/组织/社会保障',
            'key': '1400020000'
        }, {
            'parentKey': '0',
            'value': '生活服务',
            'key': '1500000000'
        }, {
            'parentKey': '1500000000',
            'value': '餐饮业',
            'key': '1500000000'
        }, {
            'parentKey': '1500000000',
            'value': '酒店/民宿',
            'key': '1500000000'
        }, {
            'parentKey': '1500000000',
            'value': '居民服务',
            'key': '1500000000'
        }, {
            'parentKey': '1500000000',
            'value': '旅游业',
            'key': '1500000000'
        }
    ]

    domains = {
        "100000000": "互联网/IT/电子/通信",
        "200000000": "房地产",
        "300000000": "金融业",
        "400000000": "建筑业",
        "500000000": "制造业",
        "600000000": "农林牧渔",
        "700000000": "批发/零售/贸易",
        "800000000": "专业服务",
        "900000000": "文化/体育/娱乐",
        "1000000000": "交通运输/仓储/物流",
        "1100000000": "能源/环保/矿产",
        "1200000000": "教育培训/科研",
        "1300000000": "卫生及社会工作",
        "1400000000": "公共管理/社会保障",
        "1500000000": "生活服务"
    }

    # re 区域
    areas = {
        "2945": "方山县", "2940": "汾阳市", "2949": "交城县", "2948": "交口县", "2947": "岚县", "2944": "临县",
        "2938": "离石区", "2946": "柳林县", "2950": "石楼县", "2941": "文水县", "2939": "孝义市", "2943": "兴县",
        "2942": "中阳县"
    }


    def __init__(self):
        self.connect = pymysql.Connect(host="192.168.1.214",port=3306,user="developer",passwd="123123",db="forwork_shanxi_ga",charset="utf8")
        self.cursor = self.connect.cursor()

    def openDriver(self):
        proxy = Proxy(
            {
                'proxyType': ProxyType.MANUAL,  # 用不用都行
                # '203.130.46.108:9090'
                # '117.127.0.202:8080'   00
                # '120.234.63.196:3128'  00
                'httpProxy': '39.106.223.134:80'
            }
        )
        # 新建一个“期望技能”，哈哈
        desired_capabilities = DesiredCapabilities.FIREFOX.copy()
        proxy.add_to_capabilities(desired_capabilities)
        self.driver = webdriver.Firefox(executable_path=self.firefoxPath,desired_capabilities=desired_capabilities)
        self.driver.maximize_window()
        self.driver.get(self.lvliang)
        # 手动登录时间
        # time.sleep(20)
        allhandles = self.driver.window_handles
        currenthandle = self.driver.current_window_handle
        if currenthandle != allhandles[-1]:
            self.driver.close()
            self.driver.switch_to.window(allhandles[-1])
        #################### 开始搜索 #######################
        print(self.areas.keys())
        for ide in self.indentrys:
            if ide.get("parentKey") != "0":
                print(ide)
                print("进入循环")
                self.key = ide.get("key")              # 小领域code
                self.keyword = ide.get("value")        # 小领域汉字
                self.parentCode = ide.get("parentKey") # 父领域
                # https://sou.zhaopin.com/?jl=736&in={}&sf=0&st=0
                self.driver.get(self.sou.format(self.key))
                print("开始搜素！")
                time.sleep(5)
                self.parseList()

    def parseList(self):
        try:
            WebDriverWait(self.driver,10).until(lambda x: x.find_element_by_class_name("search-box"))
        except Exception as e:
            time.sleep(2)
            print(e)

        try:
            contentDivLocated = (By.ID, "listContent")
            WebDriverWait(self.driver, timeout=6, poll_frequency=0.5).until(
                expected_conditions.presence_of_element_located(contentDivLocated))
        except Exception as e:
            print(e)
        try:
            contentDiv = self.driver.find_element_by_id("listContent")
            if None != contentDiv:
                postAs = contentDiv.find_elements_by_css_selector(".contentpile__content__wrapper__item.clearfix")
                # companyAs = contentDiv.find_elements_by_css_selector(
                #     ".contentpile__content__wrapper__item__info__box__cname__title.company_title")

                #
                if None != postAs:
                    for pa in postAs:
                        city = ""
                        area = ""
                        descDiv = pa.find_element_by_css_selector(".contentpile__content__wrapper__item__info__box__job__demand")
                        if None != descDiv:
                            deLis = descDiv.find_elements_by_tag_name("li")
                            if None != deLis:
                                areaText = deLis[0].text.strip()
                                if "-" in areaText:
                                    citiAres = areaText.split("-")
                                    if len(citiAres)==2:
                                        city = citiAres[0]
                                        area = citiAres[1]
                                else:
                                    city = areaText

                        ca = pa.find_element_by_css_selector(".contentpile__content__wrapper__item__info__box__cname__title.company_title")
                        href = ca.get_attribute("href")
                        if "company.zhaopin.com" not in href:
                            continue
                        else:
                            try:
                                self.rollBottom(pa)
                                ca.click()
                            except Exception as e:
                                self.rollTop(pa)
                                ca.click()

                            try:
                                WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,"mian-company")))
                            except Exception as e:
                                print(e)
                            # 将窗口转到企业详情页
                            self.switchSearchListToDetail()

                            self.parseEntp(city,area)
                            time.sleep(2)

                try:
                    nextBtn = self.driver.find_element_by_css_selector(".btn.soupager__btn")
                    if nextBtn.is_enabled():
                        nextBtn.click()
                    else:
                        print("结束了！！！")
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    # 解析企业详情页
    def parseEntp(self,city,area):
        entpName = ""
        entpType = ""
        personScope = ""
        industry = ""
        website = ""
        address = ""
        highlight = ""
        content = ""
        url = ""
        entpId = None
        entpUi = ""
        domain = self.keyword.decode("utf-8")
        currentUrl = str(self.driver.current_url)
        url  = currentUrl
        # https://company.zhaopin.com/CZ000163970.htm
        entpUrl = currentUrl.split("/")[-1]
        entpUi = entpUrl.split(".")[0]
        soup = BeautifulSoup(self.driver.page_source,"html.parser")
        entpItem = {}
        try:
            overviewTitleDiv = self.driver.find_element_by_class_name("overview__title")
            if None != overviewTitleDiv:
                h1Div = overviewTitleDiv.find_element_by_tag_name("h1")
                if None != h1Div:
                    entpName = h1Div.text.strip()

        except Exception as e:
            print("企业名称获取出错")
            print(e)
        try:
            detailDiv = soup.find("div",{"class":"overview__detail clearfix"})
            if None != detailDiv:
                spans = detailDiv.findAll("span")
                if spans != None:
                    entpType = spans[0].getText()
                sizeDiv = detailDiv.find("div",{"class":"overview__detail-size"})
                if None != sizeDiv:
                    personScope = sizeDiv.getText().strip()

                industryDiv = detailDiv.find("div", {"class": "overview__detail-industry"})
                if None != industryDiv:
                    industry = industryDiv.getText().strip()

        except Exception as e:
            print("企业基本信息获取出错")
            print(e)

        try:
            urlDiv = soup.find("p",{"class":"overview__url"})
            if None != urlDiv:
                website = urlDiv.getText().strip()
        except Exception as e:
            print("企业主页网址获取不到")
            print(e)

        try:
            welfareUl = soup.find("p",{"class":"overview__welfare clearfix"})
            if None != welfareUl:
                wlis = welfareUl.findAll("li")
                if None != wlis:
                    for li in wlis:
                        highlight +=","+li.getText().strip()
                highlight = highlight[1:]
        except Exception as e:
            print("企业亮点获取不到")
            print(e)

        try:
            showAllBtn = self.driver.find_element_by_class_name(u"company-show__content__btn")
            if None != showAllBtn:
                showAllBtn.click()
        except Exception as e:
            print("没有全部显示按钮")
            print(e)

        try:
            contentDiv = soup.find("div",{"class":"company-show__content"})
            if None != contentDiv:
                content = contentDiv.getText().strip()
        except Exception as e:
            contentDiv = soup.find("div",{"class":"company-show__content__description"})
            if None != contentDiv:
                content = contentDiv.getText().strip()
            print(e.message)
        else:
            print("企业详细介绍 没有报错")

        try:
            addressDiv = self.driver.find_element_by_class_name("map-box__adress")
            if None != addressDiv:
                address = addressDiv.text.strip()
        except Exception as e:
            print("企业地址获取不到")
            print(e)

        # 判断数据库中是否已经有该企业信息
        items = self.existEntpFromDB(entpName)
        if None != items:
            entpId = items[0]
            # 如果有对应的企业信息，对比详情、城市、地区、人员规模;将对应的职位信息删除再入库新的职位
            # id,entp_info,city,area,person_scope
            if None==content or ""==content:
                content = "" if items[1]==None else items[1]
            if None==city or ""==city:
                city = "" if items[2]==None else items[2]
            if None==area or ""==area:
                area = "" if items[3]==None else items[3]
            if None==personScope or ""==personScope:
                personScope = "" if items[4]==None else items[4]
            entpItem.update({"id": entpId})
            entpItem.update({"city": city})
            entpItem.update({"area": area})
            entpItem.update({"content": content})
            entpItem.update({"highlight": highlight})
            entpItem.update({"personScope": personScope})
            self.updateEntp(entpItem)
            self.deleteEntpPostByEntpId(entpId)

        # 如果没有对应的企业信息，企业信息与职位信息都要入库
        else:
            entpItem.update({"entpName":entpName})
            entpItem.update({"url":url})
            entpItem.update({"entpType":entpType})
            entpItem.update({"entpUi":entpUi})
            entpItem.update({"personScope":personScope})
            entpItem.update({"industry":industry})
            entpItem.update({"website":website})
            entpItem.update({"address":address})
            entpItem.update({"highlight":highlight})
            entpItem.update({"content":content})
            entpItem.update({"domain":domain})
            entpItem.update({"city":city})
            entpItem.update({"area":area})
            try:
                self.saveEntp(entpItem)
                etms = self.existEntpFromDB(entpName)
                if etms != None:
                    entpId = etms[0]
            except Exception as e:
                print(e)
        # 底部更多职位按钮
        moreBtn = None
        try:
            moreBtn = self.driver.find_element_by_css_selector(".more-job-btn.mian-company__left-container__more-job-but")
        except Exception as e:
            print(e)
        # 不为空,点击更多职位进入职位列表
        if None != moreBtn:
            self.rollBottom(moreBtn)
            moreBtn.click()
            time.sleep(2)
            self.driver.implicitly_wait(10)
            # 句柄从企业详情页跳转到需求列表页
            self.switchEntpDetailToPostList()
            # 解析职位列表
            self.parsePostList(entpUi,entpId)
        else:
            print("没有找到更多职位按钮！")

    # 解析职位列表
    def parsePostList(self,entpUi,entpId):
        try:
            WebDriverWait(driver=self.driver,timeout=20,poll_frequency=0.5).until(expected_conditions.presence_of_element_located((By.ID,"listContent")))
        except Exception as e:
            print(e)

        listContent = self.driver.find_element_by_id("listContent")
        if None != listContent:
            postItems = listContent.find_elements_by_class_name("contentpile__content__wrapper__item__info")
            if None != postItems:
                for it in postItems:
                    try:
                        self.rollBottom(it)
                        jobNameSpan = it.find_element_by_class_name("contentpile__content__wrapper__item__info__box__jobname__title")
                        jobNameSpan.click()
                    except ElementClickInterceptedException as e:
                        self.rollTop(it)
                        jobNameSpan = it.find_element_by_class_name(
                            "contentpile__content__wrapper__item__info__box__jobname__title")
                        jobNameSpan.click()
                    else:
                        self.rollDeep(it)
                        jobNameSpan = it.find_element_by_class_name(
                            "contentpile__content__wrapper__item__info__box__jobname__title")
                        jobNameSpan.click()

                    time.sleep(random.randint(3,4))
                    # 将句柄转到职位详情页
                    self.switchPostListToPostDetail()
                    # 解析职位详情
                    self.parsePostDetail(entpUi,entpId)
                    # 将句柄从职位详情页转到职位列表页
                    self.switchPostDetailToPostList()

            # 有下一页点击下一页，如果没有就跳转到搜索页面
            try:
                nextBtn = self.driver.find_element_by_css_selector(".btn.soupager__btn")
                if nextBtn.is_enabled():
                    try:
                        self.rollBottom(nextBtn)
                        nextBtn.click()
                        self.parsePostList()
                    except Exception as e:
                        self.rollTop(nextBtn)
                        nextBtn.click()
                        self.parsePostList()
                else:
                    self.switchPostListToSearchList()
            except Exception as e:
                self.switchPostListToSearchList()
                print(e)

    # 解析职位详情
    def parsePostDetail(self,entpUi,entpId):
        postItem={}
        postName = ""
        salary = ""
        city = ""
        workExp = ""
        education = ""
        postNum = ""
        postHighlights = ""
        postDesc = ""
        address = ""
        area = ""
        # 先看有没有“注册指南”广告，关闭
        try:
            registerCloseBtn = self.driver.find_element_by_class_name("register-guide__close")
            if registerCloseBtn != None:
                registerCloseBtn.click()
        except Exception as e:
            print("注册指南没有找到！")
            print(e)

        try:
            postNameH3 = self.driver.find_element_by_class_name("summary-plane__title")
            if None != postNameH3:
                postName = postNameH3.text.strip()
        except Exception as e:
            print(e)

        try:
            replaceTimeSpan = self.driver.find_element_by_class_name("summary-plane__time")
            if None != replaceTimeSpan:
                # replaceTime 更新于  10:14 ; 更新于  7月11日
                replaceTmp = replaceTimeSpan.text.strip()
                replaceTmp = replaceTmp.replace("更新于","").strip()
                replaceTime = self.gotPostPlaneTime(replaceTmp)
        except Exception as e:
            print(e)

        try:
            salaryDiv = self.driver.find_element_by_class_name("summary-plane__salary")
            if None != salaryDiv:
                salary = salaryDiv.text.strip()
        except Exception as e:
            print(e)

        try:
            planUl = self.driver.find_element_by_class_name("summary-plane__info")
            if None != planUl:
                lis = planUl.find_elements_by_tag_name("li")
                if len(lis) == 4:
                    try:
                        cityDiv = lis[0].find_element_by_tag_name("a")
                        if None != cityDiv:
                            city = cityDiv.text.strip()
                    except Exception as e:
                        print(e)

                    try:
                        areaDiv = lis[0].find_element_by_tag_name("span")
                        if None != areaDiv:
                            area = areaDiv.text.strip()
                    except Exception as e:
                        print(e)

                    workExp = lis[1].text.strip()
                    education = lis[2].text.strip()
                    postNum = lis[3].text.strip().replace("招","").replace("人","")
            else:
                print("不晓得发生了什么")
        except Exception as e:
            print(e)

        try:
            highlightsDiv = self.driver.find_element_by_class_name("highlights__content")
            if None != highlightsDiv:
                highSpans = highlightsDiv.find_elements_by_tag_name("span")
                if None != highSpans:
                    for hp in highSpans:
                        postHighlights += (","+hp.text.strip())
        except Exception as e:
            print(e)

        try:
            describtionDiv = self.driver.find_element_by_class_name("describtion__detail-content")
            if None != describtionDiv:
                postDesc = describtionDiv.text
        except Exception as e:
            print(e)

        try:
            addresDiv = self.driver.find_element_by_class_name("job-address__content-text")
            if None != addresDiv:
                address = addresDiv.text.strip()
        except Exception as e:
            print(e)
        # if area == "" or area == None:
        #     area = self.areas.get(self.areaCode)
        postItem.update({"entpId": entpId})
        postItem.update({"postName": postName})
        postItem.update({"salary": salary})
        postItem.update({"entpUi": entpUi})
        postItem.update({"city": city})
        postItem.update({"workExp": workExp})
        postItem.update({"education": education})
        postItem.update({"postNum": postNum})
        postItem.update({"postHighlights": postHighlights[1:]})
        postItem.update({"postDesc": postDesc})
        postItem.update({"address": address})
        postItem.update({"area": area})
        postItem.update({"replaceTime": replaceTime})
        # 将职位保存到数据库
        try:
            self.savePost(postItem)
        except Exception as e:
            print(e)

    # 1.如果为true，元素的顶端将和其所在滚动区的可视区域的顶端对齐。
    def rollTop(self,target):
        print("滑动到窗口顶部")
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", target)
        except Exception as e:
            print(e)

    # 2.如果为false，元素的底端将和其所在滚动区的可视区域的底端对齐。
    def rollBottom(self,target):
        print("滑动到窗口底部")
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(false);", target)
        except Exception as e:
            print(e)
    # 3.滑动到顶
    def rollHead(self,target):
        try:
            self.driver.execute_script("arguments[0].scrollTo(0,1);",target)
        except Exception as e:
            print(e)

    # 4.滑动到底
    def rollDeep(self,target):
        try:
            self.driver.execute_script("arguments[0].scrollTo(0,10000);",target)
        except Exception as e:
            print(e)

    # 将句柄从列表页转向企业详情页
    def switchSearchListToDetail(self):
        print("将句柄从列表页转向企业详情页")
        allHandles = self.driver.window_handles
        if len(allHandles) == 2:
            self.driver.switch_to.window(allHandles[-1])
        # 将多余的窗口关闭
        elif len(allHandles)>2:
            for hd in allHandles:
                if hd != allHandles[0] and hd != allHandles[-1]:
                    self.driver.switch_to.window(hd)
                    self.driver.close()
            # 将窗口转换到最后一个窗口
            self.driver.switch_to.window(allHandles[-1])

    # 将句柄从企业详情页转换到搜索列表页
    def switchEntpDetailToSearchList(self):
        print("将句柄从企业详情页转换到搜索列表页")
        allHandles = self.driver.window_handles
        currentHandles = self.driver.current_window_handle
        if len(allHandles) == 2:
            if currentHandles == allHandles[1]:
                self.driver.close()
                self.driver.switch_to.window(allHandles[0])
        # 将多余的窗口关闭
        elif len(allHandles) > 2:
            for hd in allHandles:
                if hd != allHandles[0]:
                    self.driver.switch_to.window(hd)
                    self.driver.close()
            # 将窗口转换到最后一个窗口
            self.driver.switch_to.window(allHandles[0])

    # 将句柄从企业的详情页面转到需求列表
    def switchEntpDetailToPostList(self):
        print("将句柄从企业的详情页面转到需求列表")
        allhandles = self.driver.window_handles
        currentHandles  = self.driver.current_window_handle
        #判断是否有3个窗口
        if len(allhandles) == 3:
            #判断是否是企业详情页，并且关闭详情页==》跳转到职位列表页
            if currentHandles == allhandles[1]:
                self.driver.close()
                self.driver.switch_to.window(allhandles[-1])
            #如果当前页不是详情页，先转到详情页，将其关闭==》跳转到职位列表页
            else:
                self.driver.switch_to.window(allhandles[1])
                self.driver.close()
                self.driver.switch_to.window(allhandles[-1])
        # 如果大于3个窗口，就将除第一个和最后一个以外的窗口全部关闭
        elif len(allhandles) > 3:
            for hd in allhandles:
                if hd != allhandles[0] and hd != allhandles[-1]:
                    self.driver.switch_to.window(hd)
                    self.driver.close()
            # 将窗口转换到最后一个窗口
            self.driver.switch_to.window(allhandles[-1])
        else:
            print("将句柄从企业的详情页面转到需求列表  窗口不对")

    # 将句柄从职位列表转到职位详情页
    def switchPostListToPostDetail(self):
        print("将句柄从职位列表转到职位详情页")
        allhandles = self.driver.window_handles
        currentHandles = self.driver.current_window_handle
        # 判断是否有3个窗口
        if len(allhandles) == 3:
            # 判断是否是职位列表页，跳转到职位详情页
            self.driver.switch_to.window(allhandles[2])
        # 如果大于3个窗口，就将除第一个、第二个和最后一个以外的窗口全部关闭
        elif len(allhandles) > 3:
            for hd in allhandles:
                if hd != allhandles[0] and hd != allhandles[1] and hd != allhandles[-1]:
                    self.driver.switch_to.window(hd)
                    self.driver.close()
            # 将窗口转换到最后一个窗口（职位详情页）
            self.driver.switch_to.window(allhandles[-1])
        else:
            print("将句柄从职位列表转到职位详情页  窗口不对")

    # 将句柄从职位列表页跳转到搜索列表页
    def switchPostListToSearchList(self):
        print("将句柄从职位列表页跳转到搜索列表页")
        allhandles = self.driver.window_handles
        for hd in allhandles:
            if hd != allhandles[0]:
                self.driver.switch_to.window(hd)
                self.driver.close()
        self.driver.switch_to.window(allhandles[0])

    # 将句柄从职位详情页转到职位列表页
    def switchPostDetailToPostList(self):
        print("将句柄从职位详情页转到职位列表页")
        allhandles = self.driver.window_handles
        currenthandles = self.driver.current_window_handle
        if len(allhandles) == 3:
            if currenthandles != allhandles[2]:
                self.driver.switch_to.window(allhandles[2])
            self.driver.close()
            self.driver.switch_to.window(allhandles[1])
        else:
            print("将句柄从职位详情页转到职位列表页  窗口有错")
            print(currenthandles)
            print(allhandles)

    # 获取职位更新时间
    def gotPostPlaneTime(self,replaceTmp):
        try:
            if "月" in replaceTmp:
                timeDs = replaceTmp.split("月")
                month = timeDs[0].strip()
                date = timeDs[1].split("日")[0].strip()
                year = str(time.localtime().tm_year)
                timeStr = year + "-" + month + "-" + date + " 8:20"
                print(timeStr)
            else:
                year = str(time.localtime().tm_year)
                month = str(time.localtime().tm_mon)
                date = str(time.localtime().tm_mday)
                timeDs = replaceTmp.split(":")
                hours = timeDs[0]
                minute = timeDs[1]
                timeStr = year + "-" + month + "-" + date + " " + hours + ":" + minute
                print(timeStr)
            timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M")
            replaceTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
        except Exception as e:
            replaceTime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            print("生成职位修改时间报错啦！ ",e)
        finally:
            return replaceTime

    # 企业信息存入数据库
    def saveEntp(self,entpItem):
        now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        sqlStr = """
        INSERT INTO `forwork_shanxi_ga`.`zhilian_entp`
        (`entp_name`, `url`,`website`, `address`, `entp_info`, `entp_type`,`entp_ui`, 
        `highlight`, `industry`,  `person_scope`, `domain`, `record_status`, 
        `city`, `area`, `create_time`, `update_time`) 
        VALUES (%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s)
        """
        try:
            self.cursor.execute(sqlStr,(
                entpItem['entpName'],entpItem['url'],entpItem['website'],entpItem['address'],entpItem['content'],entpItem['entpType'],entpItem['entpUi'],
                entpItem['highlight'],entpItem['industry'],entpItem['personScope'],entpItem['domain'],'0',
                entpItem['city'],entpItem['area'],now,now
            ))
            self.connect.commit()
        except Exception as e:
            print(e)

    # 企业职位存入数据库
    def savePost(self, postItem):
        print(postItem)
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sqlStr = """
            INSERT INTO `forwork_shanxi_ga`.`zhilian_entp_post`
            (`entp_id`, `post_name`, `salary`, `area`, `city`, `work_exp`, `entp_ui`, 
            `education`, `post_num`, `post_highlights`, `post_desc`,`replace_time`,
            `address`,`record_status`,`create_time`, `update_time`) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(sqlStr, (
                postItem['entpId'],postItem['postName'],postItem['salary'],postItem['area'],postItem['city'],postItem['workExp'],postItem['entpUi'],
                postItem['education'],postItem['postNum'],postItem['postHighlights'],postItem['postDesc'],postItem['replaceTime'],
                postItem['address'],'0',now,now
            ))
            self.connect.commit()
        except Exception as e:
            print(e)

    # 通过企业名称查询数据库
    def existEntpFromDB(self,entpName):
        searchSql = ("SELECT id,entp_info,city,area,person_scope FROM `forwork_shanxi_ga`.zhilian_entp where entp_name ='"+entpName.encode('utf-8')+"'")
        items = None
        try:
            # 执行SQL语句
            self.cursor.execute(searchSql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            if len(results) >0:
                items = results[0]
        except Exception as e:
            print(e)
        finally:
            print("数据库验证结果："+str(items))
            return items

    def updateEntp(self,items):
        searchSql = ("UPDATE `forwork_shanxi_ga`.zhipin_entp SET entp_info = %s,city = %s,area=%s,person_scope = %s,highlight = %s where id = %s")

        try:
            self.cursor.execute(searchSql,(
                items['content'],
                items['city'],
                items['area'],
                items['personScope'],
                items['highlight'],
                items['id']
            ))
            self.connect.commit()
        except Exception as e:
            print(e)

    # 根据企业id删除职位
    def deleteEntpPostByEntpId(self,entpId):
        try:
            self.cursor.execute("DELETE FROM `forwork_shanxi_ga`.zhilian_entp_post WHERE id = "+entpId)
            self.connect.commit()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    spider = ZhilianSpider()
    spider.openDriver()
    spider.connect.close()
    spider.driver.quit()
