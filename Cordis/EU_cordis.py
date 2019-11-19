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
import requests

class CordisSpider(object):

    urls = [
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
        "https://cordis.europa.eu/project/rcn/223890/factsheet/en",
        "https://cordis.europa.eu/project/rcn/216064/factsheet/en",
        "https://cordis.europa.eu/project/rcn/199751/factsheet/en",
        "https://cordis.europa.eu/project/rcn/218616/factsheet/en",
        "https://cordis.europa.eu/project/rcn/198797/factsheet/en",
        "https://cordis.europa.eu/project/rcn/193292/factsheet/en",
        "https://cordis.europa.eu/project/rcn/212577/factsheet/en",
        "https://cordis.europa.eu/project/rcn/211875/factsheet/en",
        "https://cordis.europa.eu/project/rcn/209696/factsheet/en",
        "https://cordis.europa.eu/project/rcn/205807/factsheet/en",
        "https://cordis.europa.eu/project/rcn/216354/factsheet/en",
        "https://cordis.europa.eu/project/rcn/211080/factsheet/en",
        "https://cordis.europa.eu/project/rcn/218720/factsheet/en",
        "https://cordis.europa.eu/project/rcn/219108/factsheet/en",
        "https://cordis.europa.eu/project/rcn/219103/factsheet/en",
        "https://cordis.europa.eu/project/rcn/220360/factsheet/en",
        "https://cordis.europa.eu/project/rcn/218727/factsheet/en",
        "https://cordis.europa.eu/project/rcn/219938/factsheet/en",
        "https://cordis.europa.eu/project/rcn/220361/factsheet/en",
        "https://cordis.europa.eu/project/rcn/213179/factsheet/en",
        "https://cordis.europa.eu/project/rcn/213157/factsheet/en",
        "https://cordis.europa.eu/project/rcn/213144/factsheet/en",
        "https://cordis.europa.eu/project/rcn/213123/factsheet/en",
        "https://cordis.europa.eu/project/rcn/213188/factsheet/en",
        "https://cordis.europa.eu/project/rcn/213086/factsheet/en",
        "https://cordis.europa.eu/project/rcn/213168/factsheet/en",
        "https://cordis.europa.eu/project/rcn/223279/factsheet/en",
        "https://cordis.europa.eu/project/rcn/220679/factsheet/en",
        "https://cordis.europa.eu/project/rcn/222608/factsheet/en",
        "https://cordis.europa.eu/project/rcn/218595/factsheet/en",
        "https://cordis.europa.eu/project/rcn/218050/factsheet/en",
        "https://cordis.europa.eu/project/rcn/217697/factsheet/en",
        "https://cordis.europa.eu/project/rcn/216370/factsheet/en",
        "https://cordis.europa.eu/project/rcn/214655/factsheet/en",
        "https://cordis.europa.eu/project/rcn/214073/factsheet/en"
    ]

    def __init__(self):
        self.connect = pymysql.connect(host='127.0.0.1',
            port=3306,
            db='eu_cordis',
            user='root',
            passwd='root',
            charset="utf8")
        self.cursor = self.connect.cursor()

    def openDriver(self):
        proxy = Proxy(
            {
                # 'proxyType': ProxyType.MANUAL,  # 用不用都行
                # 'httpProxy': '122.137.185.240:80'
                'httpProxy': '123.232.199.89:8118'  # 27.上午
                # 'httpProxy': '115.159.155.83:8118'  # 27.上午
                # 'httpProxy': '115.219.12.145:8118'
            }
        )
        # 新建一个“期望技能”，哈哈
        # desired_capabilities = DesiredCapabilities.FIREFOX.copy()
        # # 把代理ip加入到技能中
        # proxy.add_to_capabilities(desired_capabilities)
        host = "https://cordis.europa.eu"
        chromePath = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        firePath = "D:\\software\\Firefox\\geckodriver.exe"
        #带代理请求
        # self.driver = webdriver.Firefox(executable_path=firePath,desired_capabilities=desired_capabilities)
        self.driver = webdriver.Firefox(executable_path=firePath)
        self.driver.get(host)
        # 窗口最大化
        self.driver.maximize_window()
        # 隐式等待10s
        self.driver.implicitly_wait(10)

    def requestList(self):
        for url in self.urls:
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            self.parseResource()

    def parseResource(self):

        try:
            # 等待元素显示
            WebDriverWait(driver= self.driver,timeout=10,poll_frequency=0.5,).until(expected_conditions.presence_of_element_located(By.CLASS_NAME,"ux-tab-content"))
        except TimeoutException as e:
            print(e)

        source = self.driver.page_source

        projectTitle = self.driver.find_element_by_css_selector(".col-12.col-sm-10.col-md-10.title").text
        projectName = self.driver.find_element_by_class_name("acronym").text
        country = self.driver.find_element_by_class_name("coordinator-country").text
        purpose = self.driver.find_element_by_css_selector(".general-text.objective").text
        leadDiv = self.driver.find_element_by_class_name("coordinator-block")
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
        cordisDict['projectTitle'] = projectTitle
        cordisDict['projectName'] = projectName
        cordisDict['projectStatus'] = projectStatus
        cordisDict['leaderOrg'] = leaderOrg
        cordisDict['country'] = country
        cordisDict['startDate'] = startDate
        cordisDict['endDate'] = endDate
        cordisDict['purpose'] = purpose
        self.save(cordisDict)

    def save(self,cordisDict):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            sqlStr = """INSERT INTO cordis_project 
                        (`project_name`,  `project_title`, `purpose`,
                         `lead_org`, `country`, `start_date`, `end_date`, 
                         `create_time`, `update_time`, `project_status`) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

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
                cordisDict['projectStatus']))
            self.connect.commit()
        except Exception as e:
            print(e)

if __name__ == '__main__':

    spider = CordisSpider()
    spider.openDriver()
    time.sleep(2)
    spider.requestList()







