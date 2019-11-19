# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         ScientistSpider
# Description:  
# Author:       forwork
# Date:         2018/12/19
# -------------------------------------------------------------------------------
import random

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
import time,datetime
import json
from scientistSpider.items import PaperItem
from scientistSpider.items import PatentItem
from scientistSpider.items import ProjectItem
from scientistSpider.items import SelfItem
from scientistSpider.items import TagItem
from scientistSpider.items import TeamItem
from scientistSpider.items import CoordinateItem


class ScientistSpider(scrapy.Spider):
    name = "scientistSpider"

    host = "www.scientistin.com"
    """ 
                以专利为查询条件：
                http://www.scientistin.com/api/search-service?p=/user/patent:大数据/0/0/0/0&callback=resultcallback&_=1560474985988
                以领域为查询条件：
                http://www.scientistin.com/api/search-service?p=/user/domain:大数据/0/0/0/0&callback=resultcallback&_=1560474985989
    """
    base_url = "http://www.scientistin.com/api/search-service?p=/user/patent:{}/{}/0/0/0&callback=resultcallback&_={}"
    detail_url = "http://www.scientistin.com/search/web/user.jsp?{}"
    ditu_url = "http://www.scientistin.com/api/geo-graph?src={}&type=1"
    # 云标签 url参数：uri 时间戳
    yun_tag_url = "http://60.205.143.54:8181/scientist/{}?callback=resultcallback2&_={}"

    custom_settings = {
        'LOG_LEVEL': 'INFO',  # 减少Log输出量，仅保留必要的信息
        # ...... 在爬虫内部用custom_setting可以让这个配置信息仅对这一个爬虫生效
    }

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Host": "www.scientistin.com",
        "Referer": "http://www.scientistin.com/search/web/result.jsp"
    }

    # 接口URL 返回json
    do_mains = [
        "大数据",
        "5G",
        "人工智能",
        "物联网",
        "云计算",
        "云制造",
        "区块链",
        "信息产业",
        "节能环保",
        "新能源",
        "新能源汽车",
        "生物医疗",
        "高端装备制造业",
        "新材料",
        "其他"]

    # 启动
    def start_requests(self):
        # for dm in self.do_mains:
        #     for i in range(30):
        #         start_url = self.base_url.format(dm, str(i),str(time.localtime()))
        #         time.sleep(2)
        #         yield Request(url=start_url, meta={"dm":dm}, headers=self.headers, callback=self.pars_list_page)
        start_url = self.base_url.format("5G", str(i),str(int(time.time()*1000)))
        print(start_url)
        yield Request(url=start_url, meta={"dm": "节能环保"}, headers=self.headers, callback=self.pars_list_page)


    def pars_list_page(self, response):
        if "已被禁止操作" in response.text:
            print(response.url + "::已被禁止操作！！！！")
            return

        result = response.text.replace("/**/resultcallback(", "")
        resultJson = json.loads(result[:-2])
        contents = resultJson.get("content")

        dm = response.meta['dm']
        sc_detail_url = ""
        if contents != None:
            for con in contents:

                selfItem = SelfItem()
                selfItem['domain'] = dm

                uri = con.get("uri")
                ulen = len(uri)
                if uri == None or uri == '':
                    uri = con.get("uid")
                    selfItem['uri'] = uri
                    sc_detail_url = self.detail_url.format("uid=" + uri)
                    selfItem['pageUrl'] = sc_detail_url
                else:
                    if ulen > 32:
                        uri = uri[1:-1]
                    selfItem['uri'] = uri
                    sc_detail_url = self.detail_url.format("uri=" + uri)
                    selfItem['pageUrl'] = sc_detail_url

                selfItem['scName'] = con.get("name")
                selfItem['scOrg'] = con.get("org")

                domains = con.get("domains")
                dlen = len(domains)
                domain = ""
                if domains != None:
                    for i in range(dlen):
                        domain += domains[i] + ("" if (i == (dlen - 1)) else ",")
                selfItem['scDomain'] = domain
                selfItem['urlIspersistence'] = '1'
                selfItem['urlIsgather'] = '1'
                selfItem['paperNum'] = con.get("ach")
                selfItem['quoteRate'] = con.get("cited")
                selfItem['HFactor'] = con.get("h")
                headers1 = self.headers.update({"Referer": sc_detail_url})
                # 云标签
                # yunTagUrl = self.yun_tag_url.format(uri, str(time.localtime()))
                yield scrapy.Request(url=sc_detail_url, meta={"sc_detail_url":sc_detail_url,"selfItem":selfItem},
                                     encoding='utf-8', headers=headers1, callback=self.parse_sc_detail, method="GET")

    # 解析详情URL数据
    def parse_sc_detail(self, response):
        sc_detail_url = response.meta['sc_detail_url']
        if "已被禁止操作" in response.text:
            print(sc_detail_url + "::已被禁止操作！！！！")
            return
        selfItem = response.meta['selfItem']

        selfUri = selfItem.get("uri")

        # 云标签
        yunTagUrl = self.yun_tag_url.format(selfUri, str(time.localtime()))

        soup = BeautifulSoup(response.text, 'html.parser')

        # # 合作团队
        teamb = soup.find("div", {"id": "home"})
        if teamb != None:
            teams = teamb.findAll("div", {"class": "ser_conts"})
            if teams != None:
                for item in teams:
                    teamItem = TeamItem()
                    teamItem['uri'] = selfUri

                    href = item.a.get("href")  # 合作人的URL
                    teamItem['tUrl'] = href.strip()

                    spans = item.a.findAll("span")
                    if spans != None:
                        teamItem['tName'] = spans[0].getText().strip()
                        teamItem['tOrg'] = spans[1].getText().strip()
                        hh = spans[2].getText()
                        if hh != None:
                            hh = hh.strip().split("：")[1]
                            teamItem['tHFactor'] = hh
                        nn = spans[3].getText()
                        if nn != None:
                            nn = nn.strip().split(":")[1]
                            teamItem['tNum'] = nn
                    yield teamItem

        # # 科研项目
        aboutb = soup.find("div", {"id": "about"})
        if aboutb != None:
            abouts = aboutb.findAll("div", {"class": "ser_conts"})
            if abouts != None:
                for item in abouts:
                    projectItem = ProjectItem()
                    projectItem['uri'] = selfUri

                    spans = item.findAll("span")
                    if spans != None:
                        projectLeader = spans[0].getText().strip().split("：")[1]
                        projectItem['projectLeader'] = projectLeader
                        projectItem['projectLeaderOrg'] = spans[1].getText().strip()
                        projectItem['projectName'] = spans[2].getText().strip().split("：")[1]
                        projectItem['projectFund'] = spans[3].getText().strip().split(":")[1]
                        projectItem['projectKeyword'] = spans[4].getText().strip().split(":")[1]
                    yield projectItem

        # # 发明专利
        profileb = soup.find("div", {"id": "profile"})
        if profileb != None:
            profiles = profileb.findAll("div", {"class": "ser_conts"})
            if profiles != None:
                for item in profiles:
                    patentItem = PatentItem()
                    patentItem['uri'] = selfUri
                    spans = item.findAll("span")
                    if spans != None:
                        patentItem['pathentName'] = spans[0].getText().strip().split("：")[1]
                        patentItem['pathentNo'] = spans[1].getText().strip().split("：")[1]
                        patentItem['pathentTime'] = spans[2].getText().strip().split("：")[1]
                    yield patentItem

        # # 论文成果contact
        contactb = soup.find("div", {"id": "contact"})
        if contactb != None:
            contacts = contactb.findAll("div", {"class": "ser_conts"})
            if contacts != None:
                for item in contacts:
                    paperItem = PaperItem()
                    paperItem['uri'] = selfUri
                    spans = item.findAll("span")
                    if spans != None:
                        paperItem['paperName'] = spans[0].font.getText().strip()
                        paperItem['paperAuthor'] = spans[1].getText().strip().split("：")[1]
                        paperItem['quoteNum'] = spans[2].getText().strip().split("：")[1]
                        paperItem['periodical'] = spans[4].getText().strip().split("：")[1]
                    yield paperItem
        time.sleep(random.randint(1, 3))
        yield scrapy.Request(url=yunTagUrl, encoding='utf-8', meta={"selfItem":selfItem,"uri":selfUri},
                             callback=self.parse_yun_tag, method="GET")

    def parse_yun_tag(self, response):
        selfItem = response.meta["selfItem"]
        uri = response.meta["uri"]
        result = response.text.replace("/**/resultcallback2(", "")
        resultJson = json.loads(result[:-2])
        datas = resultJson.get("data")
        tags = ""
        if datas != None and datas != "":
            for it in datas:
                tags += it +":"+str(datas[it])+","
            tags = tags[:-1]
        selfItem["tagCloud"] = tags


        yield selfItem
        # yield Request(url=self.ditu_url.format(uri),meta={"uri":uri,"selfItem":selfItem},
        #               encoding='utf-8',callback=self.paese_ditu, method="GET")

    def paese_ditu(self,response):
        uri = response.meta["uri"]
        selfItem = response.meta["selfItem"]
        resultJson = json.loads(response.text)
        content = resultJson.get("data")
        maps = content.get("authorMap")
        keys = maps.keys()
        for key in keys:
            coordinateItem = CoordinateItem()
            coordinateItem['uri'] = uri
            value = "["+str(maps.get(key)[0])+","+str(maps.get(key)[1])+"]"
            coordinateItem['coordinate'] = key+"="+value
            yield coordinateItem
