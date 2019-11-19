# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         daoshiSpider
# Description:  
# Author:       forwork
# Date:         2019/1/14
#-------------------------------------------------------------------------------
import json
import random
import time
import uuid

import scrapy
from scrapy import Request, FormRequest
from bs4 import BeautifulSoup
from daoshi_spider.items import TalentItem

class DaoshiSpider(scrapy.Spider):
    name = "daoshiSpider"
    host = "daoshi.eol.cn"
    baseUrl = "https://daoshi.eol.cn/home/getTutor?special_id=&page={}&recommend=1"
    detailUrl = "https://daoshi.eol.cn/tutor/{}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Host": "daoshi.eol.cn",
        "Referer": "https://daoshi.eol.cn/",
        "X-Requested-With": "XMLHttpRequest"
    }

    def start_requests(self):
        # 4984
        # url = self.baseUrl.format(str(3))
        # yield Request(url=url, callback=self.parse, dont_filter=True, headers=self.headers, method="GET")

        for i in range(5020):
            url = self.baseUrl.format(str(i))
            # time.sleep(random.randint(2,5))
            time.sleep(1)
            print("列表页：：",url)
            yield Request(url=url,callback=self.parse, dont_filter=True,headers=self.headers,method="GET")

    def parse(self, response):
        if response.status != 200:
            print(response.text)
            print("url::"+response.url+"  请求异常！！！进行重试")
            yield Request(url=response.url,callback=self.parse,meta={"download_timeout":5}, dont_filter=True,headers=self.headers,method="GET")
        results = json.loads(response.text)
        print(response.text)
        datas = results['data']

        if datas != None:
            for dt in datas:
                id = dt['tutor_id']
                print("详情页：：：：",self.detailUrl.format(id))
                yield Request(url=self.detailUrl.format(id), meta={"download_timeout":3},dont_filter=True,callback=self.parseDetail,headers=self.headers,method="GET")

    def parseDetail(self,response):
        if response.status != 200:
            print("url::"+response.url+"  请求异常！！！进行重试")
            yield Request(url=response.url,callback=self.parseDetail,meta={"download_timeout":3},dont_filter=True,headers=self.headers,method="GET")
        soup = BeautifulSoup(response.text,"html.parser")
        jieshaoDiv = soup.find("div",{"class":"teacher-jieshao"})
        baseDivs = jieshaoDiv.findAll("div",{"class":"teacher-td"})
        talentItem = TalentItem()
        url = response.url
        tid = str(uuid.uuid3(uuid.NAMESPACE_DNS, url))

        name = ""
        sex = ""
        orgName = ""
        title = ""
        daoshiType = ""
        zhuanye = ""
        domain = ""
        telephone = ""
        email = ""
        address = ""
        for it in baseDivs:
            divs = it.findAll("div")
            # teacher-td xinxi-more dpn
            if divs != None:
                for dd in divs:
                    if "姓名" in dd.getText():
                        name = dd.getText().split("：")[1]
                    if "性别" in dd.getText():
                        sex = dd.getText().split("：")[1]
                    if "院校" in it.getText():
                        orgName = it.div.getText().split("：")[1]
                    if "院系" in it.getText():
                        yuanxi = it.getText().split("：")[1]
                    if "职称" in it.getText():
                        title = it.div.getText().split("：")[1]
                    if "类型" in it.getText():
                        daoshiType = it.getText().split("：")[1]
            if "专业" in it.getText():
                zhuanye = it.getText().split("：")[1].replace("\\n","").replace("、",",").strip()
        domainDiv = jieshaoDiv.find("div",{"class":"teacher-td xinxi-more dpn"})
        if domainDiv != None:
            #  特殊： 1）药物分析；2）微生物蛋白组学研究；3）电催化研究
            domain = domainDiv.getText().replace("\d+",",")[:1].replace("；","").replace("）","")
        tongxun = soup.find("div",{"class":"main-lf-con"})
        if tongxun != None:
            txDivs = tongxun.find("div",{"class":"lf-item-con"})
            if txDivs != None:
                for tx in txDivs.findAll("div"):
                    if "电话" in tx.getText():
                        telephone = tx.getText().split("：")[1]
                    if "邮件" in tx.getText():
                        email = tx.getText().split("：")[1]
                    if "地址" in tx.getText():
                        address = tx.getText().split("：")[1]

        talentItem['url']=url
        talentItem['tid']=tid
        talentItem['name']=name
        talentItem['sex']=("男" if sex == "" else sex)
        talentItem['orgName']=orgName.strip()
        talentItem['title']=title.strip()
        talentItem['domain']= domain if zhuanye == "" else zhuanye
        talentItem['telephone']=telephone.strip()
        talentItem['email']=email.strip()
        talentItem['address']=address.strip()
        talentItem['highestEdu']=title.strip()
        talentItem['researchInterest']=domain.strip()
        print("数据：：",talentItem)
        yield talentItem