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
    wuhan = "https://www.zhaopin.com/wuhan"
    sou = "https://sou.zhaopin.com/?jl=736&re={}&in={}&sf=0&st=0"

    keyword = ""

    # 领域
    # indentrys= [{'parentKey':'10100','value':'互联网/电子商务','key':'210500'[{'parentKey':'10100','value':'互联网/电子商务','key':'210500'},{'parentKey':'10100','value':'计算机软件','key':'160400'},{'parentKey':'10100','value':'IT服务(系统/数据/维护)','key':'160000'},{'parentKey':'10100','value':'电子技术/半导体/集成电路','key':'160500'},{'parentKey':'10100','value':'计算机硬件','key':'160200'},{'parentKey':'10100','value':'通信/电信/网络设备','key':'300100'},{'parentKey':'10100','value':'通信/电信运营、增值服务','key':'160100'},{'parentKey':'10100','value':'网络游戏','key':'160600'},{'parentKey':'10200','value':'基金/证券/期货/投资','key':'180000'},{'parentKey':'10200','value':'保险','key':'180100'},{'parentKey':'0','value':'IT|通信|电子|互联网','key':'10100'},{'parentKey':'10200','value':'银行','key':'300500'},{'parentKey':'0','value':'金融业','key':'10200'},{'parentKey':'10200','value':'信托/担保/拍卖/典当','key':'300900'},{'parentKey':'0','value':'房地产|建筑业','key':'10800'},{'parentKey':'10800','value':'房地产/建筑/建材/工程','key':'140000'},{'parentKey':'0','value':'商业服务','key':'10900'},{'parentKey':'10800','value':'家居/室内设计/装饰装潢','key':'140100'},{'parentKey':'0','value':'贸易|批发|零售|租赁业','key':'10300'},{'parentKey':'10800','value':'物业管理/商业中心','key':'140200'},{'parentKey':'0','value':'文体教育|工艺美术','key':'10400'},{'parentKey':'10900','value':'专业服务/咨询(财会/法律/人力资源等)','key':'200300'},{'parentKey':'0','value':'生产|加工|制造','key':'10500'},{'parentKey':'10900','value':'广告/会展/公关','key':'200302'},{'parentKey':'0','value':'交通|运输|物流|仓储','key':'11500'},{'parentKey':'10900','value':'中介服务','key':'201400'},{'parentKey':'0','value':'服务业','key':'10000'},{'parentKey':'10900','value':'检验/检测/认证','key':'201300'},{'parentKey':'0','value':'文化|传媒|娱乐|体育','key':'11300'},{'parentKey':'10900','value':'外包服务','key':'300300'},{'parentKey':'0','value':'能源|矿产|环保','key':'11600'},{'parentKey':'10300','value':'快速消费品（食品/饮料/烟酒/日化）','key':'120400'},{'parentKey':'0','value':'政府|非盈利机构','key':'11100'},{'parentKey':'10300','value':'耐用消费品（服饰/纺织/皮革/家具/家电）','key':'120200'},{'parentKey':'0','value':'农|林|牧|渔|其他','key':'11400'},{'parentKey':'10300','value':'贸易/进出口','key':'170500'},{'parentKey':'10300','value':'零售/批发','key':'170000'},{'parentKey':'10300','value':'租赁服务','key':'300700'},{'parentKey':'10400','value':'教育/培训/院校','key':'201100'},{'parentKey':'10400','value':'礼品/玩具/工艺美术/收藏品/奢侈品','key':'120800'},{'parentKey':'10500','value':'汽车/摩托车','key':'121000'},{'parentKey':'10500','value':'大型设备/机电设备/重工业','key':'129900'},{'parentKey':'10500','value':'加工制造（原料加工/模具）','key':'121100'},{'parentKey':'10500','value':'仪器仪表及工业自动化','key':'121200'},{'parentKey':'10500','value':'印刷/包装/造纸','key':'210600'},{'parentKey':'10500','value':'办公用品及设备','key':'120700'},{'parentKey':'10500','value':'医药/生物工程','key':'121300'},{'parentKey':'10500','value':'医疗设备/器械','key':'121500'},{'parentKey':'10500','value':'航空/航天研究与制造','key':'300000'},{'parentKey':'11500','value':'交通/运输','key':'150000'},{'parentKey':'11500','value':'物流/仓储','key':'301100'},{'parentKey':'10000','value':'医疗/护理/美容/保健/卫生服务','key':'121400'},{'parentKey':'10000','value':'酒店/餐饮','key':'200600'},{'parentKey':'10000','value':'旅游/度假','key':'200800'},{'parentKey':'11300','value':'媒体/出版/影视/文化传播','key':'210300'},{'parentKey':'11300','value':'娱乐/体育/休闲','key':'200700'},{'parentKey':'11600','value':'能源/矿产/采掘/冶炼','key':'130000'},{'parentKey':'11600','value':'石油/石化/化工','key':'120500'},{'parentKey':'11600','value':'电气/电力/水利','key':'130100'},{'parentKey':'11600','value':'环保','key':'201200'},{'parentKey':'11100','value':'政府/公共事业/非盈利机构','key':'200100'},{'parentKey':'11100','value':'学术/科研','key':'120600'},{'parentKey':'11400','value':'农/林/牧/渔','key':'100000'},{'parentKey':'11400','value':'跨领域经营','key':'100100'},{'parentKey':'11400','value':'其他','key':'990000'}]},{'parentKey':'10100','value':'计算机软件','key':'160400'},{'parentKey':'10100','value':'IT服务(系统/数据/维护)','key':'160000'},{'parentKey':'10100','value':'电子技术/半导体/集成电路','key':'160500'},{'parentKey':'10100','value':'计算机硬件','key':'160200'},{'parentKey':'10100','value':'通信/电信/网络设备','key':'300100'},{'parentKey':'10100','value':'通信/电信运营、增值服务','key':'160100'},{'parentKey':'10100','value':'网络游戏','key':'160600'},{'parentKey':'10200','value':'基金/证券/期货/投资','key':'180000'},{'parentKey':'10200','value':'保险','key':'180100'},{'parentKey':'0','value':'IT|通信|电子|互联网','key':'10100'},{'parentKey':'10200','value':'银行','key':'300500'},{'parentKey':'0','value':'金融业','key':'10200'},{'parentKey':'10200','value':'信托/担保/拍卖/典当','key':'300900'},{'parentKey':'0','value':'房地产|建筑业','key':'10800'},{'parentKey':'10800','value':'房地产/建筑/建材/工程','key':'140000'},{'parentKey':'0','value':'商业服务','key':'10900'},{'parentKey':'10800','value':'家居/室内设计/装饰装潢','key':'140100'},{'parentKey':'0','value':'贸易|批发|零售|租赁业','key':'10300'},{'parentKey':'10800','value':'物业管理/商业中心','key':'140200'},{'parentKey':'0','value':'文体教育|工艺美术','key':'10400'},{'parentKey':'10900','value':'专业服务/咨询(财会/法律/人力资源等)','key':'200300'},{'parentKey':'0','value':'生产|加工|制造','key':'10500'},{'parentKey':'10900','value':'广告/会展/公关','key':'200302'},{'parentKey':'0','value':'交通|运输|物流|仓储','key':'11500'},{'parentKey':'10900','value':'中介服务','key':'201400'},{'parentKey':'0','value':'服务业','key':'10000'},{'parentKey':'10900','value':'检验/检测/认证','key':'201300'},{'parentKey':'0','value':'文化|传媒|娱乐|体育','key':'11300'},{'parentKey':'10900','value':'外包服务','key':'300300'},{'parentKey':'0','value':'能源|矿产|环保','key':'11600'},{'parentKey':'10300','value':'快速消费品（食品/饮料/烟酒/日化）','key':'120400'},{'parentKey':'0','value':'政府|非盈利机构','key':'11100'},{'parentKey':'10300','value':'耐用消费品（服饰/纺织/皮革/家具/家电）','key':'120200'},{'parentKey':'0','value':'农|林|牧|渔|其他','key':'11400'},{'parentKey':'10300','value':'贸易/进出口','key':'170500'},{'parentKey':'10300','value':'零售/批发','key':'170000'},{'parentKey':'10300','value':'租赁服务','key':'300700'},{'parentKey':'10400','value':'教育/培训/院校','key':'201100'},{'parentKey':'10400','value':'礼品/玩具/工艺美术/收藏品/奢侈品','key':'120800'},{'parentKey':'10500','value':'汽车/摩托车','key':'121000'},{'parentKey':'10500','value':'大型设备/机电设备/重工业','key':'129900'},{'parentKey':'10500','value':'加工制造（原料加工/模具）','key':'121100'},{'parentKey':'10500','value':'仪器仪表及工业自动化','key':'121200'},{'parentKey':'10500','value':'印刷/包装/造纸','key':'210600'},{'parentKey':'10500','value':'办公用品及设备','key':'120700'},{'parentKey':'10500','value':'医药/生物工程','key':'121300'},{'parentKey':'10500','value':'医疗设备/器械','key':'121500'},{'parentKey':'10500','value':'航空/航天研究与制造','key':'300000'},{'parentKey':'11500','value':'交通/运输','key':'150000'},{'parentKey':'11500','value':'物流/仓储','key':'301100'},{'parentKey':'10000','value':'医疗/护理/美容/保健/卫生服务','key':'121400'},{'parentKey':'10000','value':'酒店/餐饮','key':'200600'},{'parentKey':'10000','value':'旅游/度假','key':'200800'},{'parentKey':'11300','value':'媒体/出版/影视/文化传播','key':'210300'},{'parentKey':'11300','value':'娱乐/体育/休闲','key':'200700'},{'parentKey':'11600','value':'能源/矿产/采掘/冶炼','key':'130000'},{'parentKey':'11600','value':'石油/石化/化工','key':'120500'},{'parentKey':'11600','value':'电气/电力/水利','key':'130100'},{'parentKey':'11600','value':'环保','key':'201200'},{'parentKey':'11100','value':'政府/公共事业/非盈利机构','key':'200100'},{'parentKey':'11100','value':'学术/科研','key':'120600'},{'parentKey':'11400','value':'农/林/牧/渔','key':'100000'},{'parentKey':'11400','value':'跨领域经营','key':'100100'},{'parentKey':'11400','value':'其他','key':'990000'}]
    indentrys= [{'parentKey': '10100', 'value': '互联网/电子商务', 'key': '210500'}, {'parentKey': '10100', 'value': '计算机软件', 'key': '160400'}, {'parentKey': '10100', 'value': 'IT服务(系统/数据/维护)', 'key': '160000'}, {'parentKey': '10100', 'value': '电子技术/半导体/集成电路', 'key': '160500'}, {'parentKey': '10100', 'value': '计算机硬件', 'key': '160200'}, {'parentKey': '10100', 'value': '通信/电信/网络设备', 'key': '300100'}, {'parentKey': '10100', 'value': '通信/电信运营、增值服务', 'key': '160100'}, {'parentKey': '10100', 'value': '网络游戏', 'key': '160600'}, {'parentKey': '10200', 'value': '基金/证券/期货/投资', 'key': '180000'}, {'parentKey': '10200', 'value': '保险', 'key': '180100'}, {'parentKey': '0', 'value': 'IT/通信/电子/互联网', 'key': '10100'}, {'parentKey': '10200', 'value': '银行', 'key': '300500'}, {'parentKey': '0', 'value': '金融业', 'key': '10200'}, {'parentKey': '10200', 'value': '信托/担保/拍卖/典当', 'key': '300900'}, {'parentKey': '0', 'value': '房地产/建筑业', 'key': '10800'}, {'parentKey': '10800', 'value': '房地产/建筑/建材/工程', 'key': '140000'}, {'parentKey': '0', 'value': '商业服务', 'key': '10900'}, {'parentKey': '10800', 'value': '家居/室内设计/装饰装潢', 'key': '140100'}, {'parentKey': '0', 'value': '贸易/批发/零售/租赁业', 'key': '10300'}, {'parentKey': '10800', 'value': '物业管理/商业中心', 'key': '140200'}, {'parentKey': '0', 'value': '文体教育/工艺美术', 'key': '10400'}, {'parentKey': '10900', 'value': '专业服务/咨询(财会/法律/人力资源等)', 'key': '200300'}, {'parentKey': '0', 'value': '生产/加工/制造', 'key': '10500'}, {'parentKey': '10900', 'value': '广告/会展/公关', 'key': '200302'}, {'parentKey': '0', 'value': '交通/运输/物流/仓储', 'key': '11500'}, {'parentKey': '10900', 'value': '中介服务', 'key': '201400'}, {'parentKey': '0', 'value': '服务业', 'key': '10000'}, {'parentKey': '10900', 'value': '检验/检测/认证', 'key': '201300'}, {'parentKey': '0', 'value': '文化/传媒/娱乐/体育', 'key': '11300'}, {'parentKey': '10900', 'value': '外包服务', 'key': '300300'}, {'parentKey': '0', 'value': '能源/矿产/环保', 'key': '11600'}, {'parentKey': '10300', 'value': '快速消费品（食品/饮料/烟酒/日化）', 'key': '120400'}, {'parentKey': '0', 'value': '政府/非盈利机构', 'key': '11100'}, {'parentKey': '10300', 'value': '耐用消费品（服饰/纺织/皮革/家具/家电）', 'key': '120200'}, {'parentKey': '0', 'value': '农/林/牧/渔/其他', 'key': '11400'}, {'parentKey': '10300', 'value': '贸易/进出口', 'key': '170500'}, {'parentKey': '10300', 'value': '零售/批发', 'key': '170000'}, {'parentKey': '10300', 'value': '租赁服务', 'key': '300700'}, {'parentKey': '10400', 'value': '教育/培训/院校', 'key': '201100'}, {'parentKey': '10400', 'value': '礼品/玩具/工艺美术/收藏品/奢侈品', 'key': '120800'}, {'parentKey': '10500', 'value': '汽车/摩托车', 'key': '121000'}, {'parentKey': '10500', 'value': '大型设备/机电设备/重工业', 'key': '129900'}, {'parentKey': '10500', 'value': '加工制造（原料加工/模具）', 'key': '121100'}, {'parentKey': '10500', 'value': '仪器仪表及工业自动化', 'key': '121200'}, {'parentKey': '10500', 'value': '印刷/包装/造纸', 'key': '210600'}, {'parentKey': '10500', 'value': '办公用品及设备', 'key': '120700'}, {'parentKey': '10500', 'value': '医药/生物工程', 'key': '121300'}, {'parentKey': '10500', 'value': '医疗设备/器械', 'key': '121500'}, {'parentKey': '10500', 'value': '航空/航天研究与制造', 'key': '300000'}, {'parentKey': '11500', 'value': '交通/运输', 'key': '150000'}, {'parentKey': '11500', 'value': '物流/仓储', 'key': '301100'}, {'parentKey': '10000', 'value': '医疗/护理/美容/保健/卫生服务', 'key': '121400'}, {'parentKey': '10000', 'value': '酒店/餐饮', 'key': '200600'}, {'parentKey': '10000', 'value': '旅游/度假', 'key': '200800'}, {'parentKey': '11300', 'value': '媒体/出版/影视/文化传播', 'key': '210300'}, {'parentKey': '11300', 'value': '娱乐/体育/休闲', 'key': '200700'}, {'parentKey': '11600', 'value': '能源/矿产/采掘/冶炼', 'key': '130000'}, {'parentKey': '11600', 'value': '石油/石化/化工', 'key': '120500'}, {'parentKey': '11600', 'value': '电气/电力/水利', 'key': '130100'}, {'parentKey': '11600', 'value': '环保', 'key': '201200'}, {'parentKey': '11100', 'value': '政府/公共事业/非盈利机构', 'key': '200100'}, {'parentKey': '11100', 'value': '学术/科研', 'key': '120600'}, {'parentKey': '11400', 'value': '农/林/牧/渔', 'key': '100000'}, {'parentKey': '11400', 'value': '跨领域经营', 'key': '100100'}, {'parentKey': '11400', 'value': '其他', 'key': '990000'}]

    # re 区域
    areas = {
        "2367":"武汉吴家山经济技术开发区","2366":"东湖新技术开发区","2365":"武汉经济技术开发区","2067":"江夏区",
        "2066":"汉南区","2065":"东西湖区","2064":"蔡甸区","2063":"洪山区","2062":"青山区","2061":"武昌区",
        "2060":"汉阳区","2059":"硚口区","2058":"江汉区","2057":"江岸区","2069":"新洲区","2068":"黄陂区"
    }


    def __init__(self):
        self.connect = pymysql.Connect(host="192.168.1.214",port=3306,user="spider",passwd="123456",db="forwork_ga",charset="utf8")
        self.cursor = self.connect.cursor()

    def openDriver(self):
        proxy = Proxy(
            {
                'proxyType': ProxyType.MANUAL,  # 用不用都行
                # '203.130.46.108:9090'
                # '117.127.0.202:8080'   00
                # '120.234.63.196:3128'  00
                'httpProxy': '101.231.104.82:80'
            }
        )
        # 新建一个“期望技能”，哈哈
        desired_capabilities = DesiredCapabilities.FIREFOX.copy()
        proxy.add_to_capabilities(desired_capabilities)
        self.driver = webdriver.Firefox(executable_path=self.firefoxPath,desired_capabilities=desired_capabilities)
        self.driver.maximize_window()
        self.driver.get(self.wuhan)
        # 手动登录时间
        # time.sleep(20)
        allhandles = self.driver.window_handles
        currenthandle = self.driver.current_window_handle
        if currenthandle != allhandles[-1]:
            self.driver.close()
            self.driver.switch_to.window(allhandles[-1])
        #################### 开始搜索 #######################
        print(self.areas.keys())
        for re in self.areas.keys():
            for ide in self.indentrys:
                if ide.get("parentKey") != "0":
                    print("进入循环")
                    self.key = ide.get("key")              # 小领域code
                    self.keyword = ide.get("value")        # 小领域汉字
                    self.parentCode = ide.get("parentKey") # 父领域
                    self.areaCode = re                     # 地区code
                    # https://sou.zhaopin.com/?jl=736&re={}&in={}&sf=0&st=0
                    self.driver.get(self.sou.format(self.areaCode,self.key))
                    print("开始搜素！")
                    time.sleep(5)
                    self.parseList()

    def parseList(self):
        searchBox = WebDriverWait(self.driver,10).until(lambda x: x.find_element_by_class_name("search-box"))
        # 使用关键词查询、
        if None != searchBox:
            searchInput = searchBox.find_element_by_tag_name("input")
            if None != searchInput:
                searchInput.send_keys(self.keyword.decode(encoding='utf-8'))
                time.sleep(random.randint(2,3))
                searchA = searchBox.find_element_by_tag_name("a")
                if None != searchA:
                    searchA.click()
                    time.sleep(random.randint(2,3))
                    searchA.click()
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

                            #武汉-江夏区
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
        if area == "" or area == None:
            area = self.areas.get(self.areaCode)
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
        postItem.update({"postType": "全职"})
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
        INSERT INTO `forwork_ga`.`zhilian_entp`
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
            INSERT INTO `forwork_ga`.`zhilian_entp_post`
            (`entp_id`, `post_name`, `salary`, `area`, `city`, `work_exp`, `entp_ui`, 
            `education`, `post_num`, `post_highlights`, `post_desc`,`replace_time`,
            `address`,`record_status`,`create_time`, `update_time`,`post_type`) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(sqlStr, (
                postItem['entpId'],postItem['postName'],postItem['salary'],postItem['area'],postItem['city'],postItem['workExp'],postItem['entpUi'],
                postItem['education'],postItem['postNum'],postItem['postHighlights'],postItem['postDesc'],postItem['replaceTime'],
                postItem['address'],'0',now,now,postItem['postType']
            ))
            self.connect.commit()
        except Exception as e:
            print(e)

    # 通过企业名称查询数据库
    def existEntpFromDB(self,entpName):
        searchSql = ("SELECT id,entp_info,city,area,person_scope FROM zhilian_entp where entp_name ='"+entpName.encode('utf-8')+"'")
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
        searchSql = ("UPDATE zhipin_entp SET entp_info = %s,city = %s,area=%s,person_scope = %s,highlight = %s where id = %s")
        """"
        entpItem.update({"id": items[0]})
            entpItem.update({"city": city})
            entpItem.update({"area": area})
            entpItem.update({"content": content})
            entpItem.update({"highlight": highlight})
            entpItem.update({"personScope": personScope})
        """
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
            self.cursor.execute("DELETE FROM zhilian_entp_post WHERE id = "+entpId)
            self.connect.commit()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    spider = ZhilianSpider()
    spider.openDriver()
    spider.connect.close()
    spider.driver.quit()
