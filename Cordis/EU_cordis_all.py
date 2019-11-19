# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         EU_cordis
# Description:  
# Author:       forwork
# Date:         2019/5/30
#-------------------------------------------------------------------------------
import random
import time

import pymysql
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Proxy, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class CordisSpider(object):
    # 项目列表页，没有参数
    host = "https://cordis.europa.eu/search/en?q=contenttype%3D%27project%27&p=1&num=10&srt=Relevance:decreasing"

    list_base_url = "https://cordis.europa.eu/search/en?q=contenttype%3D%27project%27%20AND%20exploitationDomain%2Fcode%3D%27{0}%27&p=1&num=10&srt=Relevance:decreasing"

    list = [
        "https://cordis.europa.eu/project/rcn/223595/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223582/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223577/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223568/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223334/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223332/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223329/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223324/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223320/factsheet/en",
        "https://cordis.europa.eu/project/rcn/221895/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223285/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223344/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223308/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223267/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223258/factsheet/en",
        "https://cordis.europa.eu/project/rcn/222629/factsheet/en",
        "https://cordis.europa.eu/project/rcn/222585/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223439/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223398/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223318/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223190/factsheet/en",
    ]

    domains={
        "indust":"Industrial Technologies",
        "funda":"Fundamental Research",
        "trans":"Transport and Mobility",
        "health":"Health",
        "society":"Society",
        "secur":"Security",
        "env":"Climate Change and Environment",
        "ener":"Energy",
        "space":"Space",
        "ict":"Digital Economy",
        "agri":"Food and Natural Resources"
        }

    domains_chinese = {
        "indust":"工业技术",
        "funda":"基础研究",
        "trans":"运输和流动性",
        "health":"健康",
        "society":"社会",
        "secur":"安全",
        "env":"气候变化与环境",
        "ener":"能源",
        "space":"空间",
        "ict":"数字经济",
        "agri":"食物和自然资源"
        }

    items = [
        "Fact Sheet",  # 情况说明书
        "Reporting",   # 报告
        "Result in Brief", # 结果简介
        "Results",         # 成果
        "News & Multimedia" # 新闻与多媒体
    ]

    def __init__(self):
        self.connect = pymysql.connect(host='127.0.0.1',
            port=3306,
            db='for_test',
            user='root',
            passwd='root',
            charset="utf8")
        self.cursor = self.connect.cursor()

    def openDriver(self):
        '123.115.240.148:8118' # 普匿
        '111.77.100.60:8118' # 高匿
        proxy = Proxy(
            {
                # 'proxyType': ProxyType.MANUAL,  # 用不用都行
                # 'httpProxy': '112.87.131.160:8118'
                # 'httpProxy': '111.77.100.60:8118'
                # 'httpProxy': '115.28.148.192:8118'  # 27.上午
                # 'httpProxy': '62.221.41.130:8080'  # 27.上午
                'httpProxy': '117.63.156.123:8118'
            }
        )
        # 新建一个“期望技能”，哈哈
        desired_capabilities = DesiredCapabilities.FIREFOX.copy()
        # # 把代理ip加入到技能中
        proxy.add_to_capabilities(desired_capabilities)
        host = "https://cordis.europa.eu"
        chromePath = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        # firePath = "D:\\software\\Firefox\\geckodriver.exe"
        # self.driver = webdriver.Firefox(executable_path=firePath,desired_capabilities=desired_capabilities)

        self.driver = webdriver.Chrome(executable_path=chromePath,desired_capabilities=desired_capabilities)

        self.driver.get(host)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    # domains 条件
    def requestList(self):
            daKeys = self.domains.keys()
            da = "secur"
            listUrl = self.list_base_url.format(da)
            self.driver.get(listUrl)
            time.sleep(2)
            self.parseList(da)

            # for da in daKeys:
            #     listUrl = self.list_base_url.format(da)
            #     self.driver.get(listUrl)
            #     time.sleep(2)
            #     self.parseList(da)

    def parseList(self,domain):
        try:
            # located2 = (By.CSS_SELECTOR,".col-12.ng-star-inserted")
            located2 = (By.CLASS_NAME,"linked-content row")
            WebDriverWait(driver=self.driver, timeout=10, poll_frequency=0.5).until(
                expected_conditions.presence_of_element_located(located2))
        except Exception as e:
            time.sleep(random.randint(2,4))
            print(e)
        print(self.driver.current_url)

        time.sleep(random.randint(5,7))
        aDivs = self.driver.find_elements_by_css_selector(".col-sm-12.col-lg")
        if None != aDivs:
            for div in aDivs:
                try:
                    a = div.find_element(By.TAG_NAME,"a")
                    self.driver.execute_script("arguments[0].scrollIntoView();",a)
                    ahref = a.get_attribute("href")
                    js = 'window.open(\"'+ahref+'\")'
                    self.driver.execute_script(js)
                    # 将句柄调到详情页
                    allHandles = self.driver.window_handles
                    self.driver.switch_to.window(allHandles[-1])
                    time.sleep(random.randint(5,8))
                    self.parseDetail(domain,ahref)
                except Exception as e:
                    # 发生异常：点击下一页时加载异常，回退到上一页
                    self.driver.back()
                    self.driver.implicitly_wait(10)
                    # 寻找并点击下一页，解析list
                    self.searchNextAndClick(domain)
                    print(e)
        # 寻找并点击下一页，解析list
        self.searchNextAndClick(domain)
        print(u"分页：："+self.driver.current_url)


    def parseDetail(self,domain,url):
        # WebDriverWait(driver=self.driver,timeout=6,poll_frequency=0.5,ignored_exceptions=None)
        time.sleep(random.randint(4,6))
        source = self.driver.page_source
        myurl = self.driver.current_url
        print(myurl)
        if 'factsheet' not in myurl:
            self.logUrl(myurl,domain)
            self.closeDetail()
        else:
            try:
                located1 = (By.CLASS_NAME,"ng-star-inserted")
                WebDriverWait(driver=self.driver, poll_frequency=0.5, timeout=10).until(expected_conditions.presence_of_all_elements_located(located1))
            except TimeoutException as e:
                print(e)

            domain = self.domains.get(domain)
            projectTitle = ''
            try:
                # col-12 col-sm-10 col-md-10 title
                projectTitle = self.driver.find_element_by_css_selector(".col-12.col-sm-10.col-md-10.title.ng-star-inserted").text
            except NoSuchElementException as e:
                projectTitle = self.driver.find_element_by_css_selector(".col-12.col-sm-10.col-md-10.title").text
                print(e)
            else:
                return

            projectName = self.driver.find_element_by_class_name("acronym").text
            country = self.driver.find_element_by_class_name("coordinator-country").text
            leadDiv = self.driver.find_element_by_class_name("coordinator-block")
            purpose = self.driver.find_element_by_css_selector(".general-text.objective").text
            leaderOrg = ''
            if None != leadDiv:
                leaderOrg = leadDiv.find_element_by_css_selector(".coordinated.coordinated-name").text

            startDate = ''
            endDate = ''
            projectStatus = ''
            rightDiv = self.driver.find_element_by_class_name("grey-background")
            if None != rightDiv:
                lis = rightDiv.find_element_by_css_selector(".row.padding5.date-row").find_elements(By.TAG_NAME, "li")
                startDate = lis[0].find_element_by_class_name("date").text
                endDate = lis[1].find_element_by_class_name("date").text

                pd15s = rightDiv.find_element_by_css_selector(".col-sm-4.col-md-12.col-lg-12").find_elements_by_class_name(
                    "padding15")
                if len(pd15s) > 0:
                    for pd in pd15s:
                        if "Status" in pd.text:
                            projectStatus = pd.find_element_by_css_selector(".date.padding5").text

            cordisDict={}
            keywords = ""

            itemsDiv = self.driver.find_element_by_class_name("ux-tabs__items")
            if None!=itemsDiv:
                items = itemsDiv.find_elements_by_class_name("ux-tab-item")
                if None != items:
                    for it in items:
                        if "Result in Brief" in it.text:
                            it.click()
                            time.sleep(1)
                            try:
                                keywordsP = self.driver.find_element_by_css_selector(".text-keywords.padding-bottom")
                                if None != keywordsP:
                                    keywords = keywordsP.text.strip()
                            except Exception as e:
                                print(e)

            cordisDict['projectTitle'] = projectTitle
            cordisDict['projectName'] = projectName
            cordisDict['projectStatus'] = projectStatus
            cordisDict['leaderOrg'] = leaderOrg
            cordisDict['country'] = country
            cordisDict['startDate'] = startDate
            cordisDict['endDate'] = endDate
            cordisDict['purpose'] = purpose
            cordisDict['keywords'] = keywords
            cordisDict['domain'] = domain
            self.save(cordisDict)
            time.sleep(2)
            self.closeDetail()

    def save(self,cordisDict):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            sqlStr = """INSERT INTO cordis_project 
                        (`project_name`,  `project_title`, `purpose`,
                         `lead_org`, `country`, `start_date`, `end_date`, 
                         `create_time`, `update_time`, `project_status`,`keywords`,`domain`) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            self.cursor.execute(sqlStr,(
                cordisDict['projectName'],
                cordisDict['projectTitle'],
                cordisDict['purpose'],
                cordisDict['leaderOrg'],
                cordisDict['country'],
                cordisDict['startDate'],
                cordisDict['endDate'],
                now,
                now,
                cordisDict['projectStatus'],
                cordisDict['keywords'],
                cordisDict['domain']
            ))
            self.connect.commit()
        except Exception as e:
            print(e)

    def closeDetail(self):
        handles = self.driver.window_handles
        myhandle = self.driver.current_window_handle
        if len(handles) > 1:
            for i in range(len(handles)):
                if i > 0:
                    self.driver.switch_to.window(handles[i])
                    self.driver.close()
        self.driver.switch_to.window(handles[0])

    def logUrl(self,url,domain):
        with open("./log/domain_logs.txt",'a+') as f:
            str = url+":"+domain+",\n"
            f.write(str)
            f.close()
    def searchNextAndClick(self,domain):
        try:
            # ui-paginator-next ui-paginator-element ui-state-default ui-corner-all
            # ui-paginator-next ui-paginator-element ui-state-default ui-corner-all ui-state-disabled
            nextButton = self.driver.find_element_by_css_selector(".ui-paginator-next.ui-paginator-element.ui-state-default.ui-corner-all")
            if None != nextButton:
                self.driver.execute_script("arguments[0].scrollIntoView();", nextButton)
                nextButton.click()
                self.parseList(domain)
        except Exception as e:
            nextButton = self.driver.find_element_by_css_selector(
                ".ui-paginator-next.ui-paginator-element.ui-state-default.ui-corner-all.ui-state-disabled")
            if None != nextButton:
                self.driver.execute_script("arguments[0].scrollIntoView();", nextButton)
                nextButton.click()
                self.parseList(domain)
            print(e)

if __name__ == '__main__':

    spider = CordisSpider()
    spider.openDriver()
    spider.driver.get("https://cordis.europa.eu/search/en?q=contenttype%3D%27project%27&p=1&num=10&srt=Relevance:decreasing")
    spider.driver.implicitly_wait(5)
    spider.requestList()
    print(spider.driver.current_url)

    spider.driver.quit()








