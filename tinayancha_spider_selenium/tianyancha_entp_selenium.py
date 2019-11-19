# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tianyancha_entp_selenium
# Description:  
# Author:       forwork
# Date:         2019/7/12
#-------------------------------------------------------------------------------
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import random
import pymysql
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities

class TianyanchaSelenium(object):

    url = "https://www.tianyancha.com/company/3299810987"

    # def __init__(self):
    #     # 链接数据库
    #     self.connect = pymysql.connect(
    #         host='192.168.1.214',
    #         port=3306,
    #         db='forwork_ga',
    #         user='spider',
    #         passwd='123456',
    #         charset = "utf8")
    #     self.cursor = self.connect.cursor()

    # 打开浏览器
    def openDriver(self):
        proxy = Proxy({
            'ProxyType':ProxyType.MANUAL,
            'httpProxy':'119.130.106.54:3128'
        })
        # 新建一个期望技能
        desiredCapabilities = DesiredCapabilities.FIREFOX.copy()
        proxy.add_to_capabilities(desiredCapabilities)
        self.driver = webdriver.Firefox(executable_path="E:\\soft\\Firefox\\geckodriver.exe",desired_capabilities=desiredCapabilities)

        self.driver.get(self.url)
        self.driver.maximize_window()  # 将浏览器最大化
        time.sleep(random.randint(1, 4))
        self.parseEntp()

    # 登录
    # def login(self):
    #     try:
    #         self.driver.find_elements_by_link_text("登录/注册")[0].click()
    #     except Exception as e:
    #         print("出错啦：：",e)
    #         return
    #     time.sleep(random.randint(1,4))
    #     self.driver.find_element_by_xpath('//div[@class="login-warp"]/div[1]/div[3]/div[1]/div[2]').click()
    #
    #     input_user = self.driver.find_element_by_xpath(
    #         '//div[@class="login-warp"]/div[1]/div[3]/div[2]/div[2]/input')
    #     input_psw = self.driver.find_element_by_xpath(
    #         '//div[@class="login-warp"]/div[1]/div[3]/div[2]/div[3]/input')
    #     input_user.send_keys('18601240809')  # 发送登录账号
    #     input_psw.send_keys('tianyan123')  # 输入密码
    #
    #     time.sleep(random.randint(3, 6))  # 等待 一秒 方式被识别为机器人
    #     # login = self.wait.until(
    #     #     EC.element_to_be_clickable((By.XPATH, '//div[@class="login-warp"]/div[1]/div[3]/div[2]/div[5]')))
    #     self.driver.find_element_by_xpath('//div[@class="login-warp"]/div[1]/div[3]/div[2]/div[5]').click()
    #     time.sleep(8)
    #     self.cookies = self.driver.get_cookies()
    #     self.searchEntp()

    def parseEntp(self):
        self.driver.implicitly_wait(10)
        soup = BeautifulSoup(self.driver.page_source,"html.parser")
        item = {}
        mobile = ""
        email = ""
        businessStatus = ""
        registerCode = ""
        entpInfo = ""
        entpName = ""
        registerFund = ""
        website = ""
        address = ""
        legalPerson = ""
        foundDate = ""
        creditCode = ""
        orgCode = ""
        taxpayerCode = ""
        entpType = ""
        businessTerm = ""
        industry = ""
        personScope = ""
        registerOrg = ""
        registerAddr = ""
        businessScope = ""

        time.sleep(2)
        # try:
        #     closeButton = self.driver.find_elements_by_css_selector("#tyc_banner_close")
        #     closeButton[0].click()
        # except Exception as e:
        #     print("找不到底部banner关闭按钮！！")
        #     print(e)

        url = self.driver.current_url
        item['url'] = url
        div = soup.find("div", {"id": "company_web_top"})
        content = div.find("div", {"class": "-company-box"}).findAll("div", {"class": "content"})[1]

        try:
            entpName = content.find("div", {"class": "header"}).find("h1", {"class": "name"}).getText()
        except Exception as e:
            entpName = div.find("h1").getText()
            print(u"解析企业名称异常：：", e)

        item['entpName'] = entpName
        detail = content.find("div", {"class": "detail"})
        f0s = detail.findAll("div", {"class": "f0"})
        # 电话，邮箱
        try:
            blocks = f0s[0].findAll("div", {"class": "in-block"})
            lianxis = blocks[0].findAll("span")
            mobile = lianxis[1].getText()
            youxiangs = blocks[1].findAll("span")
            email = youxiangs[1].getText()
            if u'暂无信息' in mobile:
                mobile = ""
            if u'暂无信息' in email:
                email = ""
        except Exception as e:
            print(u"联想方式出错！！")

        item['mobile'] = mobile
        item['email'] = email
        try:
            block2s = f0s[1].findAll("div", {"class": "in-block"})
            website = ''
            if block2s[0].a != None:
                website = block2s[0].a.getText()
            address = block2s[1].find("div", {"class": "auto-folder"}).find("div").getText()
            if u'暂无信息' in address:
                address = ''
        except Exception as e:
            print(u"网站、地址出错！！",e)

        item['website'] = website
        item['address'] = address

        # 简介按钮
        try:
            entpInfoScript = self.driver.find_element_by_id("company_base_info_detail").text
            if None != entpInfoScript:
                entpInfo = entpInfoScript.strip()
            else:
                entpInfo = ""
        except Exception as e:
            entpInfo = ""
            print(u"企业详情介绍出错啦！！", e)

        item['entpInfo'] = entpInfo

        webDiv = soup.find("div", {"id": "web-content"})
        tables = webDiv.findAll("table", {"class": "table"})
        try:
            legalPersonDiv = tables[1].findAll("tr")[1].findAll("td")[0].a  # 企业法人
            legalPerson = ''
            if None != legalPersonDiv:
                legalPerson = legalPersonDiv.getText()
            if '-' in legalPerson:
                legalPerson = ''
        except Exception as e:
            print(u"企业法人出错",e)

        item['legalPerson'] = legalPerson

        trs = tables[2].findAll("tr")  # 长度11
        td0s = trs[0].findAll("td")
        try:
            registerFund = td0s[1].find("div").get("title")
            if '-' in registerFund:
                registerFund = ''
        except Exception as e:
            print(u"注册资金：：",e)

        try:
            td1s = trs[1].findAll("td")
            right_day = td1s[1].getText().strip()
            print(u"注册日期：：",right_day)
            if '-' == right_day:
                foundDate = ''
            else:
                if right_day.startswith("19") or right_day.startswith("20"):
                    foundDate = right_day
                else:
                    dates = right_day.split("-")
                    year = self.trans(dates[0])
                    month = self.trans(dates[1])
                    date = self.trans(dates[2])
                    foundDate = (year+"-"+month+"-"+date)

        except Exception as e:
            foundDate = ''
            print(u"注册时间：：",e)

        try:
            td1s = trs[1].findAll("td")
            businessStatus = td1s[3].getText()  # 经营状态
            if '-' in businessStatus:
                businessStatus = ""
        except Exception as e:
            print(u"经营状态::: ",e)

        try:
            td2s = trs[2].findAll("td")
            registerCode = td2s[3].getText()  # 工商注册号
            if "-" in registerCode:
                registerCode = ""
        except Exception as e:
            print(u"工商注册号：：",e)

        item['registerFund'] = registerFund
        item['foundDate'] = foundDate
        item['businessStatus'] = businessStatus
        item['registerCode'] = registerCode

        try:
            td2s = trs[2].findAll("td")
            creditCode = td2s[1].getText()  # 统一社会信用代码
            if '-' in creditCode:
                creditCode = ''

            td3s = trs[3].findAll("td")
            orgCode = td3s[3].getText()  # 组织机构代码
            if '-' in orgCode:
                orgCode = ''

            td3s = trs[3].findAll("td")
            taxpayerCode = td3s[1].getText()  # 纳税人识别号
            if '-' in taxpayerCode:
                taxpayerCode = ''

            td6s = trs[6].findAll("td")
            businessTerm = td6s[1].getText().strip()  # 营业期限
            if '-' == businessTerm:
                businessTerm = ''

            td4s = trs[4].findAll("td")
            entpType = td4s[1].getText().strip()  # 公司类型
            if '-' == entpType:
                entpType = ''

            industry = td4s[3].getText().strip()  # 行业
            if '-' in industry:
                industry = ''

        except Exception as e:
            print("352 line ::",e)

        item['creditCode'] = creditCode
        item['orgCode'] = orgCode
        item['taxpayerCode'] = taxpayerCode
        item['entpType'] = entpType
        item['businessTerm'] = businessTerm
        item['industry'] = industry
        try:
            td6s = trs[7].findAll("td")
            personScope = td6s[1].getText()
            if "-" in personScope:
                personScope = ""

            td7s = trs[5].findAll("td")
            registerOrg = td7s[3].getText()
            if '-' in registerOrg:
                registerOrg = ''

            td9s = trs[9].findAll("td")

            registerAddr = td9s[1].getText().replace(u"附近公司", "").strip()
            if '-' in registerAddr:
                registerAddr = ''
            td10s = trs[10].findAll("td")
            businessScope = td10s[1].getText()
            if '-' in businessScope:
                businessScope = ''
        except Exception as e:
            print(u"最后一个：：",e)

        item['personScope'] = personScope
        item['registerOrg'] = registerOrg
        item['registerAddr'] = registerAddr
        item['businessScope'] = businessScope
        print(item)

    # 将窗口转到详情页
    def switchEntpDetail(self):
        print(u"将窗口转到详情页")
        allhandles = self.driver.window_handles
        if len(allhandles) == 2:
            self.driver.switch_to.window(allhandles[1])
        elif len(allhandles) > 2:
            for hl in allhandles:
                if hl != allhandles[0] and hl != allhandles[-1]:
                    self.driver.switch_to.window(hl)
                    self.driver.close()
            self.driver.switch_to.window(allhandles[-1])

    # 将窗口转到列表页
    def switchSearchList(self):
        print(u"将窗口转到列表页")
        allhandles = self.driver.window_handles
        currentHandle = self.driver.current_window_handle
        for hl in allhandles:
            if hl != allhandles[0]:
                self.driver.switch_to.window(hl)
                self.driver.close()
        self.driver.switch_to.window(allhandles[0])


    # 字符转换
    def trans(self,A):
        num = []
        # 9521-29-91  2018-12-28
        # 9528-50-92  2019-03-21
        # 9520-57-51  2013-06-08
        # 9521-29-54  2018-12-05
        for i in range(0, len(A)):
            if A[i] == "0":
                zero = re.compile("0")
                z = re.sub(zero, "3", A[i])
                num.append(z)

            elif A[i] == "1":
                one = re.compile("1")
                o = re.sub(one, "8", A[i])
                # print(o,i)
                num.append(o)

            elif A[i] == "2":
                two = re.compile("2")
                t = re.sub(two, "1", A[i])
                # print(t,i)
                num.append(t)

            elif A[i] == "3":
                three = re.compile("3")
                t2 = re.sub(three, "7", A[i])
                # print(t2,i)
                num.append(t2)

            elif A[i] == "4":
                four = re.compile("4")
                f = re.sub(four, "5", A[i])
                # print(f,i)
                num.append(f)

            elif A[i] == "5":
                five = re.compile("5")
                f2 = re.sub(five, "0", A[i])
                # print(f2,i)
                num.append(f2)

            elif A[i] == "6":
                six = re.compile("6")
                s = re.sub(six, "4", A[i])
                # print(s,i)
                num.append(s)

            elif A[i] == "7":
                seven = re.compile("7")
                s2 = re.sub(seven, "6", A[i])
                # print(s2,i)
                num.append(s2)

            elif A[i] == "8":
                eight = re.compile("8")
                e = re.sub(eight, "9", A[i])
                # print(e,i)
                num.append(e)

            elif A[i] == "9":
                nine = re.compile("9")
                n = re.sub(nine, "2", A[i])
                # print(n,i)
                num.append(n)
        number = ''.join(num)
        return number

if __name__ == "__main__":
    tianyancha = TianyanchaSelenium()
    tianyancha.openDriver()
    tianyancha.driver.quit()
