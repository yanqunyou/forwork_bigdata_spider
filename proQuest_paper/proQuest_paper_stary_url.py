# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         lagou_entp_post_spider
# Description:  
# Author:       forwork
# Date:         2019/7/29
#-------------------------------------------------------------------------------

import pymysql
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType, Proxy
from selenium.webdriver.support.select import By
from rollElementUtil import RollElementUtil

import random

class ProQuestSpider(object):
    firefoxPath = "E:\\soft\\Firefox\\geckodriver.exe"
    chromePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
    host = "http://www.pqdtcn.com/"

    baseUrl = "http://www.pqdtcn.com/basic"
    detailBaseUrl = "http://www.pqdtcn.com"

    domains = [
        '大数据',
        '5G',
        '云制造',
        '物联网',
        '区块链',
        '人工智能',
        '云计算'
    ]

    domain = "5G"

    def __init__(self):
        self.connect = pymysql.connect(host='192.168.1.214',
                                       port=3306,
                                       db='forwork_ga',
                                       user='spider',
                                       passwd='123456',
                                       charset='utf8')
        self.cursor = self.connect.cursor()
        self.rollUtil = RollElementUtil()

    def openDriver(self):
        proxy = Proxy(
            {
                'proxyType': ProxyType.MANUAL,  # 用不用都行
                # '203.130.46.108:9090'
                # '117.127.0.202:8080'   00
                # '120.234.63.196:3128'  00
                'httpProxy': '60.217.132.244:8060'
            }
        )
        # 新建一个“期望技能”，哈哈
        desired_capabilities = DesiredCapabilities.FIREFOX.copy()
        proxy.add_to_capabilities(desired_capabilities)
        # self.driver = webdriver.Firefox(executable_path=self.firefoxPath,desired_capabilities=desired_capabilities)
        self.driver = webdriver.Firefox(executable_path=self.firefoxPath)
        self.driver.get(self.host)
        time.sleep(10)

        self.driver.get(self.baseUrl)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        try:
            WebDriverWait(self.driver,10,0.5).until(lambda x: x.find_element_by_id("searchStr"))
        except Exception as e:
            print(e)
        time.sleep(8)
        searchInput = self.driver.find_element_by_id("searchStr")
        if None != searchInput:
            # searchInput.send_keys(self.domain)
            time.sleep(4)
            submitBtn = self.driver.find_element_by_id("basic_searchData")
            submitBtn.click()
            self.parseSearchPage(self.domain)

    def parseSearchPage(self,domain):
        try:
            WebDriverWait(self.driver,10,0.5).until(lambda x:x.find_element_by_id("basic_search"))
        except Exception as e:
            print(e)
        time.sleep(random.randint(3,5))
        searchDiv = self.driver.find_element_by_id("basic_search")
        if None != searchDiv:
            tables = searchDiv.find_elements(By.CLASS_NAME,"table")
            print(len(tables))
            for i in range(len(tables)):
                tr = tables[i].find_element_by_tag_name("tr")
                a = tr.find_element_by_tag_name("a")
                print(a.text)
                url = self.detailBaseUrl+a.get_attribute("href")
                self.insertStayUrl(url,domain)

            try:
                pageDiv = self.driver.find_element_by_id("basic_page")
                nextPage = pageDiv.find_element_by_class_name("layui-laypage-next")
                try:
                    self.rollUtil.rollToView_bottom(self.driver,nextPage)
                    nextPage.click()
                except Exception as e:
                    self.rollUtil.rollToView_top(self.driver, nextPage)
                    nextPage.click()

                time.sleep(random.randint(2,4))
                self.parseSearchPage(self.domain)
            except Exception as e:
                print("can't find next page btn ：： ",e)


    def insertStayUrl(self,url,domain):
        insertStr = """
        INSERT INTO proquest_paper_stary_url (`url`,`domain`,`status`) values (%s,%s,%s) ;
        """
        try:
            self.cursor.execute(insertStr,(
                url,domain,'1'
            ))
        except Exception as e:
            print(e)
            self.connect.rollback()
        finally:
            self.connect.commit()


if __name__ == "__main__":
    wanFangSpider = ProQuestSpider()
    wanFangSpider.openDriver()
    # lagouSpider.driver.close()