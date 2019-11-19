# _*_ coding=utf-8 _*_

import pymysql
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import By
from selenium.webdriver import DesiredCapabilities     # 期待性能
from selenium.webdriver.common.proxy import ProxyType,Proxy
from spider_util.dateFormatUtil import DateFormatUtil
from spider_util.rollElementUtil import RollElementUtil
from spider_util.handlesManage import HandlesManage
import random


class BossEntpPostSpider(object):

    fireFoxPath = "D:\\software\\Firefox\\geckodriver.exe"
    bossHost = "https://www.zhipin.com"

    def __init__(self):
        self.connect = pymysql.connect(host="192.168.1.214", port=3306, user="developer", password="123123",db="forwork_shanxi_ga", charset="utf8")
        self.cursor = self.connect.cursor()
        result = self.getBossFirstUrl()
        self.urlItem = {}
        if None != result:
            self.urlItem['id'] = result[0]
            self.urlItem['city'] = result[1]
            self.urlItem['area'] = result[2]
            self.urlItem['domain'] = result[3]
            self.urlItem['industry'] = result[4]
            self.urlItem['url'] = result[5]
            self.urlItem['urlType'] = result[6]
        self.rollElementUtil = RollElementUtil()
        self.handlesManage = HandlesManage()
        self.dateFormatUtil = DateFormatUtil()

    def openDriver(self):
        proxy = Proxy({
            "proxyType":ProxyType.MANUAL,
            "httpProxy":"116.62.190.100:3128"
        })

        # 创建一个期望技能
        dc = DesiredCapabilities.FIREFOX.copy()
        proxy.add_to_capabilities(dc)
        self.driver = webdriver.Firefox(executable_path=self.fireFoxPath,desired_capabilities=dc)
        # self.driver = webdriver.Firefox(executable_path=self.fireFoxPath)
        self.driver.get(self.bossHost)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        time.sleep(random.randint(2,4))
        self.driver.get(self.urlItem['url'])
        self.parseSearchPage()

    # 搜索页面解析
    def parseSearchPage(self):
        try:
            WebDriverWait(self.driver,10,0.5).until(EC.element_located_to_be_selected((By.ID,"main")))
        except:
            print("搜索页面解析等待！")

        try:
            mainDiv = self.driver.find_element_by_id("main")
            if None != mainDiv:
                jobListDiv = mainDiv.find_element_by_class_name("job-list")
                if None != jobListDiv:
                    jobLis = jobListDiv.find_elements_by_tag_name("li")
                    if len(jobLis)>0:
                        for li in jobLis:
                            companyName = li.find_element_by_class_name("job-title")
                            try:
                                self.rollElementUtil.rollToView_bottom(self.driver,companyName)
                                companyName.click()
                            except Exception as e:
                                self.rollElementUtil.rollToView_top(self.driver, companyName)
                                companyName.click()
                                print(e)
                            time.sleep(random.randint(3,4))
                            self.handlesManage.switch_SearchPage_To_EntpPage(self.driver)
                            self.parseEntp()
        except Exception as e:
            print(e)

        try:
            pageDiv = self.driver.find_element_by_class_name("page")
            if None != pageDiv:
                nextBtn = pageDiv.find_element_by_class_name("next")
                if None != nextBtn:
                    try:
                        self.rollElementUtil.rollToView_bottom(self.driver,nextBtn)
                        nextBtn.click()
                    except Exception as e:
                        self.rollElementUtil.rollToView_bottom(self.driver,nextBtn)
                        nextBtn.click()
                        print(e)
                    self.parseSearchPage()
        except Exception as e:
            print(e)

    # 企业页面分析
    def parseEntp(self):
        print("进入企业解析页面：",self.driver.current_url)
        try:
            WebDriverWait(driver=self.driver,timeout=10,poll_frequency=0.5).until(EC.element_located_to_be_selected((By.CLASS_NAME,"info")))
        except Exception as e:
            print("企业页面分析等待！",e)
        entpItem = {}
        entpName = ""
        url = self.driver.current_url
        address = ""
        entpInfo = ""
        registerFund = ""
        foundDate = ""
        entpType = ""
        highlight = ""
        industry = self.urlItem['industry']
        businessScope = ""
        personScope = ""
        recordStatus = "0"
        city = self.urlItem['city']
        domain = self.urlItem['domain']
        legalPerson = ""
        creditCode = ""
        area = self.urlItem['area']
        dataFrom = "4"
        businessStatus = ""
        registerAddr = ""
        entpId = None
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        try:
            companyTab = self.driver.find_element_by_class_name("company-tab")
            print(companyTab.text)
        except Exception as e:
            print("职位列表点击：",e)

        try:
            comanyBusinessDiv = self.driver.find_element_by_class_name("company-business")
            h4 = comanyBusinessDiv.find_element_by_tag_name("h4")
            surplusStr = h4.find_element_by_tag_name("span").text
            entpName = h4.text.replace(surplusStr,"").strip()
            entpResult = self.existEntpFromDB(entpName)
            if None != entpResult:
                # 数据库中已经有该企业
                entpId = entpResult[0]
            else:
                try:
                    # 数据库中没有该企业 label
                    businessDiv = comanyBusinessDiv.find_element_by_class_name("business-detail")
                    moreBtn = businessDiv.find_element_by_tag_name("label").find_element_by_tag_name("i")
                    self.rollElementUtil.rollToView_bottom(self.driver,moreBtn)
                    try:
                        self.rollElementUtil.rollToView_bottom(self.driver,moreBtn)
                        moreBtn.click()
                    except Exception as e:
                        self.rollElementUtil.rollToView_bottom(self.driver, moreBtn)
                        moreBtn.click()
                        print("工商信息全部点击：：",e)
                    companyInfoLis = comanyBusinessDiv.find_elements_by_tag_name("li")
                    legalPerson = self.getLiFile(companyInfoLis[0])
                    registerFund = self.getLiFile(companyInfoLis[1])
                    foundDate = self.getLiFile(companyInfoLis[2])
                    entpType = self.getLiFile(companyInfoLis[3])
                    businessStatus = self.getLiFile(companyInfoLis[4])
                    registerAddr = self.getLiFile(companyInfoLis[5])
                    creditCode = self.getLiFile(companyInfoLis[6])
                    businessScope = self.getLiFile(companyInfoLis[7])
                except Exception as a:
                    print("企业工商基本信息报错：",a)
        except Exception as b:
            print("企业信息验证机采集：",b)

        try:
            addressDiv = self.driver.find_element_by_class_name("location-address")
            address = addressDiv.text.replace(" ","")
        except Exception as c:
            print("企业地址报错：",c)
        try:
            infoDiv = soup.find(attrs={"class":"info"})
            infoP = infoDiv.find("p")
            personScope = str(infoP.next.next.next)
        except Exception as d:
            print("企业人员规模报错：",d)

        try:
            HightDiv = soup.find("div",{"class":"info"})
            jobTagsDiv = HightDiv.find("div",{"class":"job-tags"})
            tagLis = jobTagsDiv.findAll("span")
            for job in tagLis:
                highlight = highlight + "," + job.getText()
            highlight = highlight[1:]
        except Exception as e:
            print("企业亮点：",e)

        try:
            detailDiv = self.driver.find_element_by_class_name("detail-content")
            entpInfo = detailDiv.find_element_by_css_selector(".text.fold-text").text.replace("\n展开","").replace("公司简介\n","")
        except Exception as f:
            print("企业详细介绍：",f)

        entpItem['entpName'] = entpName
        entpItem['url'] = url
        entpItem['address'] = address
        entpItem['entpInfo'] = entpInfo
        entpItem['registerFund'] = registerFund
        entpItem['foundDate'] = foundDate
        entpItem['entpType'] = entpType
        entpItem['highlight'] = highlight
        entpItem['industry'] = industry
        entpItem['businessScope'] = businessScope
        entpItem['personScope'] = personScope
        entpItem['recordStatus'] = recordStatus
        entpItem['city'] = city
        entpItem['domain'] = domain
        entpItem['legalPerson'] = legalPerson
        entpItem['creditCode'] = creditCode
        entpItem['area'] = area
        entpItem['dataFrom'] = dataFrom
        entpItem['businessStatus'] = businessStatus
        entpItem['registerAddr'] = registerAddr
        result = self.existEntpFromDB(entpName=entpName)
        if None != result:
            entpId = result[0]
        else:
            self.saveEntp(entpItem)
            result = self.existEntpFromDB(entpName=entpName)
            entpId = result[0]
        try:
            bannerDiv = self.driver.find_element_by_css_selector(".company-banner")
            tabDiv = bannerDiv.find_element_by_css_selector(".inner.home-inner")
            tags = tabDiv.find_elements_by_tag_name("a")
            tags[-1].click()
            try:
                self.rollElementUtil.rollToView_bottom(self.driver, tags[-1])
                tags[-1].click()
            except Exception as g:
                self.rollElementUtil.rollToView_top(self.driver, tags[-1])
                tags[-1].click()
                print("职位列表点击：", g)

            time.sleep(random.randint(2, 3))
            self.parsePostList(entpId, entpName)

        except Exception as e:
            print("职位列表点击：",e)

    # 职位列表解析
    def parsePostList(self,entpId,entpName):
        try:
            WebDriverWait(driver=self.driver,timeout=10,poll_frequency=0.5).until(EC.presence_of_element_located((By.CLASS_NAME,"job-primary")))
        except Exception as e:
            print("职位详情页面等待：",e)
        try:
            jobListDiv = self.driver.find_element_by_class_name("job-list")
            if None != jobListDiv:
                jobLis = jobListDiv.find_elements_by_tag_name("li")
                if None != jobLis:
                    for job in jobLis:
                        jobA = job.find_element_by_tag_name("a")
                        try:
                            self.rollElementUtil.rollToView_bottom(self.driver, jobA)
                            jobA.click()
                        except Exception as g:
                            self.rollElementUtil.rollToView_top(self.driver, jobA)
                            jobA.click()
                        time.sleep(random.randint(2, 3))
                        self.handlesManage.switch_Entp_To_Post(self.driver)
                        self.parsePost(entpId,entpName)
                    try:
                        pageDiv = jobListDiv.find_element_by_class_name("page")
                        nextBtn = pageDiv.find_element_by_class_name("next")
                        if nextBtn.is_enabled():
                            try:
                                self.rollElementUtil.rollToView_bottom(self.driver, nextBtn)
                                nextBtn.click()
                            except Exception as g:
                                self.rollElementUtil.rollToView_top(self.driver, nextBtn)
                                nextBtn.click()
                            time.sleep(random.randint(2, 3))
                            self.parsePostList(entpId,entpName)
                        else:
                            self.handlesManage.switch_entp_to_searchPage(self.driver)
                    except Exception as e:
                        print("职位列表下一页报错： ", e)
        except Exception as e:
            print(e)

    # 企业信息存入数据库
    def saveEntp(self, entpItem):
        print("企业添加：：", entpItem)
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sqlStr = """
        INSERT INTO `forwork_shanxi_ga`.`zhilian_entp`
        (`entp_name`, `url`,`address`, `entp_info`, `entp_type`,
        `industry`,  `person_scope`, `domain`, `record_status`, `highlight`, 
        `city`, `area`, `create_time`, `update_time`,`data_from`) 
        VALUES (%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(sqlStr, (
                entpItem['entpName'], entpItem['url'],  entpItem['address'],
                entpItem['entpInfo'], entpItem['entpType'],
                entpItem['industry'], entpItem['personScope'], entpItem['domain'], '0',entpItem['highlight'],
                entpItem['city'], entpItem['area'], now, now, '4'
            ))

        except Exception as e:
            self.connect.rollback()
            print("添加企业数据出错：", e)
        finally:
            self.connect.commit()

    def parsePost(self,entpId,entpName):
        try:
            WebDriverWait(driver=self.driver,timeout=10,poll_frequency=0.5).until(EC.presence_of_element_located((By.ID,"main")))
        except Exception as e:
            print("职位详情页面等待：",e)
        now = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        postName = ""
        salary = ""
        address = ""
        replaceTime = now
        city = ""
        area = ""
        workExp = ""
        education = ""
        postNum = random.randint(2,8)
        postHighlights = ""
        postType = "全职"
        postDesc = ""

        soup = BeautifulSoup(self.driver.page_source,"html.parser")
        jobBanner = soup.find("div",{"class":"job-banner"})
        if None != jobBanner:
            jobInfo = jobBanner.find("div",{"class":"info-primary"})
            jobNameDiv = jobInfo.find(attrs={"class":"name"})
            postName = jobNameDiv.find("h1").getText().strip()
            salary = jobNameDiv.find("span",{"class":"salary"}).getText().strip()
            city = str(jobNameDiv.find("p").next)
            workExp = str(jobNameDiv.find("p").next.next.next)
            education = str(jobNameDiv.find("p").next.next.next.next.next)
            tags = jobNameDiv.find("div",{"class":"job-tags"}).findAll("span")
            for tg in tags:
                postHighlights = postHighlights + ","+tg.getText()
            postHighlights = postHighlights[1:]

        detailContenDiv = soup.find("div",{"class":"detail-content"})
        if None != detailContenDiv:
            jobSecDiv = detailContenDiv.find("div",{"class":"job-sec"})
            if None != jobSecDiv:
                postDesc = jobSecDiv.find("div",{"class":"text"}).getText()
        address = detailContenDiv.find("div",{"class":"location-address"}).getText()

        postItem = {}
        postItem['entpId'] = entpId
        postItem['entpName'] = entpName
        postItem['salary'] = salary
        postItem['address'] = address
        postItem['postName'] = postName
        postItem['postNum'] = postNum
        postItem['city'] = city
        postItem['area'] = area
        postItem['workExp'] = workExp
        postItem['education'] = education
        postItem['postHighlights'] = postHighlights
        postItem['postDesc'] = postDesc
        postItem['replaceTime'] = replaceTime
        postItem['postType'] = postType
        postItem['dataFrom'] = "4"
        postItem['createTime'] = now
        postItem['updateTime'] = now
        postItem['recordStatus'] = "0"
        print(postItem)
        # self.savePost(postItem)

    def savePost(self,postItem):
        print("职位添加：：",postItem)
        saveStr = """
            INSERT INTO `forwork_shanxi_ga`.`zhilian_entp_post`
            (`entp_id`, `entp_name`, `post_name`, `salary`, `area`, `post_type`, `city`, `work_exp`, 
            `education`, `post_num`, `post_highlights`, `post_desc`,`replace_time`,
            `address`,`record_status`,`create_time`, `update_time`,`data_from`) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(saveStr,(
                postItem['entpId'], postItem['entpName'], postItem['postName'], postItem['salary'],
                postItem['area'], postItem['postType'], postItem['city'],
                postItem['workExp'],
                postItem['education'], postItem['postNum'], postItem['postHighlights'], postItem['postDesc'],
                postItem['replaceTime'],
                postItem['address'], postItem['recordStatus'], postItem['createTime'], postItem['updateTime'], postItem['dataFrom']
            ))
        except Exception as e:
            self.connect.rollback()
            print(e)
        finally:
            self.connect.commit()

    def getBossFirstUrl(self):
        strSql = "SELECT * FROM `forwork_shanxi_ga`.boss_stay_url WHERE record_state = '1' LIMIT 1;"
        result = None
        try:
            self.cursor.execute(strSql)
            result = self.cursor.fetchone()
        except:
            print("获取url失败！")
        return result

    def existEntpFromDB(self,entpName):
        strSql = "SELECT id,city,area,`domain`,industry FROM `forwork_shanxi_ga`.zhilian_entp WHERE entp_name ='"+entpName+"'"
        result = None
        try:
            self.cursor.execute(strSql)
            result = self.cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            return result

    def getLiFile(self,liElement):
        fileValue = ""
        fullStr = liElement.text
        surplusStr = liElement.find_element_by_tag_name("span").text
        fileValue = fullStr.replace(surplusStr,"").strip()
        return fileValue


if __name__ == "__main__":
    spider = BossEntpPostSpider()
    spider.openDriver()
    spider.connect.close()
    spider.driver.quit()
