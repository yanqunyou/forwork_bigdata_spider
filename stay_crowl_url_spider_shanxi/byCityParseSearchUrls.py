# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         byCityParseSearchUrls
# Description:  智联招聘---这是根据特定的城市，生成职位搜索URL
# Author:       forwork
# Date:         2019/7/18
#-------------------------------------------------------------------------------
import hashlib
import random
import time
import pymysql
import logging
import requests
import json
import uuid


class ByCityParseSearchUrls(object):
    # 领域
    # indentrys= [{'parentKey':'10100','value':'互联网/电子商务','key':'210500'[{'parentKey':'10100','value':'互联网/电子商务','key':'210500'},{'parentKey':'10100','value':'计算机软件','key':'160400'},{'parentKey':'10100','value':'IT服务(系统/数据/维护)','key':'160000'},{'parentKey':'10100','value':'电子技术/半导体/集成电路','key':'160500'},{'parentKey':'10100','value':'计算机硬件','key':'160200'},{'parentKey':'10100','value':'通信/电信/网络设备','key':'300100'},{'parentKey':'10100','value':'通信/电信运营、增值服务','key':'160100'},{'parentKey':'10100','value':'网络游戏','key':'160600'},{'parentKey':'10200','value':'基金/证券/期货/投资','key':'180000'},{'parentKey':'10200','value':'保险','key':'180100'},{'parentKey':'0','value':'IT|通信|电子|互联网','key':'10100'},{'parentKey':'10200','value':'银行','key':'300500'},{'parentKey':'0','value':'金融业','key':'10200'},{'parentKey':'10200','value':'信托/担保/拍卖/典当','key':'300900'},{'parentKey':'0','value':'房地产|建筑业','key':'10800'},{'parentKey':'10800','value':'房地产/建筑/建材/工程','key':'140000'},{'parentKey':'0','value':'商业服务','key':'10900'},{'parentKey':'10800','value':'家居/室内设计/装饰装潢','key':'140100'},{'parentKey':'0','value':'贸易|批发|零售|租赁业','key':'10300'},{'parentKey':'10800','value':'物业管理/商业中心','key':'140200'},{'parentKey':'0','value':'文体教育|工艺美术','key':'10400'},{'parentKey':'10900','value':'专业服务/咨询(财会/法律/人力资源等)','key':'200300'},{'parentKey':'0','value':'生产|加工|制造','key':'10500'},{'parentKey':'10900','value':'广告/会展/公关','key':'200302'},{'parentKey':'0','value':'交通|运输|物流|仓储','key':'11500'},{'parentKey':'10900','value':'中介服务','key':'201400'},{'parentKey':'0','value':'服务业','key':'10000'},{'parentKey':'10900','value':'检验/检测/认证','key':'201300'},{'parentKey':'0','value':'文化|传媒|娱乐|体育','key':'11300'},{'parentKey':'10900','value':'外包服务','key':'300300'},{'parentKey':'0','value':'能源|矿产|环保','key':'11600'},{'parentKey':'10300','value':'快速消费品（食品/饮料/烟酒/日化）','key':'120400'},{'parentKey':'0','value':'政府|非盈利机构','key':'11100'},{'parentKey':'10300','value':'耐用消费品（服饰/纺织/皮革/家具/家电）','key':'120200'},{'parentKey':'0','value':'农|林|牧|渔|其他','key':'11400'},{'parentKey':'10300','value':'贸易/进出口','key':'170500'},{'parentKey':'10300','value':'零售/批发','key':'170000'},{'parentKey':'10300','value':'租赁服务','key':'300700'},{'parentKey':'10400','value':'教育/培训/院校','key':'201100'},{'parentKey':'10400','value':'礼品/玩具/工艺美术/收藏品/奢侈品','key':'120800'},{'parentKey':'10500','value':'汽车/摩托车','key':'121000'},{'parentKey':'10500','value':'大型设备/机电设备/重工业','key':'129900'},{'parentKey':'10500','value':'加工制造（原料加工/模具）','key':'121100'},{'parentKey':'10500','value':'仪器仪表及工业自动化','key':'121200'},{'parentKey':'10500','value':'印刷/包装/造纸','key':'210600'},{'parentKey':'10500','value':'办公用品及设备','key':'120700'},{'parentKey':'10500','value':'医药/生物工程','key':'121300'},{'parentKey':'10500','value':'医疗设备/器械','key':'121500'},{'parentKey':'10500','value':'航空/航天研究与制造','key':'300000'},{'parentKey':'11500','value':'交通/运输','key':'150000'},{'parentKey':'11500','value':'物流/仓储','key':'301100'},{'parentKey':'10000','value':'医疗/护理/美容/保健/卫生服务','key':'121400'},{'parentKey':'10000','value':'酒店/餐饮','key':'200600'},{'parentKey':'10000','value':'旅游/度假','key':'200800'},{'parentKey':'11300','value':'媒体/出版/影视/文化传播','key':'210300'},{'parentKey':'11300','value':'娱乐/体育/休闲','key':'200700'},{'parentKey':'11600','value':'能源/矿产/采掘/冶炼','key':'130000'},{'parentKey':'11600','value':'石油/石化/化工','key':'120500'},{'parentKey':'11600','value':'电气/电力/水利','key':'130100'},{'parentKey':'11600','value':'环保','key':'201200'},{'parentKey':'11100','value':'政府/公共事业/非盈利机构','key':'200100'},{'parentKey':'11100','value':'学术/科研','key':'120600'},{'parentKey':'11400','value':'农/林/牧/渔','key':'100000'},{'parentKey':'11400','value':'跨领域经营','key':'100100'},{'parentKey':'11400','value':'其他','key':'990000'}]},{'parentKey':'10100','value':'计算机软件','key':'160400'},{'parentKey':'10100','value':'IT服务(系统/数据/维护)','key':'160000'},{'parentKey':'10100','value':'电子技术/半导体/集成电路','key':'160500'},{'parentKey':'10100','value':'计算机硬件','key':'160200'},{'parentKey':'10100','value':'通信/电信/网络设备','key':'300100'},{'parentKey':'10100','value':'通信/电信运营、增值服务','key':'160100'},{'parentKey':'10100','value':'网络游戏','key':'160600'},{'parentKey':'10200','value':'基金/证券/期货/投资','key':'180000'},{'parentKey':'10200','value':'保险','key':'180100'},{'parentKey':'0','value':'IT|通信|电子|互联网','key':'10100'},{'parentKey':'10200','value':'银行','key':'300500'},{'parentKey':'0','value':'金融业','key':'10200'},{'parentKey':'10200','value':'信托/担保/拍卖/典当','key':'300900'},{'parentKey':'0','value':'房地产|建筑业','key':'10800'},{'parentKey':'10800','value':'房地产/建筑/建材/工程','key':'140000'},{'parentKey':'0','value':'商业服务','key':'10900'},{'parentKey':'10800','value':'家居/室内设计/装饰装潢','key':'140100'},{'parentKey':'0','value':'贸易|批发|零售|租赁业','key':'10300'},{'parentKey':'10800','value':'物业管理/商业中心','key':'140200'},{'parentKey':'0','value':'文体教育|工艺美术','key':'10400'},{'parentKey':'10900','value':'专业服务/咨询(财会/法律/人力资源等)','key':'200300'},{'parentKey':'0','value':'生产|加工|制造','key':'10500'},{'parentKey':'10900','value':'广告/会展/公关','key':'200302'},{'parentKey':'0','value':'交通|运输|物流|仓储','key':'11500'},{'parentKey':'10900','value':'中介服务','key':'201400'},{'parentKey':'0','value':'服务业','key':'10000'},{'parentKey':'10900','value':'检验/检测/认证','key':'201300'},{'parentKey':'0','value':'文化|传媒|娱乐|体育','key':'11300'},{'parentKey':'10900','value':'外包服务','key':'300300'},{'parentKey':'0','value':'能源|矿产|环保','key':'11600'},{'parentKey':'10300','value':'快速消费品（食品/饮料/烟酒/日化）','key':'120400'},{'parentKey':'0','value':'政府|非盈利机构','key':'11100'},{'parentKey':'10300','value':'耐用消费品（服饰/纺织/皮革/家具/家电）','key':'120200'},{'parentKey':'0','value':'农|林|牧|渔|其他','key':'11400'},{'parentKey':'10300','value':'贸易/进出口','key':'170500'},{'parentKey':'10300','value':'零售/批发','key':'170000'},{'parentKey':'10300','value':'租赁服务','key':'300700'},{'parentKey':'10400','value':'教育/培训/院校','key':'201100'},{'parentKey':'10400','value':'礼品/玩具/工艺美术/收藏品/奢侈品','key':'120800'},{'parentKey':'10500','value':'汽车/摩托车','key':'121000'},{'parentKey':'10500','value':'大型设备/机电设备/重工业','key':'129900'},{'parentKey':'10500','value':'加工制造（原料加工/模具）','key':'121100'},{'parentKey':'10500','value':'仪器仪表及工业自动化','key':'121200'},{'parentKey':'10500','value':'印刷/包装/造纸','key':'210600'},{'parentKey':'10500','value':'办公用品及设备','key':'120700'},{'parentKey':'10500','value':'医药/生物工程','key':'121300'},{'parentKey':'10500','value':'医疗设备/器械','key':'121500'},{'parentKey':'10500','value':'航空/航天研究与制造','key':'300000'},{'parentKey':'11500','value':'交通/运输','key':'150000'},{'parentKey':'11500','value':'物流/仓储','key':'301100'},{'parentKey':'10000','value':'医疗/护理/美容/保健/卫生服务','key':'121400'},{'parentKey':'10000','value':'酒店/餐饮','key':'200600'},{'parentKey':'10000','value':'旅游/度假','key':'200800'},{'parentKey':'11300','value':'媒体/出版/影视/文化传播','key':'210300'},{'parentKey':'11300','value':'娱乐/体育/休闲','key':'200700'},{'parentKey':'11600','value':'能源/矿产/采掘/冶炼','key':'130000'},{'parentKey':'11600','value':'石油/石化/化工','key':'120500'},{'parentKey':'11600','value':'电气/电力/水利','key':'130100'},{'parentKey':'11600','value':'环保','key':'201200'},{'parentKey':'11100','value':'政府/公共事业/非盈利机构','key':'200100'},{'parentKey':'11100','value':'学术/科研','key':'120600'},{'parentKey':'11400','value':'农/林/牧/渔','key':'100000'},{'parentKey':'11400','value':'跨领域经营','key':'100100'},{'parentKey':'11400','value':'其他','key':'990000'}]
    indentrys = [{'parentKey': '10100', 'value': '互联网/电子商务', 'key': '210500'},
                 {'parentKey': '10100', 'value': '计算机软件', 'key': '160400'},
                 {'parentKey': '10100', 'value': 'IT服务(系统/数据/维护)', 'key': '160000'},
                 {'parentKey': '10100', 'value': '电子技术/半导体/集成电路', 'key': '160500'},
                 {'parentKey': '10100', 'value': '计算机硬件', 'key': '160200'},
                 {'parentKey': '10100', 'value': '通信/电信/网络设备', 'key': '300100'},
                 {'parentKey': '10100', 'value': '通信/电信运营、增值服务', 'key': '160100'},
                 {'parentKey': '10100', 'value': '网络游戏', 'key': '160600'},
                 {'parentKey': '10200', 'value': '基金/证券/期货/投资', 'key': '180000'},
                 {'parentKey': '10200', 'value': '保险', 'key': '180100'},
                 {'parentKey': '0', 'value': 'IT|通信|电子|互联网', 'key': '10100'},
                 {'parentKey': '10200', 'value': '银行', 'key': '300500'},
                 {'parentKey': '0', 'value': '金融业', 'key': '10200'},
                 {'parentKey': '10200', 'value': '信托/担保/拍卖/典当', 'key': '300900'},
                 {'parentKey': '0', 'value': '房地产|建筑业', 'key': '10800'},
                 {'parentKey': '10800', 'value': '房地产/建筑/建材/工程', 'key': '140000'},
                 {'parentKey': '0', 'value': '商业服务', 'key': '10900'},
                 {'parentKey': '10800', 'value': '家居/室内设计/装饰装潢', 'key': '140100'},
                 {'parentKey': '0', 'value': '贸易|批发|零售|租赁业', 'key': '10300'},
                 {'parentKey': '10800', 'value': '物业管理/商业中心', 'key': '140200'},
                 {'parentKey': '0', 'value': '文体教育|工艺美术', 'key': '10400'},
                 {'parentKey': '10900', 'value': '专业服务/咨询(财会/法律/人力资源等)', 'key': '200300'},
                 {'parentKey': '0', 'value': '生产|加工|制造', 'key': '10500'},
                 {'parentKey': '10900', 'value': '广告/会展/公关', 'key': '200302'},
                 {'parentKey': '0', 'value': '交通|运输|物流|仓储', 'key': '11500'},
                 {'parentKey': '10900', 'value': '中介服务', 'key': '201400'},
                 {'parentKey': '0', 'value': '服务业', 'key': '10000'},
                 {'parentKey': '10900', 'value': '检验/检测/认证', 'key': '201300'},
                 {'parentKey': '0', 'value': '文化|传媒|娱乐|体育', 'key': '11300'},
                 {'parentKey': '10900', 'value': '外包服务', 'key': '300300'},
                 {'parentKey': '0', 'value': '能源|矿产|环保', 'key': '11600'},
                 {'parentKey': '10300', 'value': '快速消费品（食品/饮料/烟酒/日化）', 'key': '120400'},
                 {'parentKey': '0', 'value': '政府|非盈利机构', 'key': '11100'},
                 {'parentKey': '10300', 'value': '耐用消费品（服饰/纺织/皮革/家具/家电）', 'key': '120200'},
                 {'parentKey': '0', 'value': '农|林|牧|渔|其他', 'key': '11400'},
                 {'parentKey': '10300', 'value': '贸易/进出口', 'key': '170500'},
                 {'parentKey': '10300', 'value': '零售/批发', 'key': '170000'},
                 {'parentKey': '10300', 'value': '租赁服务', 'key': '300700'},
                 {'parentKey': '10400', 'value': '教育/培训/院校', 'key': '201100'},
                 {'parentKey': '10400', 'value': '礼品/玩具/工艺美术/收藏品/奢侈品', 'key': '120800'},
                 {'parentKey': '10500', 'value': '汽车/摩托车', 'key': '121000'},
                 {'parentKey': '10500', 'value': '大型设备/机电设备/重工业', 'key': '129900'},
                 {'parentKey': '10500', 'value': '加工制造（原料加工/模具）', 'key': '121100'},
                 {'parentKey': '10500', 'value': '仪器仪表及工业自动化', 'key': '121200'},
                 {'parentKey': '10500', 'value': '印刷/包装/造纸', 'key': '210600'},
                 {'parentKey': '10500', 'value': '办公用品及设备', 'key': '120700'},
                 {'parentKey': '10500', 'value': '医药/生物工程', 'key': '121300'},
                 {'parentKey': '10500', 'value': '医疗设备/器械', 'key': '121500'},
                 {'parentKey': '10500', 'value': '航空/航天研究与制造', 'key': '300000'},
                 {'parentKey': '11500', 'value': '交通/运输', 'key': '150000'},
                 {'parentKey': '11500', 'value': '物流/仓储', 'key': '301100'},
                 {'parentKey': '10000', 'value': '医疗/护理/美容/保健/卫生服务', 'key': '121400'},
                 {'parentKey': '10000', 'value': '酒店/餐饮', 'key': '200600'},
                 {'parentKey': '10000', 'value': '旅游/度假', 'key': '200800'},
                 {'parentKey': '11300', 'value': '媒体/出版/影视/文化传播', 'key': '210300'},
                 {'parentKey': '11300', 'value': '娱乐/体育/休闲', 'key': '200700'},
                 {'parentKey': '11600', 'value': '能源/矿产/采掘/冶炼', 'key': '130000'},
                 {'parentKey': '11600', 'value': '石油/石化/化工', 'key': '120500'},
                 {'parentKey': '11600', 'value': '电气/电力/水利', 'key': '130100'},
                 {'parentKey': '11600', 'value': '环保', 'key': '201200'},
                 {'parentKey': '11100', 'value': '政府/公共事业/非盈利机构', 'key': '200100'},
                 {'parentKey': '11100', 'value': '学术/科研', 'key': '120600'},
                 {'parentKey': '11400', 'value': '农/林/牧/渔', 'key': '100000'},
                 {'parentKey': '11400', 'value': '跨领域经营', 'key': '100100'},
                 {'parentKey': '11400', 'value': '其他', 'key': '990000'}]

    # 吕梁
    lvliangAreas = {
        "2945": "方山县","2940": "汾阳市","2949": "交城县","2948": "交口县","2947": "岚县","2944": "临县",
        "2938": "离石区","2946": "柳林县","2950": "石楼县","2941": "文水县","2939": "孝义市","2943": "兴县",
        "2942": "中阳县"
    }

    # re 区域 目标城市：武汉、北京、上海、深圳、杭州
    wuhanAreas = {
        "2367": "武汉吴家山经济技术开发区", "2366": "东湖新技术开发区", "2365": "武汉经济技术开发区", "2067": "江夏区",
        "2066": "汉南区", "2065": "东西湖区", "2064": "蔡甸区", "2063": "洪山区", "2062": "青山区", "2061": "武昌区",
        "2060": "汉阳区", "2059": "硚口区", "2058": "江汉区", "2057": "江岸区", "2069": "新洲区", "2068": "黄陂区"
        }

    beijingAreas = {
        "2001":"东城区","2012":"大兴区","2011":"房山区","2010":"顺义区","2009":"通州区","2008":"石景山区","2007":"丰台区","2006":"朝阳区",
        "2005":"海淀区","2004":"宣武区","2003":"崇文区","2002":"西城区","2018":"延庆县","2017":"密云县","2016":"门头沟区","2015":"平谷区",
        "2014":"怀柔区","2013":"昌平区"
        }

    shanghaiAreas = {
        "2023": "静安区","2022": "长宁区","2021": "徐汇区","2019": "黄浦区","2034": "青浦区","2033": "松江区","2032": "金山区",
        "2031": "浦东新区","2030": "嘉定区","2029": "宝山区","2028": "闵行区","2027": "杨浦区","2026": "虹口区","2025": "闸北区",
        "2024": "普陀区","2036": "崇明区","2035": "奉贤区"
        }

    hangzhouAreas = {
        "2409": "建德市","2457": "下沙","2479": "临安市","2478": "富阳区","2242": "淳安县","2241": "桐庐县","2240": "余杭区",
        "2239": "萧山区","2238": "滨江区","2237": "西湖区","2236": "拱墅区","2235": "江干区","2234": "下城区","2233": "上城区"
        }

    shenzhenAreas = {
        "2362": "大鹏新区","2361": "龙华新区","2044": "光明新区","2043": "坪山新区","2042": "龙岗区",
        "2041": "宝安区","2040": "盐田区","2039": "南山区","2038": "罗湖区","2037": "福田区"
        }


    # sou = "https://sou.zhaopin.com/?jl=736&re={}&in={}&sf=0&st=0"  489 武汉
    sou = "https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId={0}&industry={1}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3"


    def __init__(self):
        self.connect = pymysql.connect(
            host='192.168.1.214',
            port=3306,
            db='forwork_shanxi_ga',
            user='developer',
            passwd='123123',
            charset='utf8')
        self.cursor = self.connect.cursor()

    def lvliangSearchUrls(self):
        for re in self.lvliangAreas.keys():
            for ide in self.indentrys:
                if ide.get("parentKey") != "0":
                    key = ide.get("key")  # 小领域code
                    indentry = ide.get("value")  # 小领域汉字
                    parentCode = ide.get("parentKey")  # 父领域
                    domain = ''
                    for isy in self.indentrys:
                        if isy.get('key') == parentCode:
                            domain = isy.get("value")
                    areaCode = re  # 地区code
                    area = self.lvliangAreas.get(areaCode)
                    city = "吕梁"
                    # https://sou.zhaopin.com/?jl=736&re={}&in={}&sf=0&st=0
                    url = self.sou.format(areaCode, key)
                    domain = domain.replace("|","/")
                    print("主领域："+domain+"  副领域："+indentry+"  地区："+area+"  访问地址："+url)
                    item = {}
                    item.update({"city":city})
                    item.update({"area":area})
                    item.update({"domain":domain})
                    item.update({"indentry":indentry})
                    item.update({"url":url})
                    item.update({"urlType":"0"})
                    item.update({"recordState":"1"})
                    self.save(item)

    def save(self,item):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sqlStr = """
            INSERT INTO `forwork_shanxi_ga`.`zhilian_entp_stay_url` 
            (`city`, `area`, `domain`, `indentry`, `url`, `url_type`, `record_state`,`update_time`)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(sqlStr,(
                item['city'],
                item['area'],
                item['domain'],
                item['indentry'],
                item['url'],
                item['urlType'],
                item['recordState'],
                now
            ))
            self.connect.commit()
        except Exception as e:
            print(e)


    def getFirstUrl(self):
        sqlStr = "SELECT * FROM `forwork_shanxi_ga`.zhilian_entp_spider_url WHERE record_state = '1' ORDER BY update_time ASC LIMIT 1 "
        result = []
        try:
            self.cursor.execute(sqlStr)
            result = self.cursor.fetchone()
            self.connect.close()
        except Exception as e:
            print("获取URL失败！",e)
        finally:
            return result


def getTest(searchUrl):
    print(searchUrl)
    result = requests.get(searchUrl).text
    jspo = json.loads(result, encoding="utf-8")
    results = jspo['data']['results']
    count = jspo['data']['count']

    if count > 90:
        temUrls = searchUrl.split("start=")
        if len(temUrls) > 1:
            prevStartStr = temUrls[1].split("&")[0]
            prevStart = int(prevStartStr)
            if (prevStart + 90) <= count:
                searchUrl = searchUrl.split("start=")[0]
                searchUrl += "&start=" + str(prevStart + 90)
                getTest(searchUrl)
        else:
            searchUrl += "&start=90"
            getTest(searchUrl)


def splitJointSearchUrl(url):
    # 1、生成一个随机32位数id
    md5 = hashlib.md5()
    id = str(random.random())
    md5.update(id.encode('utf-8'))
    random_id = md5.hexdigest()
    # 2、生成当前时间戳
    now_time = int(time.time() * 1000)
    # 3、生成随机6位数
    randomnumb = int(random.random() * 1000000)
    # 4、生成32位UUID x-zp-client-id:015a58ca-5b0a-4402-83bb-28db2b85e257
    client_id = str(uuid.uuid4())
    # 组合代码
    x_zp_page_request_id = str(random_id) + '-' + str(now_time) + '-' + str(randomnumb)
    url_v = round(random.random(), 8)
    "x-zp-client-id"
    url = url+"&x_zp_page_request_id="+x_zp_page_request_id+"&_v="+str(url_v)+"&x-zp-client-id="+client_id
    return url


if __name__ == "__main__":
    spider = ByCityParseSearchUrls()
    result = spider.lvliangSearchUrls()
    spider.connect.close()
    # url = "https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=2367&industry=150000&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3"
    # rurl = splitJointSearchUrl(url)
    # print(rurl)
