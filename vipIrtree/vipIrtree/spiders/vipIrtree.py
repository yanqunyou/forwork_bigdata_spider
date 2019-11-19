# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         VipIrtree
# Description:  
# Author:       yqy
# Date:         2019/1/3
# -------------------------------------------------------------------------------
import json
import random
import time

import scrapy
from scrapy import Request, FormRequest
from bs4 import BeautifulSoup
from vipIrtree.items import VipirtreeItem


class VipIrtreeSpider(scrapy.Spider):
    name = "vipIrtreeSpider"
    host = "http://www.irtree.com"
    startUrls = ['http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0101%23%e5%93%b2%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0201%23%e7%bb%8f%e6%b5%8e%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0202%23%e8%b4%a2%e6%94%bf%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0203%23%e9%87%91%e8%9e%8d%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0204%23%e7%bb%8f%e6%b5%8e%e4%b8%8e%e8%b4%b8%e6%98%93%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0301%23%e6%b3%95%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0302%23%e6%94%bf%e6%b2%bb%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0303%23%e7%a4%be%e4%bc%9a%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0304%23%e6%b0%91%e6%97%8f%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0305%23%e9%a9%ac%e5%85%8b%e6%80%9d%e4%b8%bb%e4%b9%89%e7%90%86%e8%ae%ba%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0401%23%e6%95%99%e8%82%b2%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0402%23%e4%bd%93%e8%82%b2%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0501%23%e4%b8%ad%e5%9b%bd%e8%af%ad%e8%a8%80%e6%96%87%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0502%23%e5%a4%96%e5%9b%bd%e8%af%ad%e8%a8%80%e6%96%87%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0503%23%e6%96%b0%e9%97%bb%e4%bc%a0%e6%92%ad%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0601%23%e5%8e%86%e5%8f%b2%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0701%23%e6%95%b0%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0702%23%e7%89%a9%e7%90%86%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0703%23%e5%8c%96%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0704%23%e5%a4%a9%e6%96%87%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0705%23%e5%9c%b0%e7%90%86%e7%a7%91%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0706%23%e5%a4%a7%e6%b0%94%e7%a7%91%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0707%23%e6%b5%b7%e6%b4%8b%e7%a7%91%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0708%23%e5%9c%b0%e7%90%83%e7%89%a9%e7%90%86%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0709%23%e5%9c%b0%e8%b4%a8%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0710%23%e7%94%9f%e7%89%a9%e7%a7%91%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0711%23%e5%bf%83%e7%90%86%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0712%23%e7%bb%9f%e8%ae%a1%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0801%23%e5%8a%9b%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0802%23%e6%9c%ba%e6%a2%b0%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0803%23%e4%bb%aa%e5%99%a8%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0804%23%e6%9d%90%e6%96%99%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0805%23%e8%83%bd%e6%ba%90%e5%8a%a8%e5%8a%9b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0806%23%e7%94%b5%e6%b0%94%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0807%23%e7%94%b5%e5%ad%90%e4%bf%a1%e6%81%af%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0808%23%e8%87%aa%e5%8a%a8%e5%8c%96%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0809%23%e8%ae%a1%e7%ae%97%e6%9c%ba%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0810%23%e5%9c%9f%e6%9c%a8%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0811%23%e6%b0%b4%e5%88%a9%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0812%23%e6%b5%8b%e7%bb%98%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0813%23%e5%8c%96%e5%b7%a5%e4%b8%8e%e5%88%b6%e8%8d%af%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0814%23%e5%9c%b0%e8%b4%a8%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0815%23%e7%9f%bf%e4%b8%9a%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0816%23%e7%ba%ba%e7%bb%87%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0817%23%e8%bd%bb%e5%b7%a5%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0818%23%e4%ba%a4%e9%80%9a%e8%bf%90%e8%be%93%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0819%23%e6%b5%b7%e6%b4%8b%e5%b7%a5%e7%a8%8b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0820%23%e8%88%aa%e7%a9%ba%e8%88%aa%e5%a4%a9%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0821%23%e5%85%b5%e5%99%a8%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0822%23%e6%a0%b8%e5%b7%a5%e7%a8%8b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0823%23%e5%86%9c%e4%b8%9a%e5%b7%a5%e7%a8%8b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0824%23%e6%9e%97%e4%b8%9a%e5%b7%a5%e7%a8%8b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0825%23%e7%8e%af%e5%a2%83%e7%a7%91%e5%ad%a6%e4%b8%8e%e5%b7%a5%e7%a8%8b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0826%23%e7%94%9f%e7%89%a9%e5%8c%bb%e5%ad%a6%e5%b7%a5%e7%a8%8b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0827%23%e9%a3%9f%e5%93%81%e7%a7%91%e5%ad%a6%e4%b8%8e%e5%b7%a5%e7%a8%8b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0828%23%e5%bb%ba%e7%ad%91%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0829%23%e5%ae%89%e5%85%a8%e7%a7%91%e5%ad%a6%e4%b8%8e%e5%b7%a5%e7%a8%8b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0830%23%e7%94%9f%e7%89%a9%e5%b7%a5%e7%a8%8b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0901%23%e6%a4%8d%e7%89%a9%e7%94%9f%e4%ba%a7%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0902%23%e8%87%aa%e7%84%b6%e4%bf%9d%e6%8a%a4%e4%b8%8e%e7%8e%af%e5%a2%83%e7%94%9f%e6%80%81%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0904%23%e5%8a%a8%e7%89%a9%e5%8c%bb%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0905%23%e6%9e%97%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0906%23%e6%b0%b4%e4%ba%a7%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de0907%23%e8%8d%89%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1001%23%e5%9f%ba%e7%a1%80%e5%8c%bb%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1002%23%e4%b8%b4%e5%ba%8a%e5%8c%bb%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1003%23%e5%8f%a3%e8%85%94%e5%8c%bb%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1004%23%e5%85%ac%e5%85%b1%e5%8d%ab%e7%94%9f%e4%b8%8e%e9%a2%84%e9%98%b2%e5%8c%bb%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1005%23%e4%b8%ad%e5%8c%bb%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1006%23%e4%b8%ad%e8%a5%bf%e5%8c%bb%e7%bb%93%e5%90%88%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1007%23%e8%8d%af%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1008%23%e4%b8%ad%e8%8d%af%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1009%23%e6%b3%95%e5%8c%bb%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1011%23%e6%8a%a4%e7%90%86%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1201%23%e7%ae%a1%e7%90%86%e7%a7%91%e5%ad%a6%e4%b8%8e%e5%b7%a5%e7%a8%8b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1202%23%e5%b7%a5%e5%95%86%e7%ae%a1%e7%90%86%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1204%23%e5%85%ac%e5%85%b1%e7%ae%a1%e7%90%86%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1205%23%e5%9b%be%e4%b9%a6%e6%83%85%e6%8a%a5%e4%b8%8e%e6%a1%a3%e6%a1%88%e7%ae%a1%e7%90%86%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1206%23%e7%89%a9%e6%b5%81%e7%ae%a1%e7%90%86%e4%b8%8e%e5%b7%a5%e7%a8%8b%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1209%23%e6%97%85%e6%b8%b8%e7%ae%a1%e7%90%86%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1301%23%e8%89%ba%e6%9c%af%e5%ad%a6%e7%90%86%e8%ae%ba%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1302%23%e9%9f%b3%e4%b9%90%e4%b8%8e%e8%88%9e%e8%b9%88%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1303%23%e6%88%8f%e5%89%a7%e4%b8%8e%e5%bd%b1%e8%a7%86%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1304%23%e7%be%8e%e6%9c%af%e5%ad%a6%e7%b1%bb',
                 'http://www.irtree.com/writer/writersearch.aspx?cf=ZY%3de1305%23%e8%ae%be%e8%ae%a1%e5%ad%a6%e7%b1%bb']

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Host": "www.irtree.com",
        "Cookie": "ASP.NET_SessionId=c9f5177c-e63e-47a4-ad08-c45e8c0eaea0",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36",
        "Referer": "http://www.irtree.com/writer/writerguide.aspx",
        "X-Requested-With": "XMLHttpRequest",
    }

    cookies = {
        "SelectedExportwriter": "%2C100000012242425%7C%E8%83%A1%E5%A4%A7%E4%B8%80%2C",
        "ASP.NET_SessionId": "6134cb7e-9c78-4608-9ddb-63919440bcf8",
        "LIBUSERCOOKIE": "Oosn4ui+3LLtqonRNbj8Ks0pJGpwtxkDIN4f3Lm7EtFQLbIeiFzb/pACjWyVcmiT8k0o8s8wP1d185xH4jjnuvHI66OZW16slJ7VLB4D5JBwF6ZU3zkev7AJkYgmMapTxTBrBQ/gXc4izn65sNx+mHEowOZj1glIz3jt9+kVnWAMyVpbv/qAVg==",
        "LIBUSERIDCOOKIE": "19047070",
        "LIBUSERNAMECOOKIE": "1533162363@qq.com",
        "bdshare_firstime": 1546507284307,
    }

    # 1.登录   1533162363 已经被禁...
    def start_requests(self):
        loginUrl = "http://www.irtree.com/user/login.aspx?"
        url = loginUrl + str(random.random())
        yield FormRequest(url=url,
                          formdata={
                              "username": "1055008931@qq.com",
                              "password": "yanqunyou123",
                              "operate": "NormalLogin"
                          },
                          method='GET',
                          headers=self.headers,
                          callback=self.afterLogin,
                          meta={"listUrl": self.startUrls[60]}  # 从61开始2.20 ==> 85
                          )

    # && 替补登录
    def login(self, listUrl):
        loginUrl = "http://www.irtree.com/user/login.aspx?"
        url = loginUrl + str(random.random())
        yield FormRequest(url=url,
                          formdata={
                              "username": "1055008931@qq.com",
                              "password": "yanqunyou123",
                              "operate": "NormalLogin"
                          },
                          method='GET',
                          headers=self.headers,
                          meta={"listUrl": listUrl}
                          )

    # 2.发送第一次list页面请求
    def afterLogin(self, reponse):
        result = json.loads(reponse.text)
        listUrl = reponse.meta["listUrl"]
        if result["success"]:
            yield Request(url=listUrl, callback=self.parse_page,
                          headers=self.headers, meta={"listUrl": listUrl})

    # 3. 目的是获取总页数，发送所有的分页请求
    def parse_page(self, response):
        listUrl = response.meta["listUrl"]
        soup = BeautifulSoup(response.text, "html.parser")
        # 获取总共页数，进行下一页循环
        tstr = soup.find("span", {"class": "total"}).getText()
        if tstr != None:
            pgnum = int(tstr[1:-1].replace(",", ""))
            #分页只到250页，后面显示不了
            if pgnum > 1:
                for i in range(250):
                    pgurl = "&page=" + str(i) + "&ids="
                    tmpUrl = listUrl + pgurl
                    time.sleep(random.randint(3,5))    #随机阻塞
                    yield Request(url=tmpUrl, headers=self.headers, callback=self.parse_list, cookies=self.cookies)

    # 4. 目的是接受所有的分页的请求，解析详情URL，发送请求
    def parse_list(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        pgcookies = self.cookies
        print("解析list： "+response.url)
        # 获取列表里面的详情URL
        dts = soup.findAll("dt")
        if len(dts) > 0:
            for dt in dts:
                href = dt.a.get("href")
                time.sleep(random.randint(1, 3))
                yield Request(url=self.host + href, headers=self.headers, callback=self.parse_detail, cookies=pgcookies)

    # 解析详情页
    def parse_detail(self, response):
        item = VipirtreeItem()
        url = response.url
        if "id=" in url:
            item['url'] = url
            soup = BeautifulSoup(response.text, "html.parser")
            str1 = soup.find("div", {"class", "summary"}).find("h1").getText()
            name = str1.split(" ")[0]
            org = str1.split(" ")[1]
            item['name'] = name
            item['org'] = org
            dds = soup.find("dl", {"class", "ranking"}).findAll("dd")
            if len(dds) > 0:
                ppRank = int(dds[0].find("span", {"class": "num"}).getText())
            else:
                ppRank = 0

            if len(dds) > 1:
                qtRank = int(dds[1].find("span", {"class": "num"}).getText())
            else:
                qtRank= 0

            item['paperRank'] = ppRank
            item['quoteRank'] = qtRank
            # 成就 信息
            data = soup.find("p", {"class": "data"})
            spans1 = data.findAll("span")
            spl1 =   len(spans1)
            if spl1 > 0:
                try:
                    paperNum = int(spans1[0].getText().strip().split("：")[1].replace(",", ""))
                    quoteNum = int(spans1[1].getText().strip().split("：")[1].replace(",", ""))
                except Exception as e:
                    paperNum = 0
                    quoteNum = 0
                item['paperNum'] = paperNum
                item['quoteNum'] = quoteNum
                if len(spans1) > 2:
                    hfactor = int(spans1[2].getText().strip().split("：")[1].replace(",", ""))
                    item['hfactor'] = hfactor
                else:
                    item['hfactor'] = 0

                if len(spans1)>3:
                    bdhx = int(spans1[3].getText().strip().split(":")[1].replace(",", ""))
                    item['bdhx'] = bdhx
                else:
                    item['bdhx'] = 0

                if len(spans1) >4:
                    ndhx = int(spans1[4].getText().strip().split(":")[1].replace(",", ""))
                    item['ndhx'] = ndhx
                else:
                    item['ndhx'] = 0

                if len(spans1) > 5:
                    rdfybkzl = int(spans1[5].getText().strip().split(":")[1].replace(",", ""))
                    item['rdfybkzl'] = rdfybkzl
                else:
                    item['rdfybkzl'] = 0


            # 研究主题
            subject = soup.find("p", {"class": "subject"})
            spans2 = subject.findAll("span")
            study_theme = ""
            if len(spans2) > 0:
                for i in range(len(spans2)):
                    study_theme += spans2[i].getText() + ","
                study_theme = study_theme[:-1]
            item['studyTheme'] = study_theme

            # 研究学科
            subject_buil = soup.find("div", {"class": "subject-build"})
            study_subject = ""
            if subject_buil != None:
                sublis = subject_buil.ul.findAll("li")
                if len(sublis) > 0:
                    sub = ""
                    quoteRank = ""
                    paperRank = ""
                    for li in sublis:
                        spans3 = li.findAll("span")
                        if spans3[0] != None:
                            sub = spans3[0].a.get("title").strip()
                        if spans3[1] != None:
                            paperRank = spans3[1].getText().strip()
                        if len(spans3)>2:
                            quoteRank = spans3[2].getText().strip()
                        study_subject += sub + ":" + paperRank + ":" + quoteRank + ","
                    study_subject = study_subject[:-1]
            item['studySubject'] = study_subject

            # 主要文献 main_docum
            article_list = soup.find("div", {"class": "article-list"})
            main_docum = ""
            if article_list != None:
                articleLis = article_list.ul.findAll("li")
                if len(articleLis) > 0:
                    for li in articleLis:
                        main_docum += li.a.get("title").strip() + ","
                    main_docum = main_docum[:-1]
            item['mainDocum'] = main_docum

            yield item

    def listToDict(self, cookie):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        [b'PHPSESSID=cc49664f5d570695d39fce6bbbdd1a6d; path=/',
        :return:
        '''
        itemDict = {}

        for item in cookie:
            str = item.decode("utf-8")
            items = str.split('; ')
            for it in items:
                index = it.index("=")
                key = it[:index]
                value = it[(index + 1):]
                itemDict[key] = value
        return itemDict

    def getRequestHeaders(self):
        timestamp = int(time.time())
        headers = self.headers
        return headers
