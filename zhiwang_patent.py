# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         zhiwang_patent
# Description:  这个项目主要功能是采集知网专利网站的数据
# Author:       eleven
# Date:         2019/6/20
#-------------------------------------------------------------------------------
import time
import MySQLdb
import selenium.webdriver as webdriver
from selenium.webdriver import Proxy, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import logging

class Zhiwang_patent(object):

    firefoxPath = "D:\\software\\Firefox\\geckodriver.exe"
    chromePath = "C:\\Program Files (x86)\\Google\Chrome\\Application\\chromedriver.exe"
    searchUrl = "http://kns.cnki.net/KNS/brief/result.aspx?dbPrefix=SCOD"

    realUrl ="http://kns.cnki.net/KNS/brief/brief.aspx?pagename=ASP.brief_result_aspx&isinEn=0&dbPrefix=SCPD&dbCatalog=%e4%b8%ad%e5%9b%bd%e4%b8%93%e5%88%a9%e6%95%b0%e6%8d%ae%e5%ba%93&ConfigFile=SCPD.xml&research=off&t={}&keyValue=&S=1&sorttype="

    searchKey = "SU=5G OR TI=5G OR KY=5G"
    domain = "5G"
    # SU=主题,TI=专利名称,KY=关键词,AB=摘要,FT=全文,SQH=申请号,GKH=公开号,
    # CLC=专利分类号,CLZ=主分类号,SQR=申请人,FMR=发明人,
    # DZ=地址,SDF=专利代理机构,DLR=代理人,YXQ=优先权,GDM=国省代码,GMC=国省名称
    domains = [
        "5G",
        "大数据",
        "人工智能",
        "物联网",
        "云计算",
        "云制造",
        "区块链",
        "新能源",
        "机械制造",
        "材料科学",
        "节能环保",
        "电子信息",
        "化学化工"]

    def __init__(self):
        self.conne = MySQLdb.connect(host="127.0.0.1",db="kexuejia",port=3306,user="root",passwd="root",charset="utf8")
        self.curse = self.conne.cursor()

    def openDriver(self):

        # Proxy是代理类，初始化参数是一个字典包含多个参数
        # myProxy = "182.138.242.128:8118"
        # myProxy = "182.108.47.231:808"
        # myProxy = "113.140.1.82:53281"

        # myProxy = "47.94.135.32:8118"
        myProxy = "120.83.106.27:9999"
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy,
            'ftpProxy': myProxy,
            'sslProxy': myProxy
        })

        # executable_path="chromedriver",  浏览器驱动路径
        # port=0,                          端口
        # options=None,                    选项
        # service_args=None,               要传递给驱动程序服务的参数列表
        # desired_capabilities=None,       渴望能力，浏览器的Dictionary对象，仅限于“代理”或“日志记录首选项”等功能。
        # service_log_path=None,           日志信息路径
        # chrome_options=None,
        # keep_alive=True
        myCapabilities = DesiredCapabilities.CHROME.copy()  # 创建自己的期望
        proxy.add_to_capabilities(myCapabilities)           # 将代理加入到期望值中
        self.driver = webdriver.Chrome(executable_path=self.chromePath,desired_capabilities=myCapabilities)
        # self.driver = webdriver.Chrome(executable_path=self.chromePath)
        # self.driver = webdriver.Firefox(executable_path=self.firefoxPath)
        self.driver.maximize_window()
        self.driver.get(self.searchUrl)

        try:
            self.driver.implicitly_wait(10)
        except Exception as e:
            print(e)

        tabLi = self.driver.find_element_by_id("1_3")
        if None != tabLi:
            tabA = tabLi.find_element(By.TAG_NAME,"a")
            if None != tabA:
                tabA.click()
                try:
                    self.driver.implicitly_wait(10)
                except Exception as e:
                    print(e)
                self.listSearch()
        else:
            print("没有点击 专业检索！")

    def listSearch(self):
        searchTextarea = self.driver.find_element_by_id("expertvalue")
        if None != searchTextarea:
            searchTextarea.send_keys(self.searchKey)
        btnSearch = self.driver.find_element_by_id("btnSearch")
        if None != btnSearch:
            btnSearch.click()
            self.driver.implicitly_wait(10)
            time.sleep(10)
            timestamp = str(int(round(time.time() * 1000)))
            realUrl = self.realUrl.format(timestamp)
            self.driver.get(realUrl)
            self.driver.implicitly_wait(10)

            self.parseList()

    def parseList(self):

        contentTable = self.driver.find_element_by_class_name("GridTableContent")
        if None != contentTable:
            conTrs = contentTable.find_elements_by_tag_name("tr")
            if None != conTrs:
                for i in range(1,len(conTrs)):
                    conTds = conTrs[i].find_elements_by_tag_name("td")
                    if None != conTds:
                        condA = conTds[1].find_element_by_tag_name("a")
                        if None != condA:
                            # 点击超链接
                            condA.click()
                            self.driver.implicitly_wait(10)
                            self.parseDetail()

            #   键盘的 左右箭头可以控制上一页下一页
            footTag = self.driver.find_element_by_class_name("TitleLeftCell")
            if None != footTag:
                nextButton = footTag.find_element_by_link_text("下一页")
                if None != nextButton:
                    nextButton.click()
                    self.driver.implicitly_wait(10)
                    self.switchToList()
                    self.parseList()


    def parseDetail(self):
        self.driver.implicitly_wait(10)
        self.switchToDetail()
        patentNo = ''
        patentName = ''
        applyNo = ''
        applyDate = ''
        patentDate = ''
        ipcNo = ''
        patentOwner = ''
        inventor = ''
        applyAddress = ''
        cpcNo = ''
        proxy = ''
        proxyOrg = ''
        summary = ''
        content = ''
        domain = self.domain

        item = {}

        tables = self.driver.find_elements_by_tag_name("table")
        try:
            patentName = tables[0].find_elements_by_tag_name("tr")[0].find_elements_by_tag_name("td")[1].text.strip()
        except Exception as e:
            print(e)

        if len(tables)>3:
            titleTable = tables[3]
            patentName = titleTable.find_elements_by_tag_name("tr")[0].text.strip()
            contentTable = tables[4]
            # 带上隐藏的总共有16行
            ctrs = contentTable.find_elements_by_tag_name("tr")
            # if len(ctrs)==16:
            td1s = ctrs[0].find_elements_by_tag_name("td")
            if len(td1s)==4:
                applyNo  = td1s[1].text.strip()  # 申请号
                applyDate  = td1s[3].text.strip()  # 申请号

            td2s = ctrs[1].find_elements_by_tag_name("td")
            if len(td2s)==4:
                patentNo = td2s[1].text.strip() # 公开号
                patentDate = td2s[3].text.strip() # 公开日

            td3s = ctrs[2].find_elements_by_tag_name("td")
            if len(td3s)==4:
                patentOwner = td3s[1].text.strip() # 申请人
                applyAddress = td3s[3].text.strip() # 地址

            td5s = ctrs[4].find_elements_by_tag_name("td")
            if len(td5s) == 2:
                inventor = td5s[1].text.strip()  # 发明人

            td7s = ctrs[7].find_elements_by_tag_name("td")
            if len(td7s) == 4:
                proxy = td7s[1].text.strip()  # 代理
                proxyOrg = td7s[3].text.strip()  # 代理机构

            td10s = ctrs[10].find_elements_by_tag_name("td")
            if len(td10s) == 2:
                summary = td10s[1].text.strip()  # 摘要

            td11s = ctrs[11].find_elements_by_tag_name("td")
            if len(td11s) == 2:
                content = td11s[1].text.strip()  # 主权项

            td15s = ctrs[14].find_elements_by_tag_name("td")
            if len(td15s) == 2:
                cpcNo = td15s[1].text.strip()  # cpc分类号
            # else:
            #     print("不知道发生了什么::")
            #     print(contentTable.text)

        item['patentNo'] = patentNo
        item['patentName'] = patentName
        item['applyNo'] = applyNo
        item['applyDate'] = applyDate
        item['patentDate'] = patentDate
        item['ipcNo'] = ipcNo
        item['patentOwner'] = patentOwner
        item['inventor'] = inventor
        item['applyAddress'] = applyAddress
        item['cpcNo'] = cpcNo
        item['proxy'] = proxy
        item['proxyOrg'] = proxyOrg
        item['summary'] = summary
        item['content'] = content
        item['domain'] = domain
        print item
        self.save(item)
        self.switchToList()

    def switchToDetail(self):
        allHandles = self.driver.window_handles
        myHandle = self.driver.current_url
        # 如果当前的窗口超过两个，关闭除第一个和最后一个窗口
        if len(allHandles)>2:
            for i in range(1,len(allHandles)-2):
                self.driver.switch_to.window(allHandles[i])
                self.driver.close()
        # 如果当前不在最后一个窗口，切换至最后一个窗口
        if myHandle != allHandles[-1]:
            self.driver.switch_to.window(allHandles[-1])

    def switchToList(self):
        allHandles = self.driver.window_handles
        myHandle = self.driver.current_url
        if myHandle != allHandles[0]:
            self.driver.close()
            self.driver.switch_to.window(allHandles[0])

    def save(self,item):
        sqlStr = """
            INSERT INTO `zhiwang_patent`(`apply_no`, `apply_date`, `patent_no`, `patent_date`, 
              `ipc_no`, `patent_owner`, `inventor`, `porxy`, `porxy_org`,`patent_name`, 
              `apply_address`, `cpc_no`, `summary`, `content`, `domain`)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(sqlStr,(
                    item['applyNo'],
                    item['applyDate'],
                    item['patentNo'],
                    item['patentDate'],
                    item['ipcNo'],
                    item['patentOwner'],
                    item['inventor'],
                    item['porxy'],
                    item['porxyOrg'],
                    item['patentName'],
                    item['applyAddress'],
                    item['cpcNo'],
                    item['summary'],
                    item['content'],
                    item['domain']
                ))
            self.conne.commit()
        except Exception as e:
            logging.error("数据保存出错！！")
            print(e)


if __name__ == "__main__":
    spider = Zhiwang_patent()
    spider.openDriver()






