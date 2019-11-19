# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         lagou_entp_post_spider
# Description:  
# Author:       forwork
# Date:         2019/7/29
#-------------------------------------------------------------------------------

import pymysql
from bs4 import BeautifulSoup
import requests
import re
import time
import sys
import multiprocessing
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.common.proxy import ProxyType, Proxy
from selenium.webdriver.support.select import By
from rollElementUtil import RollElementUtil

import random

class ProQuestPaperSpider(object):
    firefoxPath = "E:\\soft\\Firefox\\geckodriver.exe"
    chromePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
    host = "http://www.pqdtcn.com/"

    def __init__(self):
        self.connect = pymysql.connect(host='192.168.1.214',
                                       port=3306,
                                       db='forwork_ga',
                                       user='spider',
                                       passwd='123456',
                                       charset='utf8')
        self.cursor = self.connect.cursor()
        self.rollHandleUtil = RollElementUtil()

    def openDriver(self):
        proxy = Proxy(
            {
                'proxyType': ProxyType.MANUAL,  # 用不用都行
                # '203.130.46.108:9090'
                # '117.127.0.202:8080'   00
                # '120.234.63.196:3128'  00
                'httpProxy': '114.99.10.66:61234'
            }
        )
        # 新建一个“期望技能”，哈哈
        desired_capabilities = DesiredCapabilities.FIREFOX.copy()
        proxy.add_to_capabilities(desired_capabilities)
        self.driver = webdriver.Firefox(executable_path=self.firefoxPath,desired_capabilities=desired_capabilities)
        self.driver.get(self.host)
        time.sleep(6)

        urlList = self.getProQuestStaryUrls()
        print("list ::  ",urlList)
        if len(urlList) >0:
            for i in range(len(urlList)):
                item = {}
                detailUrl = urlList[i][1][21:]
                domain = urlList[i][2]
                pid = urlList[i][0]
                item['url'] = detailUrl
                item['pid'] = pid
                item['domain'] = domain
                self.driver.get(detailUrl)
                self.driver.maximize_window()
                self.driver.implicitly_wait(10)
                self.parseSearchPage(item)
                time.sleep(random.randint(4,6))

    def parseSearchPage(self,item):
        print(self.driver.current_url)
        try:
            WebDriverWait(driver=self.driver,timeout=10,poll_frequency=0.5).until(expected_conditions.presence_of_element_located((By.ID,"index")))
        except TimeoutException as e:
            print(e)

        paperItem = {}
        paperName = ""
        remarks = ""
        paperIndustry = ""
        paperAuthor = ""
        paperDate = ""
        authorOrg = ""
        paperOrigin = ""
        address = ""
        ISBN = ""
        tutor = ""
        committee = ""
        academicDegree = ""
        language = ""
        url = ""
        domain = ""
        try:
            paperName = self.driver.find_element_by_id("thesis_title").text.strip()
            summaryDiv = self.driver.find_element_by_id("summary")
            remarks = summaryDiv.find_element_by_tag_name("div").find_element_by_tag_name("span").text.strip()
        except Exception as e:
            print(e)

        try:
            baseDiv = self.driver.find_element_by_id("index")
            # bDiv = baseDiv.find_element_by_tag_name("div")
            recordDataDivs = baseDiv.find_elements_by_class_name("display_record_indexing_data")
            paperIndustry =recordDataDivs[0].text.strip()
            paperAuthor =recordDataDivs[2].text.strip()
            paperDate =recordDataDivs[4].text.strip()
            authorOrg =recordDataDivs[6].text.strip()
            paperOrigin =recordDataDivs[7].text.strip()
            address =recordDataDivs[8].text.strip()
            if len(address) <1:
                address = recordDataDivs[9].text.strip()
            ISBN =recordDataDivs[10].text.strip()
            tutor = recordDataDivs[11].text.strip()
            committee = recordDataDivs[12].text.strip()
            academicDegree = recordDataDivs[13].text.strip()
            language = recordDataDivs[14].text.strip()
            url = self.driver.current_url
            domain = item['domain']
        except Exception as e:
            print(e)
            return

        paperItem['url'] = url
        paperItem['domain'] = domain
        paperItem['paperName'] = paperName
        paperItem['remarks'] = remarks
        paperItem['paperIndustry'] = paperIndustry
        paperItem['paperAuthor'] = paperAuthor
        paperItem['paperDate'] = paperDate
        paperItem['authorOrg'] = authorOrg
        paperItem['paperOrigin'] = paperOrigin
        paperItem['address'] = address
        paperItem['ISBN'] = ISBN
        paperItem['tutor'] = tutor
        paperItem['committee'] = committee
        paperItem['academicDegree'] = academicDegree
        paperItem['language'] = language
        print(paperItem)
        pid = item['pid']
        if self.insertPaper(paperItem):
            self.updateStaryUrl(pid,'0')
        else:
            self.updateStaryUrl(pid,'2')


    def getProQuestStaryUrls(self):
        strSql = "SELECT * FROM proquest_paper_stary_url WHERE `status` = '1' LIMIT 200;"
        result = []
        try:
            self.cursor.execute(strSql)
            result = self.cursor.fetchall()
        except Exception as e:
            print("get url fail ！", e)
        finally:
            return result

    def updateStaryUrl(self,id,status):
        updateStr = "UPDATE proquest_paper_stary_url SET `status` = {0} WHERE id = {1}".format(status,str(id))
        try:
            self.cursor.execute(updateStr)
        except Exception as e:
            self.connect.rollback()
            print(e)
        finally:
            self.connect.commit()


    def insertPaper(self,item):
        isSuccess = True
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        insertStr = """
        INSERT INTO `forwork_ga`.`alone_paper`
        (`paper_name`, `paper_author`, `domain`, `paper_industry`, 
        `paper_date`, `author_org`, `paper_origin`, `address`, 
        `ISBN`, `tutor`, `committee`, `academic_degree`, `language`, 
        `url`, `remarks`, `create_time`, `update_time`) 
        VALUES (
        %s,%s,%s,%s,
        %s,%s,%s,%s,
        %s,%s,%s,%s,%s,
        %s,%s,%s,%s)
        """
        try:
            self.cursor.execute(insertStr,(
                item['paperName'],item['paperAuthor'],item['domain'],item['paperIndustry'],
                item['paperDate'],item['authorOrg'],item['paperOrigin'],item['address'],
                item['ISBN'],item['tutor'],item['committee'],item['academicDegree'],item['language'],
                item['url'],item['remarks'],now,now
            ))
        except Exception as e:
            isSuccess = False
            self.connect.rollback()
            print("insert error ! ",e)
        finally:
            self.connect.commit()
            return isSuccess


if __name__ == "__main__":
    spider = ProQuestPaperSpider()
    spider.openDriver()
    # lagouSpider.driver.close()