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
from lagouUtil.lagouHandleUtil import LagouHandleUntl
from lagouUtil.rollElementUtil import RollElementUtil
from lagouUtil.dateFormatUtil import DateFormatUtil
import random

class LagouEntpPostSpider(object):

    firefoxPath = "D:\\software\\Firefox\\geckodriver.exe"
    chromePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
    host = "https://www.51job.com/"

    educationConstant = "中专,高中,大专,本科,硕士,博士"

    industrys = [
    {
        "code": "0002",
        "industry": "移动互联网",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0003",
        "industry": "电商",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0004",
        "industry": "金融",
        "domain": "金融业"
    }, {
        "code": "0005",
        "industry": "企业服务",
        "domain": "专业服务"
    }, {
        "code": "0006",
        "industry": "教育",
        "domain": "教育培训/科研"
    }, {
        "code": "0007",
        "industry": "文娱丨内容",
        "domain": "文化/体育/娱乐"
    }, {
        "code": "0008",
        "industry": "游戏",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0009",
        "industry": "消费生活",
        "domain": "批发/零售/贸易"
    }, {
        "code": "0010",
        "industry": "硬件",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0011",
        "industry": "社交",
        "domain": "专业服务"
    }, {
        "code": "0012",
        "industry": "旅游",
        "domain": "生活服务"
    }, {
        "code": "0013",
        "industry": "体育",
        "domain": "文化/体育/娱乐"
    }, {
        "code": "0014",
        "industry": "汽车丨出行",
        "domain": "交通运输/仓储/物流"
    }, {
        "code": "0015",
        "industry": "物流丨运输",
        "domain": "交通运输/仓储/物流"
    }, {
        "code": "0016",
        "industry": "医疗丨健康",
        "domain": "卫生及社会工作"
    }, {
        "code": "0017",
        "industry": "广告营销",
        "domain": "专业服务"
    }, {
        "code": "0018",
        "industry": "数据服务",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0019",
        "industry": "信息安全",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0020",
        "industry": "人工智能",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0021",
        "industry": "区块链",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0022",
        "industry": "物联网",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0023",
        "industry": "VR丨AR",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0024",
        "industry": "软件开发",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0025",
        "industry": "通讯电子",
        "domain": "互联网/IT/电子/通信"
    }, {
        "code": "0026",
        "industry": "房产家居",
        "domain": "房地产,建筑业"
    }]

    def __init__(self):
        self.connect = pymysql.connect(host='192.168.1.214',
                                       port=3306,
                                       db='forwork_shanxi_ga',
                                       user='developer',
                                       passwd='123123',
                                       charset='utf8')
        self.cursor = self.connect.cursor()
        urlList = self.getLagouFirstUrl()
        self.UrlItem = {}
        self.UrlItem['id'] = urlList[0]
        self.UrlItem['city'] = urlList[1]
        self.UrlItem['area'] = urlList[2]
        self.UrlItem['domain'] = urlList[3]
        self.UrlItem['industry'] = urlList[4]
        self.UrlItem['url'] = urlList[5]
        self.lagouHandleUtil = LagouHandleUntl()
        self.rollHandleUtil = RollElementUtil()
        self.dateFormatUtil = DateFormatUtil()

    def openDriver(self):
        proxy = Proxy(
            {
                'proxyType': ProxyType.MANUAL,  # 用不用都行
                # '203.130.46.108:9090'
                # '117.127.0.202:8080'   00
                # '120.234.63.196:3128'  00
                'httpProxy': '111.29.3.223:8080'
            }
        )
        # 新建一个“期望技能”，哈哈
        desired_capabilities = DesiredCapabilities.FIREFOX.copy()
        proxy.add_to_capabilities(desired_capabilities)
        # self.driver= webdriver.Firefox(executable_path=self.firefoxPath)
        self.driver = webdriver.Firefox(executable_path=self.firefoxPath, desired_capabilities=desired_capabilities)
        self.driver.get("https://www.lagou.com")
        time.sleep(40)
        self.driver.get(self.UrlItem['url'])
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.parseSearchPage()
        self.updateLagouStaryUrl(self.UrlItem['id'])

    def parseSearchPage(self):
        print(self.driver.current_url)
        try:
            WebDriverWait(driver=self.driver,timeout=10,poll_frequency=0.5).until(expected_conditions.presence_of_element_located((By.ID,"s_position_list")))
        except TimeoutException as e:
            print(e)

        # try:
        #     switchCityDiv = self.driver.find_element_by_id("switchCity")
        #     if None != switchCityDiv:
        #         cityLink = switchCityDiv.find_element_by_link_text("吕梁站")
        #         cityLink.click()
        # except Exception as e:
        #     print("切换站点：：",e)

        try:
            postList = self.driver.find_element_by_id("s_position_list")
            postUl = postList.find_element_by_class_name("item_con_list")
            postLis = postUl.find_elements_by_css_selector(".con_list_item.default_list")
            print(len(postLis))
            if None != postLis:
                for li in postLis:
                    companyNameDiv = li.find_element_by_css_selector(".company_name")
                    commpanyLink = companyNameDiv.find_element_by_tag_name("a")
                    if None != commpanyLink:
                        try:
                            self.rollHandleUtil.rollToView_bottom(self.driver,commpanyLink)
                            commpanyLink.click()
                        except Exception as e:
                            self.rollHandleUtil.rollToView_top(self.driver,commpanyLink)
                            commpanyLink.click()
                            print(e)
                        # 此处为列表页跳转到企业详情页
                        time.sleep(2)
                        self.lagouHandleUtil.switch_SearchPage_To_EntpPage(self.driver)
                        self.parseEntp()
                try:
                    pageNext = self.driver.find_element_by_class_name("pager_next ")
                    try:
                        self.rollHandleUtil.rollToView_bottom(self.driver, pageNext)
                        pageNext.click()
                    except Exception as e:
                        self.rollHandleUtil.rollToView_top(self.driver, pageNext)
                        pageNext.click()
                        print(e)
                    self.parseSearchPage()
                except Exception as e:
                    print(e)

        except NoSuchElementException as ae:
            print(ae)


    def parseEntp(self):
        print(self.driver.current_url)
        entpItem = {}
        url = self.driver.current_url
        entpName = ""
        entpId = None
        entpInfo = ""
        entpType = ""
        website = ""
        industry = ""
        domain = ""
        personScope = ""
        city = ""
        area = ""
        highlight = ""
        address = ""
        foundDate = ""
        registerFund = ""
        legalPerson = ""

        try:
            WebDriverWait(self.driver,timeout=10,poll_frequency=0.5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,"company_main")))
        except TimeoutException as e:
            print(e)

        try:
            companyDiv = self.driver.find_element_by_class_name("company_main")
            h2 = companyDiv.find_element_by_tag_name("h2")
            companyLink = h2.find_element_by_tag_name("a")
            if None != companyLink:
                website = companyLink.get_attribute("href")
                entpName = companyLink.get_attribute("title")

            try:
                textOver = self.driver.find_element_by_class_name("text_over")
                if None != textOver:
                    try:
                        self.rollHandleUtil.rollToView_bottom(self.driver,textOver)
                        textOver.click()
                    except:
                        self.rollHandleUtil.rollToView_top(self.driver,textOver)
                        textOver.click()
            except Exception as e:
                print(e)

        except Exception as e:
            print(e)

        # 企业详细信息
        try:
            companyContentDiv = self.driver.find_element_by_class_name("company_content")
            entpInfo = companyContentDiv.text
        except Exception as e:
            print(e)
        try:
        # 所属行业
            containerDiv = self.driver.find_element_by_id("basic_container")
            if None != containerDiv:
                contentDiv = containerDiv.find_element_by_class_name("item_content")
                if None != contentDiv:
                    baseUL = contentDiv.find_element_by_tag_name("ul")
                    baseLis = baseUL.find_elements_by_tag_name("li")
                    industry = baseLis[0].find_element_by_tag_name("span").text.strip()
                    domain = self.getDomainByIndustry(industry)
                    entpType = baseLis[1].find_element_by_tag_name("span").text.strip()
                    personScope = baseLis[2].find_element_by_tag_name("span").text.strip()
                    city = baseLis[3].find_element_by_tag_name("span").text.strip()
        except Exception as e:
            print(e)

        try:
            tagsDiv = self.driver.find_element_by_id("tags_container")
            tagLis = tagsDiv.find_elements_by_name("li")
            for li in tagLis:
                highlight =highlight+"," + li.text
            if "" != highlight:
                highlight = highlight[1:]
        except Exception as e:
            print(e)

        try:
            bussinessDiv = self.driver.find_element_by_class_name("company_bussiness_info_container")
            if None != bussinessDiv:
                infoDivs = bussinessDiv.find_elements_by_class_name("info_item")
                foundDate = infoDivs[1].find_element_by_class_name("content").text.strip()
                registerFund = infoDivs[2].find_element_by_class_name("content").text.strip()
                legalPerson = infoDivs[3].find_element_by_class_name("content").text.strip()
        except Exception as e:
            print(e)
        try:
            addressDiv = self.driver.find_element_by_id("location_container")
            if None != addressDiv:
                addressUl = addressDiv.find_element_by_class_name("con_mlist_ul")
                addLis = addressUl.find_elements_by_tag_name("li")
                if None != addLis:
                    cityArea = addLis[0].find_element_by_class_name("mlist_li_title").find_element_by_tag_name("span").text.strip()
                    areaList = cityArea.split(",")
                    if len(areaList) >1:
                        city = areaList[0].replace("市","")
                        area = areaList[1]
                    else:
                        city = cityArea.replace("市","")
                    address = addLis[0].find_element_by_class_name("mlist_li_desc").text.strip()
        except Exception as e:
            print(e)

        entpItem['entpName'] = entpName
        entpItem['entpInfo'] = entpInfo
        entpItem['entpType'] = entpType
        entpItem['website'] = website
        entpItem['industry'] = industry
        entpItem['url'] = url
        entpItem['domain'] = domain
        entpItem['personScope'] = personScope
        entpItem['city'] = city
        entpItem['area'] = area
        entpItem['highlight'] = highlight
        entpItem['address'] = address
        entpItem['foundDate'] = foundDate
        entpItem['registerFund'] = registerFund
        entpItem['legalPerson'] = legalPerson

        result = self.existEntpFromDB(entpName)
        if None != result:
            entpId = result[0]
        else:
            self.saveEntp(entpItem)
            result = self.existEntpFromDB(entpName)
            entpId = result[0]

        try:
            companyNavsDiv = self.driver.find_element_by_id("company_navs")
            companyNavs = companyNavsDiv.find_element_by_class_name("company_navs_wrap")
            if None != companyNavs:
                navUl = companyNavs.find_element_by_tag_name("ul")
                navLis = navUl.find_elements_by_tag_name("li")
                if None != navLis:
                    postLa = navLis[1].find_element_by_tag_name("a")
                    postLa.click()
                    time.sleep(1)
                    self.parsePostList(entpId,entpName)
        except Exception as e:
            print(e)

    def parsePostList(self,entpId,entpName):
        print("进入职位列表解析。")
        try:
            WebDriverWait(self.driver,10,0.5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,"item_con_list")))
        except Exception as e:
            print("职位列表解析：",e)

        try:
            conListDiv = self.driver.find_element_by_class_name("item_con_list")
            if None != conListDiv:
                conLis = conListDiv.find_elements_by_tag_name("li")
                for cli in conLis:
                    cDiv = cli.find_element_by_class_name("item_title_date")
                    postA = cDiv.find_element_by_tag_name("a")
                    try:
                        self.rollHandleUtil.rollToView_bottom(self.driver,postA)
                        postA.click()
                    except Exception as e:
                        self.rollHandleUtil.rollToView_top(self.driver,postA)
                        postA.click()
                        print(e)
                    time.sleep(random.randint(4,5))
                    self.lagouHandleUtil.switch_EntpPage_To_Post(self.driver)
                    self.parsePost(entpId,entpName)
        except Exception as e:
            print(e)

        try:
            pagesDiv = self.driver.find_element_by_class_name("pages")
            if None != pagesDiv:
                nextPage = pagesDiv.find_element_by_class_name("next")
                if nextPage.is_enabled():
                    try:
                        self.rollHandleUtil.rollToView_bottom(self.driver,nextPage)
                        nextPage.click()
                    except Exception as e:
                        self.rollHandleUtil.rollToView_top(self.driver,nextPage)
                        nextPage.click()
                        print(e)
                    self.parsePostList(entpId,entpName)
                else:
                    print("职位列表下一页不可点击！")
                    self.lagouHandleUtil.switch_EntpPage_To_SearchPage(self.driver)
            else:
                print("职位列表下一页找不到！")
                self.lagouHandleUtil.switch_EntpPage_To_SearchPage(self.driver)
        except Exception as e:
            self.lagouHandleUtil.switch_EntpPage_To_SearchPage(self.driver)
            print("职位下一页:",e)

    def parsePost(self,entpId,entpName):
        print("进入解析职位。")
        try:
            WebDriverWait(self.driver,10,0.5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,"position-head")))
        except Exception as e:
            print(e)

        postItem = {}
        city = ""
        area = ""
        postName = ""
        postType = ""
        workExp = ""
        education = ""
        salary = ""
        postNum = random.randint(2,6)
        replaceTime = ""
        postHighlights = ""
        postDesc = ""
        address = ""
        positionDiv = None
        try:
            positionDiv = self.driver.find_element_by_class_name("position-head")
            if None != positionDiv:
                jobNameDiv = positionDiv.find_element_by_class_name("job-name")
                postName = jobNameDiv.get_attribute("title")
        except Exception as e:
            print(e)

        try:
            # job_request
            if None != positionDiv:
                requestDiv = positionDiv.find_element_by_class_name("job_request")
                baseH3 = requestDiv.find_element_by_tag_name("h3")
                if None != baseH3:
                    baseSpans = baseH3.find_elements_by_tag_name("span")
                    salary = baseSpans[0].text.strip()
                    city = baseSpans[1].text.replace("/","").strip()
                    workExp = baseSpans[2].text.replace("/","").strip()
                    education = baseSpans[3].text.replace("/","").strip()
                    postType = baseSpans[4].text.replace("/","").strip()
                replaceDate = requestDiv.find_element_by_class_name("publish_time").text
                replaceDate = replaceDate.split(" ")[0].strip()
                if len(replaceDate) > 8:
                    # 2019-07-15
                    replaceTime = replaceDate
                elif '天前' in replaceDate:
                    replaceTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                else:
                    # 13:15
                    replaceTime = self.dateFormatUtil.dateFormat4ZhilianPost(replaceDate)
        except Exception as e:
            print(e)

        jobDetailDiv = self.driver.find_element_by_id("job_detail")
        try:
            jobAdvantage = jobDetailDiv.find_element_by_class_name("job-advantage")
            if None != jobAdvantage:
                jobAdvantage.find_element_by_tag_name("p").text.replace("、等","").replace("。","")
        except Exception as e:
            print(e)

        try:
            jobBt = jobDetailDiv.find_element_by_class_name("job_bt")
            postDesc = jobBt.find_element_by_class_name("job-detail").text.strip()
        except Exception as e:
            print(e)

        try:
            jobAddress = jobDetailDiv.find_element_by_css_selector(".job-address.clearfix")
            addressTag = jobAddress.find_element_by_class_name("work_addr").text.strip()
            addressTags = addressTag.split("-")
            city = addressTags[0].strip()
            area = addressTags[1].strip()
            address = city+area+addressTags[3].strip()
        except Exception as e:
            print(e)

        postItem['entpId'] = entpId
        postItem['entpName'] = entpName
        postItem['city'] = city
        postItem['area'] = area
        postItem['postName'] = postName
        postItem['postType'] = postType
        postItem['workExp'] = workExp
        postItem['education'] = education
        postItem['salary'] = salary
        postItem['postNum'] = postNum
        postItem['replaceTime'] = replaceTime
        postItem['postHighlights'] = postHighlights
        postItem['postDesc'] = postDesc
        postItem['address'] = address
        self.savePost(postItem)
        self.lagouHandleUtil.switch_Post_To_Entp(self.driver)

    # 企业信息存入数据库
    def saveEntp(self, entpItem):
        print("企业添加：：", entpItem)
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
                entpItem['city'], entpItem['area'], now, now, '3'
            ))

        except Exception as e:
            self.connect.rollback()
            print("添加企业数据出错：", e)
        finally:
            self.connect.commit()

    # 企业职位存入数据库
    def savePost(self, postItem):
        print("职位添加：：", postItem)
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sqlStr = """
            INSERT INTO `forwork_shanxi_ga`.`zhilian_entp_post`
            (`entp_id`, `entp_name`, `post_name`, `salary`, `area`, `post_type`, `city`, `work_exp`, 
            `education`, `post_num`, `post_highlights`, `post_desc`,`replace_time`,
            `address`,`record_status`,`create_time`, `update_time`,`data_from`) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(sqlStr, (
                postItem['entpId'], postItem['entpName'], postItem['postName'], postItem['salary'],
                postItem['area'], postItem['postType'], postItem['city'],
                postItem['workExp'],
                postItem['education'], postItem['postNum'], postItem['postHighlights'], postItem['postDesc'],
                postItem['replaceTime'],
                postItem['address'], '0', now, now, '3'
            ))
        except Exception as e:
            self.connect.rollback()
            print(e)
        finally:
            self.connect.commit()

    # 通过企业名称查询数据库
    def existEntpFromDB(self, entpName):
        searchSql = "SELECT id,entp_info,city,area,person_scope FROM zhilian_entp where entp_name ='" + entpName + "'"
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

    def getDomainByIndustry(self,industry):
        splits = industry.split(",")
        domain = ""
        for ins in self.industrys:
            for sp in splits:
                if ins['industry'] == sp:
                    domain = domain+","+ins['domain']
        if "" != domain:
            domain = domain[1:]
        return domain

    def getLagouFirstUrl(self):
        strSql = "SELECT * FROM `forwork_shanxi_ga`.lagou_stay_url WHERE record_state = '1' LIMIT 1;"
        result = []
        try:
            self.cursor.execute(strSql)
            result = self.cursor.fetchone()
        except Exception as e:
            print("获取URL失败！", e)
        finally:
            return result

    def updateLagouStaryUrl(self,id):
        updateStr = "UPDATE `forwork_shanxi_ga`.lagou_stay_url SET record_state='0' WHERE id = %s ;"
        try:
            self.cursor.execute(updateStr,(id))
        except Exception as e:
            self.connect.rollback()
            print(e)
        finally:
            self.connect.commit()


if __name__ == "__main__":
    lagouSpider = LagouEntpPostSpider()
    lagouSpider.openDriver()
    lagouSpider.driver.close()
