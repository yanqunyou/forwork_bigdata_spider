# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         patent_data_crawl_save_logic
# Description:  
# Author:       forwork
# Date:         2019/8/12
#-------------------------------------------------------------------------------
import requests
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType, Proxy
import pymysql

from selenium import webdriver
class PatentDataCrawlSave(object):

    url = "http://list.kjcg123.com:8080/wokejinews/news/detail.html?type=2&id=110241"

    firePath = "D:\\software\\Firefox\\geckodriver.exe"

    def __init__(self):
        self.mysqlContent = pymysql.connect(host='192.168.1.214', port=3306, db='forwork_ga', user='spider', passwd='123456', charset='utf8')
        self.mysqlCursor = self.mysqlContent.cursor()

    def openDriver(self):
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,  # 用不用都行
            'httpProxy': '36.249.109.46:9999'
        })

        # 新建一个“期望技能”，哈哈
        capabilities = DesiredCapabilities.FIREFOX.copy()
        proxy.add_to_capabilities(capabilities)
        self.driver = webdriver.Firefox(executable_path=self.firePath,desired_capabilities=capabilities)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.startRequest()

    def startRequest(self):
        urlList = self.getStaryUrls()
        if len(urlList) >0:
            for ul in urlList:
                print(ul[0])
                self.driver.get(url=ul[0])
                self.parsePatent()

    def parsePatent(self):
        try:
            WebDriverWait(driver=self.driver,timeout=10,poll_frequency=0.5).until(lambda x: x.find_element_by_class_name("project_detail"))
        except Exception as e:
            print(e)
        patentItem = {}
        patentName = ""
        patentTime = ""
        patentNo = ""
        patentAuthor = ""
        patentStatus = ""
        patentIndustry = ""
        patentPrice = ""
        patentType = ""
        cooperationWay = ""
        province = ""
        city = ""
        area = ""

        sout = BeautifulSoup(self.driver.page_source,"html.parser")
        projectDetailDiv = sout.find("div",{"className":"project_detail"})
        print(projectDetailDiv)
        if None != projectDetailDiv:
            projectTitleDiv = projectDetailDiv.find("div",{"class":"project_title"})
            if None != projectTitleDiv:
                patentName = projectTitleDiv.h2.getText()
                # projectDetailDiv.span.getText()

            projectInfoDiv = projectDetailDiv.find("div",{"class":"project_info"})
            if None != projectInfoDiv:
                patentTime = projectInfoDiv.date.getText()

            # projectTable1Div = projectDetailDiv.find({"class":"project_table1"})
            # if None != projectTable1Div:
            #     td1Trs = projectTable1Div.findAll("tr")
            #     if None != td1Trs:
            #         price = td1Trs[1].td.getText().replace("","")
            #         if "万元" == price:
            #             patentPrice = ""
            #         else:
            #             patentPrice = price

            projectTable2 = projectDetailDiv.find("div",{"class":"project_table2"})
            if None != projectTable2:
                td2Trs = projectTable2.findAll("tr")

                td1s = td2Trs[1].findAll("td")
                patentNo = td1s[1].getText().strip()
                patentAuthor = td1s[3].getText().strip()

                patentStatus = td2Trs[3].findAll("td")[1].getText().strip()
                patentIndustry = td2Trs[4].findAll("td")[1].getText().strip()

                td5s = td2Trs[5].findAll("td")
                patentPrice = td5s[1].getText().strip()
                address = td5s[3].getText().strip()
                adSps = address.split(",")
                for i in range(len(adSps)):
                    if "省" in adSps[i]  or "自治区" in adSps[i]:
                        province = adSps[i]
                    elif "北京" in adSps[i] or "上海" in adSps[i] or "天津" in adSps[i] or "重庆" in adSps[i]:
                        province = adSps[i]
                        city = adSps[i]
                    elif "市" in adSps[i] or "盟" in adSps[i] or "自治州" in adSps[i]:
                        city = adSps[i]
                    elif "自治" in adSps[i] or "县" in adSps[i] or "乡" in adSps[i] or "旗" in adSps[i] or "镇" in adSps[i] or "区" in adSps[i]:
                        area = adSps[i]

                patentType = td2Trs[6].findAll("td")[1].getText()
                cooperationWay = td2Trs[7].findAll("td")[1].getText()

        patentItem['patentName'] = patentName
        patentItem['patentTime'] = patentTime
        patentItem['patentNo'] = patentNo
        patentItem['patentAuthor'] = patentAuthor
        patentItem['patentStatus'] = patentStatus
        patentItem['patentIndustry'] = patentIndustry
        patentItem['patentPrice'] = patentPrice
        patentItem['patentType'] = patentType
        patentItem['cooperationWay'] = cooperationWay
        patentItem['province'] = province
        patentItem['city'] = city
        patentItem['area'] = area
        print(patentItem)
        self.driver.close()

    def getStaryUrls(self):
        searchStr = "SELECT url FROM alone_patent WHERE patent_name IS NULL LIMIT 0,10;"
        self.mysqlCursor.execute(searchStr)
        result = self.mysqlCursor.fetchall()
        return result



if __name__ == "__main__":
    crawlSpider = PatentDataCrawlSave()
    crawlSpider.openDriver()




