# coding=utf-8

# Please refer to the documentation for information on how to create and manage
# your spiders.
import requests
import selenium.webdriver as webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.firefox_profile import ProxyType
from selenium.webdriver.common.proxy import *
import time
import MySQLdb

class Lu_professor_selenium(object):
    domaina = '综合'

    firePath = "D:\\software\\Firefox\\geckodriver.exe"
    chromePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
    loginUrl = "http://www.qiyekexie.com/portal/zkx/3/login/login.action"

    # 专家列表API
    list_api = 'http://www.qiyekexie.com/expert/publicList.do'
    # 专家列表url
    list_url = "http://www.qiyekexie.com/portal/zkx/6/expert/expertList.action"

    def __init__(self):
        self.connect = MySQLdb.connect(host="127.0.0.1",port=3306,db="lupingtai",user="root",passwd="root",charset="utf8")
        self.cursor = self.connect.cursor()

    def openDriver(self):
        # myProxy = "124.232.133.199:3128"
        # myProxy = "113.64.146.126:8118"
        # myProxy = "47.100.103.71:80"

        # myProxy = "182.92.219.211:80"
        myProxy = "119.191.79.46:80"

        proxy = Proxy({
            "proxyType":ProxyType.MANUAL,
            'httpProxy': myProxy,
            'ftpProxy': myProxy,
            'sslProxy': myProxy,
            'noProxy': ''
        })
        # 新建一个“期望技能”，哈哈
        desired_capabilities = DesiredCapabilities.FIREFOX.copy()
        # # 把代理ip加入到技能中
        proxy.add_to_capabilities(desired_capabilities)

        self.driver = webdriver.Firefox(executable_path=self.firePath,proxy=proxy)

        self.driver.maximize_window()
        # self.driver.get(self.loginUrl)
        # self.driver.implicitly_wait(10)
        # usernameInput = self.driver.find_element_by_id("username")
        # passwdInput = self.driver.find_element_by_id("password")
        # submitButton = self.driver.find_element_by_id("loginSubmit")
        # usernameInput.send_keys("whcl2019")
        # time.sleep(3)
        # passwdInput.send_keys("yiziwang")
        # time.sleep(3)
        # submitButton.click()
        self.driver.implicitly_wait(10)
        self.driver.get(self.list_url)
        time.sleep(20)
        self.parseList()

    def parseList(self):
        try:
            locator = (By.ID, "expertList")
            WebDriverWait(driver=self.driver, timeout=10, poll_frequency=0.5).until(
                expected_conditions.presence_of_element_located(locator))
        except Exception as e:
            print(e)
        listDiv = self.driver.find_element_by_id("expertList")
        lis = listDiv.find_elements_by_tag_name("li")
        if None != lis:
            for li in lis:
                try:
                    aL = li.find_element(By.TAG_NAME, "a")
                    self.driver.execute_script("arguments[0].scrollIntoView(false);", aL)
                    a = li.find_element_by_tag_name("a")
                    if None != a:
                        a.click()
                        self.driver.implicitly_wait(10)
                        time.sleep(6)
                        self.parseDetail()
                except Exception as e:
                    print(e)

        nextDiv = self.driver.find_element_by_class_name("new_pagediv")
        if None != nextDiv:
            nextBtn = nextDiv.find_element_by_class_name("nextbtn")
            if None != nextBtn:
                nextbtnLo = nextDiv.find_element(By.CLASS_NAME, "nextbtn")
                self.driver.execute_script("arguments[0].scrollIntoView();", nextbtnLo)
                nextBtn.click()
                self.driver.implicitly_wait(10)
                self.parseList()

    def parseDetail(self):
        # 将句柄转换到详情页
        self.switchToDetail()
        item = {}
        name = ""
        company = ""
        domain = ""
        title = ""
        position = ""
        introduction = ""
        summary = ""
        address = ""
        speciality = ""
        achievement = ""
        antecedent = ""
        award = ""
        other = ""
        WebDriverWait(driver=self.driver, timeout=10, poll_frequency=0.5).until(
            expected_conditions.presence_of_element_located((By.ID, "expertName")))
        expertNameDiv = self.driver.find_element_by_id("expertName")
        if None != expertNameDiv:  name = expertNameDiv.text

        industryDiv = self.driver.find_element_by_id("industry")
        if None != industryDiv:  domain = industryDiv.text

        expertCompanyDiv = self.driver.find_element_by_id("expertCompany")
        if None != expertCompanyDiv:  company = expertCompanyDiv.text

        titleDiv = self.driver.find_element_by_id("title")
        if None != titleDiv:  title = titleDiv.text

        positionDiv = self.driver.find_element_by_id("expertDuties")
        if None != positionDiv:  position = positionDiv.text

        addressDiv = self.driver.find_element_by_id("expertAddress")
        if None != addressDiv:  address = addressDiv.text

        detailDiv = self.driver.find_element_by_class_name("qykx-detail-column")
        if None != detailDiv:
            introduction = detailDiv.text.replace(u"个人简介", "")
            intro1Div = detailDiv.find_element_by_id("intro1")
            if None != intro1Div:
                summaryDiv = intro1Div.find_element_by_id("expertSummary")
                if None != summaryDiv:
                    summary = summaryDiv.text.strip()

                achievementDiv = intro1Div.find_element_by_id("achievement")
                if None != achievementDiv:
                    achievement = achievementDiv.text.strip()

            intro2Div = detailDiv.find_element_by_id("intro2")
            if None != intro2Div:
                specialityDiv = intro2Div.find_element_by_id("expertSpeciality")
                if None != specialityDiv:
                    speciality = specialityDiv.text.strip()

                achievementsDiv = intro2Div.find_element_by_id("expertAchievements")
                if None != achievementsDiv:
                    achievement = (achievement + achievementsDiv.text.strip())

                antecedentsDiv = intro2Div.find_element_by_id("expertAntecedents")
                if None != antecedentsDiv:
                    antecedent = antecedentsDiv.text.strip()

                AwardsDiv = intro2Div.find_element_by_id("expertAwards")
                if None != AwardsDiv:
                    award = AwardsDiv.text.strip()

                othersDiv = intro2Div.find_element_by_id("expertOthers")
                if None != othersDiv:
                    other = othersDiv.text.strip()

        item['name'] = name
        item['domain'] = (self.domaina if domain == '' else domain)
        item['company'] = company
        item['title'] = title
        item['position'] = position
        item['introduction'] = introduction
        item['summary'] = summary
        item['address'] = address
        item['speciality'] = speciality
        item['achievement'] = achievement
        item['antecedent'] = antecedent
        item['award'] = award
        item['other'] = other
        self.saveToDB(item)
        self.switchToList()

    def switchToDetail(self):
        allHandles = self.driver.window_handles
        myHandle = self.driver.current_url
        # 如果当前的窗口超过两个，关闭除第一个和最后一个窗口
        if len(allHandles) > 2:
            for i in range(1, len(allHandles) - 2):
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

    def saveToDB(self, item):
        print item.keys()
        strSql = """
            INSERT INTO lp_professor
            (`name`, `domain`,  `address`, `title`, 
            `position`, `introduction`,`company`,  `summary`, 
            `achievement`, `speciality`, `antecedent`, `award`,`other`) 
            VALUES 
            (%s,%s,%s,%s,
            %s,%s,%s,%s,
            %s,%s,%s,%s,%s);
        """
        self.cursor.execute(strSql,(
            item['name'],
            item['domain'],
            item['address'],
            item['title'],
            item['position'],
            item['introduction'],
            item['company'],
            item['summary'],
            item['achievement'],
            item['speciality'],
            item['antecedent'],
            item['award'],
            item['other']
        ))
        self.connect.commit()


if __name__ == "__main__":
    spider = Lu_professor_selenium()
    spider.openDriver()
    spider.connect.close()
    spider.driver.quit()
