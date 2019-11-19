# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         __init__
# Description:  此爬虫为从数据库中获取搜索URL对象，采集里面的企业信息与职位列表信息，入库
# Author:       forwork
# Date:         2019/7/18
#-------------------------------------------------------------------------------
import hashlib
import random

import scrapy
from scrapy import Request
import time
import json
from bs4 import BeautifulSoup
from zhilian_entp_spider.items import ZhilianEntpSpiderItem as EntpItem
import uuid

from zhilian_entp_spider.pipelines import ZhilianEntpSpiderPipeline


class ZhilianEntpSpider(scrapy.Spider):
    name = "zhilian_entp_spider"
    host = "https://zhaopin.com"
    allowed_domains = ['zhaopin.com']
    custom_settings = {
        'LOG_LEVEL': 'INFO',  # 减少Log输出量，仅保留必要的信息
        # ...... 在爬虫内部用custom_setting可以让这个配置信息仅对这一个爬虫生效
    }

    headers = {
        "Accept":"application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN",
        "Cache-Control": "no-cache",
        "Host": "fe-api.zhaopin.com",
        "Origin": "https://sou.zhaopin.com",
        "Referer": "https://sou.zhaopin.com/?jl=530",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    }

    zhilianEntpSpiderPipeline = ZhilianEntpSpiderPipeline()
    def start_requests(self):
        result = self.zhilianEntpSpiderPipeline.getFirstUrl()
        urlItem = {}
        urlItem.update({"id":result[0]})
        urlItem.update({"city":result[1]})
        urlItem.update({"area":result[2]})
        urlItem.update({"domain":result[3]})
        urlItem.update({"industry":result[4]})
        url = result[5]
        url = splitJointSearchUrl(url=url)
        urlItem.update({"url":url})
        # dont_filter=True 加上会进行去重过滤，有时会出现一些问题
        yield Request(url=url, callback=self.parseSearchList,headers=self.headers,meta={"urlItem":urlItem})

    def parseSearchList(self,response):
        print("返回：：  ",response.request.headers['User-Agent'])
        url = response.body_as_unicode()
        url = response.urljoin(url)
        self.log("请求到：：%s " % url)
        urlItem = response.meta['urlItem']

        city = urlItem['city']
        area = urlItem['area']
        domain = urlItem['domain']
        industry = urlItem['industry']
        searchUrl = urlItem['url']

        result = json.loads(response.text, encoding='utf-8')
        code = result.get('code')
        # 使用继承自scrapy的log
        self.log("请求搜索URL返回状态code:%s" % code)
        if code == 200:
            # result.get('data')是字典类型 data为list
            data = result.get('data').get('results')
            if len(data)>0:
                # data 是list类型
                for post in data:
                    item = EntpItem()
                    # post 是字典类型
                    company = post.get('company')
                    item['entpUi'] = company.get('number').strip()
                    url = company.get('url').strip()
                    item['url'] = company.get('url').strip()
                    item['entpName'] = company.get('name').strip()
                    item['personScope'] = company.get('size').get('name').strip()
                    item['entpType'] = company.get('type').get('name').strip()

                    item['city'] = city
                    item['area'] = area
                    domain = domain.replace("|","/")
                    item['domain'] = domain
                    item['industry'] = industry
                    time.sleep(random.randint(3,6))
                    self.log("PLEASE LOOK ITEM:%s" % item)
                    yield scrapy.Request(url=url, encoding='utf-8', callback=self.parseEntpDetail,
                                         meta={"item": item}, method="GET")
                # 此为判断是否有下一页，若有拼接URL请求。
                count = result['data']['count']
                if count > 90:
                    temUrls = searchUrl.split("start=")
                    if len(temUrls) > 1:
                        prevStartStr = temUrls[1].split("&")[0]
                        prevStart = int(prevStartStr)
                        if (prevStart + 90) <= count:
                            searchUrl = searchUrl.split("start=")[0]
                            searchUrl += "&start=" + str(prevStart + 90)
                            yield Request(url=searchUrl, callback=self.parseSearchList, meta={"urlItem": urlItem})
                    else:
                        searchUrl += "&start=90"
                        yield Request(url=searchUrl, callback=self.parseSearchList, meta={"urlItem": urlItem})
            else:
                pass
        else:
            self.log("请求搜索URL返回状态code:%s" % response.text)
            print(response.text)

    def parseEntpDetail(self,response):
        time.sleep(random.randint(3,4))
        soup = BeautifulSoup(response.text,"html.parser")
        entpItem = response.meta['item']
        entpName = entpItem['entpName']
        domain = entpItem['domain']
        industry = entpItem['industry']
        highlight = ""
        entpInfo = ""
        address = ""
        entpId = None
        dbDomain = ""
        dbIndustry = ""
        jobSearchUrl= ""
        website = ""
        try:
            urlDiv = soup.find("p", {"class": "overview__url"})
            if None != urlDiv:
                website = urlDiv.getText().strip()
        except Exception as e:
            print("企业主页网址获取不到")
            print(e)

        try:
            welfareUl = soup.find("p", {"class": "overview__welfare clearfix"})
            if None != welfareUl:
                wlis = welfareUl.findAll("li")
                if None != wlis:
                    for li in wlis:
                        highlight += "," + li.getText().strip()
                highlight = highlight[1:]
        except Exception as e:
            print("企业亮点获取不到")

        try:
            contentDiv = soup.find("div", {"class": "company-show__content"})
            if None != contentDiv:
                entpInfo = contentDiv.getText().strip()
        except Exception as e:
            contentDiv = soup.find("div", {"class": "company-show__content__description"})
            if None != contentDiv:
                entpInfo = contentDiv.getText().strip()
            print(e)
        else:
            print("企业详细介绍 没有报错")

        try:
            addressDiv = soup.find("p",{"class":"map-box__adress"})
            if None != addressDiv:
                address = addressDiv.text.strip()
        except Exception as e:
            print("企业地址获取不到")
            print(e)

        jobLIstDiv = soup.find("div",{"class":"more-job-btn mian-company__left-container__more-job-but"})
        if None != jobLIstDiv:
            jobListA = jobLIstDiv.find("a")
            jobSearchUrl = jobListA.get('href')

        # 判断数据库中是否已经有该企业信息
        items = self.zhilianEntpSpiderPipeline.existEntpFromDB(entpName)
        if len(items)>0:
            entpId = items[0]
            # 如果有对应的企业信息，对比详情、城市、地区、人员规模;将对应的职位信息删除再入库新的职位
            # id,entp_info,city,area,person_scope
            if None == entpInfo or "" == entpInfo:
                entpInfo = "" if items[1] == None else items[1]
            dbDomain = items[5]
            dbIndustry = items[6]

            if domain not in dbDomain:
                dbDomain = dbDomain+","+domain

            entpItem.update({"domain": dbDomain})
            if industry not in dbIndustry:
                dbIndustry = dbIndustry+","+industry

            entpItem.update({"industry": dbIndustry})
            entpItem.update({"id": entpId})
            entpItem.update({"entpInfo": entpInfo})
            entpItem.update({"highlight": highlight})
            print("修改的企业信息：：",entpItem)
            ###########################################
            self.zhilianEntpSpiderPipeline.updateEntp(entpItem)

        # 如果没有对应的企业信息，企业信息与职位信息都要入库
        else:
            entpItem.update({"website": website})
            entpItem.update({"address": address})
            entpItem.update({"highlight": highlight})
            entpItem.update({"entpInfo": entpInfo})
            entpItem.update({"domain": domain})
            print("添加的企业信息：：",entpItem)
            ###################################
            self.zhilianEntpSpiderPipeline.saveEntp(entpItem)
        # 此一步是将职位待采集的URL入库
        try:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            postSearchItem = {}
            postSearchItem.update({"entpName":entpName})
            postSearchItem.update({"entpId":entpId})
            postSearchItem.update({"entpDomain":dbDomain})
            postSearchItem.update({"entpIndustry":dbIndustry})
            postSearchItem.update({"url":jobSearchUrl})
            postSearchItem.update({"urlType":"0"})
            postSearchItem.update({"recordState":"1"})
            postSearchItem.update({"updateTime":now})
            self.zhilianEntpSpiderPipeline.saveSearchPostUrl(postSearchItem)
        except Exception as e:
            print(e)


def splitJointSearchUrl(url):
    # 1、生成一个随机32位数id
    md5 = hashlib.md5()
    id = str(random.random())
    md5.update(id.encode('utf-8'))
    random_id = md5.hexdigest()
    # 2、生成当前时间戳
    now_time = int(time.time() * 1000)
    # 3、生成随机6位数
    randomnumb = int(random.random() * 1000000)
    # 4、生成32位UUID x-zp-client-id:015a58ca-5b0a-4402-83bb-28db2b85e257
    client_id = str(uuid.uuid4())
    # 组合代码
    x_zp_page_request_id = str(random_id) + '-' + str(now_time) + '-' + str(randomnumb)
    url_v = round(random.random(), 8)
    "x-zp-client-id"
    url = url+"&x_zp_page_request_id="+x_zp_page_request_id+"&_v="+str(url_v)+"&x-zp-client-id="+client_id
    return url