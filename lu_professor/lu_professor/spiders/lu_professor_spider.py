# -*- coding: utf-8 -*-
import scrapy
import selenium.webdriver as webdriver
import time
import json

class LuProfessorSpiderSpider(scrapy.Spider):
    name = 'lu_professor_spider'
    # allowed_domains = ['http://www.qiyekexie.com']
    firePath = "D:\\software\\Firefox\\geckodriver.exe"
    chromePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
    loginUrl = "http://www.qiyekexie.com/portal/zkx/3/login/login.action"

    # 专家列表API
    list_api = 'http://www.qiyekexie.com/expert/publicList.do'
    # 专家列表url
    list_url = "http://www.qiyekexie.com/portal/zkx/6/expert/expertList.action"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "100",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.qiyekexie.com",
        "Origin": "http://www.qiyekexie.com",
        "Referer": "http://www.qiyekexie.com/portal/zkx/6/expert/expertList.action",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }

    list_params ={
        "pageNumber":"2",
        "keyword":"",
        "code":"210000",
        "status":"2",
        "pageSize":"9",
        "provinceCode":"0",
        "cityCode":"0"
    }

    def openDriver(self):
        self.driver = webdriver.Firefox(executable_path=self.firePath)
        self.driver.maximize_window()
        self.driver.get(self.loginUrl)
        self.driver.implicitly_wait(10)
        usernameInput = self.driver.find_element_by_id("username")
        passwdInput = self.driver.find_element_by_id("password")
        submitButton = self.driver.find_element_by_id("loginSubmit")
        usernameInput.send_keys("whcl2019")
        time.sleep(3)
        passwdInput.send_keys("yiziwang")
        time.sleep(3)
        submitButton.click()
        self.parseLoginCookies()

    def parseLoginCookies(self):
        cookiesq = self.driver.get_cookies()
        self.cookiesStr = self.listToStr(cookiesq)
        self.cookiesDict = self.listToDict(cookiesq)

    def listToStr(self, cookie):
        itemStr = ""
        for item in cookie:
            name = item['name'].encode("utf-8")
            value = item['value'].encode("utf-8")
            itemStr += (name+"="+value+"; ")
        return itemStr

    def listToDict(self,cookie):
        itemDict = {}
        for item in cookie:
            name = item['name'].encode("utf-8")
            value = item['value'].encode("utf-8")
            itemDict.update({name:value})
        return itemDict

    def start_requests(self):
        self.openDriver()
        self.driver.quit()
        time.sleep(3)
        print(self.cookiesStr)
        print(self.cookiesDict)
        self.headers.update({"Cookie":self.cookiesStr})
        # yield scrapy.FormRequest(method="POST",formdata=self.list_params,url=self.list_api,
        #                          headers=self.headers,callback=self.parseList,cookies=self.cookiesDict,
        #                          dont_filter=True)
        yield scrapy.Request(url=self.list_url,method="GET",headers=self.headers,cookies=self.cookiesDict,
                             callback=self.parseList)

    def parseList(self,reponse):
        """"
        {"pageNumber":"3","keyword":"",
        "code":"210000","status":2,"pageSize":9,
        "provinceCode":"0","cityCode":"0"}
        """
        print(reponse.text)

