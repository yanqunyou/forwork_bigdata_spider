# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         qianChengWuYou_entp_and_post
# Description:   前程无忧网站 职位与企业数据采集（url从数据库区）
# Author:       forwork
# Date:         2019/7/23
#-------------------------------------------------------------------------------

import pymysql
import time
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType, Proxy
from spider_util.rollElementUtil import RollElementUtil
from spider_util.qianChengWuYouHandlesManage import QianChengWuYouHandlesManage
from spider_util.dateFormatUtil import DateFormatUtil
from selenium.webdriver.support.select import By
import random

class QianChengWuYouSpider(object):

    firefoxPath = "D:\\software\\Firefox\\geckodriver.exe"
    host = "https://www.51job.com/"

    educationConstant = "中专,高中,大专,本科,硕士,博士"

    def __init__(self):
        self.connect = pymysql.connect(host='192.168.1.214',
                                        port=3306,
                                        db='forwork_shanxi_ga',
                                        user='developer',
                                        passwd='123123',
                                        charset='utf8')
        self.cursor = self.connect.cursor()
        urlList = self.getFirstUrl()
        self.UrlItem = {}
        self.UrlItem['id'] = urlList[0]
        self.UrlItem['city'] = urlList[1]
        self.UrlItem['area'] = urlList[2]
        self.UrlItem['domain'] = urlList[3]
        self.UrlItem['industry'] = urlList[4]
        self.UrlItem['url'] = urlList[5]
        self.handlesManage = QianChengWuYouHandlesManage()
        self.rollElementUtil = RollElementUtil()
        self.dateFormatUtil = DateFormatUtil()


    def openDriver(self):
        proxy = Proxy(
            {
                'proxyType': ProxyType.MANUAL,  # 用不用都行
                # '203.130.46.108:9090'
                # '117.127.0.202:8080'   00
                # '120.234.63.196:3128'  00
                'httpProxy': '171.37.79.169:9797'
            }
        )
        # 新建一个“期望技能”，哈哈
        desired_capabilities = DesiredCapabilities.FIREFOX.copy()
        proxy.add_to_capabilities(desired_capabilities)
        # self.driver= webdriver.Firefox(executable_path=self.firefoxPath)
        self.driver= webdriver.Firefox(executable_path=self.firefoxPath, desired_capabilities=desired_capabilities)
        self.driver.maximize_window()
        self.driver.get(self.host)
        self.driver.implicitly_wait(10)
        self.driver.get(self.UrlItem['url'])
        self.parseSearchPage()
        self.updateStayUrlStatus(self.UrlItem['id'])

    def parseSearchPage(self):
        print(self.driver.current_url)
        try:
            WebDriverWait(driver=self.driver,timeout=10,poll_frequency=0.5).until(lambda x: x.find_element_by_id("resultList"))
        except Exception as e:
            time.sleep(2)
            print("等待超时！",e)

        contentDivs = self.driver.find_element_by_id("resultList").find_elements_by_class_name("el")
        for i in range(1,len(contentDivs)):
            print(contentDivs[i].text)
            entpA = contentDivs[i].find_element_by_class_name("t2")
            ea = entpA.find_element_by_tag_name("a")
            if "jobs.51job.com" in ea.get_attribute("href"):
                try:
                    self.rollElementUtil.rollToView_bottom(self.driver,ea)
                    entpA.click()
                except Exception as aa:
                    self.rollElementUtil.rollToView_top(self.driver,ea)
                    entpA.click()
                    print(aa)
                time.sleep(4)
                self.handlesManage.switch_SearchPage_To_EntpPage(driver=self.driver)
                self.parseEntp()
            else:
                continue

        try:
            pageDiv = self.driver.find_element_by_class_name("dw_page")
            if pageDiv != None:
                ul = pageDiv.find_element_by_tag_name("ul")
                nextPage = ul.find_element_by_link_text("下一页")
                try:
                    self.rollElementUtil.rollToView_bottom(self.driver, nextPage)
                    nextPage.click()
                except Exception as ae:
                    self.rollElementUtil.rollToView_top(self.driver, nextPage)
                    nextPage.click()
                    print("下一页点击：：：",ae)
                self.parseSearchPage()
        except Exception as e:
            print("获取下一页报错：：",e)

    def parseEntp(self):
        try:
            WebDriverWait(driver=self.driver,timeout=10,poll_frequency=0.5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,"con_txt")))
        except Exception as e:
            print("企业信息等待：：",e)

        print(self.driver.current_url)
        if self.driver.current_url == "about:blank":
            return

        entpItem = {}
        entpName = ""
        entpType = ""
        personScope = ""
        domain = ""
        entpInfo = ""
        website = ""
        address = ""
        entpId = None

        workExp = ""
        education = ""
        postNum = ""
        headDiv = None
        baseDiv = None
        try:
            headDiv = self.driver.find_element_by_css_selector(".tHeader.tHCop")
            baseDiv = headDiv.find_element_by_css_selector(".in")
        except Exception as e:
            return
            print("企业详情：：",e)

        try:
            entpNameH1 = baseDiv.find_element_by_tag_name("h1")
            entpName = entpNameH1.text.strip()
        except Exception as e:
            print("企业名称：：",e)

        try:
            # " 民营公司  |  150-500人  |  房地产 计算机软件 "
            ltypeDiv = baseDiv.find_element_by_class_name("ltype")
            ltypeStr = ltypeDiv.text
            splits = ltypeStr.split("|")
            if len(splits)==2:
                entpType = splits[0].strip()
                domain = splits[1].strip().replace(" ",",")
            else:
                entpType = splits[0].strip()
                personScope = splits[1].strip()
                domain = splits[2].strip().replace(" ", ",")
        except Exception as e:
            print("获取企业的基本信息出错！",e)

        companyDiv = None
        try:
            companyDiv = self.driver.find_element_by_class_name("tCompany_full")
        except Exception as e:
            print("没有找到企业的信息div::",e)
        # 点击 展开全部
        try:
            obutDiv = companyDiv.find_element_by_class_name("obut")
            obut = obutDiv.find_element_by_tag_name("em")
            if None != obut:
                try:
                    self.rollElementUtil.rollToView_bottom(self.driver,obut)
                    obut.click()
                except Exception as e:
                    self.rollElementUtil.rollToView_top(self.driver, obut)
                    obut.click()
                    print("点击展开全部L::",e)

                time.sleep(1)
        except Exception as e:
            print("没有展开全部按钮::",e)

        try:
            if None != companyDiv:
                entpInfo = companyDiv.find_element_by_class_name("con_txt").text
        except Exception as e:
            print(e)

        try:
            if None != companyDiv:
                fujiaDiv = companyDiv.find_element_by_css_selector(".tBorderTop_box.bmsg")
                dizhiDiv = fujiaDiv.find_element_by_class_name("inbox")
                pps = dizhiDiv.find_elements_by_tag_name("p")
                if pps != None:
                    address = pps[0].text.strip().replace("公司地址：","").replace(" ","").replace("\n","")
                if len(pps)>1:
                    website = pps[1].text.strip().replace("公司官网：","").replace(" ","").replace("\n","")
        except Exception as e:
            print(e)


        entpItem['entpName'] = entpName
        entpItem['entpType'] = entpType
        entpItem['personScope'] = personScope
        industry = domain if domain != "" else self.UrlItem['domain']
        entpItem['industry'] = industry
        entpItem['domain'] = self.UrlItem['domain']
        entpItem['entpInfo'] = entpInfo
        entpItem['website'] = website
        entpItem['address'] = address
        entpItem['city'] = self.UrlItem['city']
        entpItem['area'] = self.UrlItem['area']
        entpItem['url'] = self.driver.current_url
        # 通过名称查询是否已经存在
        item = self.existEntpFromDB(entpName)
        if item == None:
            entpId = self.saveEntp(entpItem)
        else:
            # updateEntpId = item[0]
            # domainDb = item[5]
            # industryDb = item[6]
            # updateDomain = ''
            # updateIndustry = ''
            # if domainDb != None and industryDb != None:
            #     updateDomain = domainDb if (entpItem['domain'] in domainDb) else (domainDb+','+entpItem['domain'])
            #     updateIndustry = industryDb if (entpItem['industry'] in industryDb) else (industryDb+','+entpItem['industry'])
            # else:
            #     updateDomain = entpItem['domain']
            #     updateIndustry = entpItem['industry']
            # #1. 如果已经存在就不在采集
            # self.updateEntpDomain(updateEntpId,updateDomain,updateIndustry)
            self.handlesManage.switch_entp_to_searchPage(self.driver)
            return
            #2. 如果已经存在还要采集
            # entpId = item[0]

        # try:
        # 获取职位列表
        joblistdata = self.driver.find_element_by_id("joblistdata")
        if None != joblistdata:
            jobLis = joblistdata.find_elements_by_class_name("el")
            if jobLis != None:
                for job in jobLis:
                    print(job.text)
                    postItem = {}
                    postNameDiv = job.find_element_by_class_name("t1")
                    postNameLink = postNameDiv.find_element_by_tag_name("a")
                    postName = postNameDiv.text.strip()
                    t2Str = job.find_element_by_class_name("t2").text
                    t3Str = job.find_element_by_class_name("t3").text
                    t4Str = job.find_element_by_class_name("t4").text
                    t5Str = job.find_element_by_class_name("t5").text
                    if t2Str == None or t2Str == "":
                        workExp = "2年经验"
                        education = "本科"
                        postNum = "3"
                    else:
                        splits = t2Str.split("|")
                        for sp in splits:
                            if "经验" in sp:
                                workExp = sp.strip()
                            if "招" in sp:
                                postNum = sp.replace("招", "").replace("人","")
                            if sp.strip() in self.educationConstant:
                                education = sp.strip()
                    city = ""
                    area = ""
                    t3Sps = t3Str.split("-")
                    if len(t3Sps) > 1:
                        city = t3Sps[0]
                        area = t3Sps[1]
                    else:
                        city = t3Str
                        area = t3Str
                    salary = t4Str
                    replaceTime = self.dateFormatUtil.dateFormat4WuyouPost(t5Str)
                    postItem['entpName'] = entpName
                    postItem['entpId'] = entpId
                    postItem['postName'] = postName
                    postItem['workExp'] = workExp
                    postItem['education'] = education
                    postItem['city'] = city
                    postItem['area'] = area
                    postItem['salary'] = salary
                    postItem['postNum'] = postNum.strip() if postNum != "" else "若干"
                    postItem['replaceTime'] = replaceTime
                    if None != postNameLink:
                        try:
                            self.rollElementUtil.rollToView_bottom(self.driver,postNameLink)
                            postNameLink.click()
                        except ElementNotInteractableException as e:
                            self.rollElementUtil.rollToView_top(self.driver,postNameLink)
                            postNameLink.click()
                            print("职位名称点击报错：：",e)
                        time.sleep(random.randint(2,3))
                        self.handlesManage.switch_Entp_To_Post(self.driver)
                        result = self.getMaxEntpId()
                        postItem['entpId'] = result[0]

                        self.parsePost(postItem)
        # except Exception as e:
        #     print("职位列表操作报错：：", e)
        time.sleep(1)
        self.handlesManage.switch_entp_to_searchPage(self.driver)

    def parsePost(self,postItem):
        time.sleep(4)
        print(self.driver.current_url)
        postHighlights = ""
        postDesc = ""
        address = ""
        try:
            WebDriverWait(self.driver,10,0.5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,"tCompany_main")))
        except Exception as e:
            print(e)

        try:
            tagDiv = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]")
            tags = tagDiv.find_elements_by_class_name("sp4")
            for tag in tags:
                postHighlights = postHighlights + ","+tag.text.strip()
        except Exception as e:
            print("职位热点找不到：：",e)
        try:
            companyDiv = self.driver.find_element_by_class_name("tCompany_main")
            if None != companyDiv:
                companyBoxs = companyDiv.find_elements_by_class_name("tBorderTop_box")
                if len(companyBoxs) == 3:
                    postDesc = companyBoxs[0].find_element_by_css_selector(".bmsg.job_msg.inbox").text
                    addressStr = companyBoxs[1].find_element_by_css_selector(".bmsg.inbox").find_element_by_css_selector(".fp").text
                    address = addressStr.replace("上班地址：","").strip()
        except Exception as e:
            print("职位描述：",e)

        postItem['postHighlights']=postHighlights[1:]
        postItem['postDesc']=postDesc
        postItem['address']=address
        postItem['postType']="全职"
        self.savePost(postItem)
        self.handlesManage.switch_Post_To_entp(self.driver)
    # 获取第一个待爬取URL
    def getFirstUrl(self):
        sqlStr = "SELECT * FROM `forwork_shanxi_ga`.qianchengwuyou_stay_url WHERE record_state = '1' ORDER BY id ASC LIMIT 1 "
        result = []
        try:
            self.cursor.execute(sqlStr)
            result = self.cursor.fetchone()
        except Exception as e:
            print("获取URL失败！",e)
        finally:
            return result

    # 企业最大id
    def getMaxEntpId(self):
        sqlStr = "SELECT MAX(id) FROM `forwork_shanxi_ga`.zhilian_entp;"
        self.cursor.execute(sqlStr)
        result = self.cursor.fetchone()
        return result

    # 企业信息存入数据库
    def saveEntp(self, entpItem):
        print("企业添加：：",entpItem)
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        last_id = None
        sqlStr = """
        INSERT INTO `forwork_shanxi_ga`.`zhilian_entp`
        (`entp_name`, `url`,`website`, `address`, `entp_info`, `entp_type`,
        `industry`,  `person_scope`, `domain`, `record_status`, 
        `city`, `area`, `create_time`, `update_time`,`data_from`) 
        VALUES (%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(sqlStr, (
                entpItem['entpName'], entpItem['url'], entpItem['website'], entpItem['address'],
                entpItem['entpInfo'], entpItem['entpType'],
                 entpItem['industry'], entpItem['personScope'], entpItem['domain'], '0',
                entpItem['city'], entpItem['area'], now, now,'2'
            ))

        except Exception as e:
            self.connect.rollback()
            print("添加企业数据出错：",e)
        finally:
            self.connect.commit()

    # 企业职位存入数据库
    def savePost(self, postItem):
        print("职位添加：：",postItem)
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sqlStr = """
            INSERT INTO `forwork_shanxi_ga`.`zhilian_entp_post`
            (`entp_id`, `entp_name`, `post_name`, `salary`, `area`, `city`, `work_exp`, 
            `education`, `post_num`, `post_highlights`, `post_desc`,`replace_time`,
            `address`,`record_status`,`create_time`, `update_time`,`data_from`,`post_type`) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(sqlStr, (
                postItem['entpId'], postItem['entpName'],postItem['postName'], postItem['salary'], postItem['area'], postItem['city'],
                postItem['workExp'],
                postItem['education'], postItem['postNum'], postItem['postHighlights'], postItem['postDesc'],
                postItem['replaceTime'],
                postItem['address'], '0', now, now,'2',postItem['postType']
            ))
        except Exception as e:
            self.connect.rollback()
            print(e)
        finally:
            self.connect.commit()

    # 根据 id 修改待爬取URL爬取状态
    def updateStayUrlStatus(self, id):
        strSql = "UPDATE qianchengwuyou_stay_url SET record_state = '0' WHERE id = " + str(id)
        try:
            self.cursor.execute(strSql)
        except Exception as e:
            print(e)
            self.connect.rollback()
        finally:
            self.connect.commit()

    # 根据企业id删除职位
    def deleteEntpPostByEntpId(self, entpId):
        try:
            self.cursor.execute("DELETE FROM `forwork_shanxi_ga`.zhilian_entp_post WHERE id = " + entpId)
            self.connect.commit()
        except Exception as e:
            print(e)

    # 通过企业名称查询数据库
    def existEntpFromDB(self, entpName):
        searchSql = ("SELECT id,entp_info,city,area,person_scope,`domain`,industry FROM `forwork_shanxi_ga`.zhilian_entp where entp_name ='" + entpName+ "'")
        items = None
        try:
            # 执行SQL语句
            self.cursor.execute(searchSql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            if len(results) > 0:
                items = results[0]
        except Exception as e:
            print(e)
        finally:
            print("数据库验证结果：" + str(items))
            return items


if __name__ == "__main__":
    spider = QianChengWuYouSpider()
    spider.openDriver()
    spider.driver.close()
    spider.connect.close()


