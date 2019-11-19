# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         scientificAchievementsSpider
# Description:  
# Author:       forwork
# Date:         2019/2/22
#-------------------------------------------------------------------------------

import time

import scrapy
from bs4 import BeautifulSoup

from scientific_achievements.items import ScientificAchievementsItem


class ScientificAchievementsSpider(scrapy.Spider):
    name = "scientificAchievementsSpider"
    host = "www.whstr.org.cn"

    # list_headers
    '''
    Cookie: visitor_type=old; 53gid2=10978529207005; 53gid0=10978529207005; 53gid1=10978529207005; 53revisit=1550804145389; 53kf_61423570_from_host=www.whstr.org.cn; 53kf_61423570_keyword=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D5jHaIrROmIRd6G9C7LCfBYbXgwG8Nv7tjMA5qSn5DVu153LwuoQPouNpyI5tQxXE%26ie%3Dutf-8%26f%3D8%26tn%3Dbaidu%26wd%3D%25E6%25AD%25A6%25E6%25B1%2589%25E7%25A7%2591%25E6%258A%2580%25E6%2588%2590%25E6%259E%259C%25E7%25BD%2591%26oq%3D%2525E7%2525A7%252591%2525E6%25258A%252580%2525E6%252588%252590%2525E6%25259E%25259C%26rqlang%3Dcn%26inputT%3D7963; 53kf_61423570_land_page=https%253A%252F%252Fwww.whstr.org.cn%252F; kf_61423570_land_page_ok=1; Hm_lvt_4364cb9f3794283aeea3d7699d1ad9b0=1550804145; 53uvid=1; onliner_zdfq61423570=0; visitor_type=old; Hm_lpvt_4364cb9f3794283aeea3d7699d1ad9b0=1550806677
    '''
    list_headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Host":"www.whstr.org.cn",
        "Referer":"https://www.whstr.org.cn/tec/",
        "Upgrade-Insecure-Requests":"1"
        }
    # https://www.whstr.org.cn/search/tec/?p=2&hangye=0&mature=0&transfer=0&complete=0&lingyu=67&area=0
    list_param = "isysjj=&username=&hangye=0&lingyu=&lingyu={}&area=0&transfer=0&mature=0&complete=0&q=&p={}"

    detail_url_base = "https://www.whstr.org.cn"
    """
    应用行业：
    ['0', '87', '15', '64', '7', '40', '69', '105', '57', '89', '45', '1', '83', '78', '92', '71', '98', '74', '48', '36', '60']
    技术领域：
    ['0', '-1', '17', '67', '100', '139', '132', '1', '42', '81', '35', '122']
    所在地：
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
    转让方式：
    ['0', '1', '2', '3', '4', '5']
    成果阶段：
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    成果完成方：
    ['0', '1', '2', '3', '4', '5', '6', '7', '8']
    """
    # 应用行业
    hangyes = ['87', '15', '64', '7', '40', '69', '105', '57', '89', '45', '1', '83', '78', '92', '71', '98', '74', '48', '36', '60']
    # 领域
    domanins = [{'code': '0', 'value': '不限'}, {'code': '-1', 'value': '其他'}, {'code': '17', 'value': '生物'}, {'code': '67', 'value': '新能源'}, {'code': '100', 'value': '先进制造'}, {'code': '139', 'value': '高技术服务'}, {'code': '132', 'value': '海洋'}, {'code': '1', 'value': '信息'}, {'code': '42', 'value': '新材料'}, {'code': '81', 'value': '现代农业'}, {'code': '35', 'value': '航空航天'}, {'code': '122', 'value': '节能环保和资源综合利用'}]

    # 县市
    citys = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

    def start_requests(self):
        for dm in self.domanins:
            # 武汉科技成果转化平台 科技资源
            listUrl = "https://www.whstr.org.cn/search/tec/?"+self.list_param.format(dm.get('code'),0)

            yield scrapy.Request(url=listUrl,encoding="utf-8",method="GET",
                                 meta={"domain":dm.get('value')},
                                 callback=self.list_parse,
                                 headers=self.list_headers)


    def list_parse(self,response):
        listUrl = response.url
        domain = response.meta['domain']
        lus = listUrl.split("=")

        soup = BeautifulSoup(response.text,"html.parser")
        div = soup.find("div",{"class":"wh_tec_l"})
        # count:数据条数 page 当前页码
        count = int(div.p.em.getText())
        page = int(lus[len(lus)-1])
        to_url = ""
        nextPage = page+1

        rexPage = "p="+str(page)
        rexNextPage = "p="+str(nextPage)
        if count > nextPage*12:
            to_url = listUrl.replace(rexPage,rexNextPage)
            print("下一页：：：",to_url)
            yield scrapy.Request(url=to_url,encoding="utf-8",method="GET",
                                     callback=self.list_parse,meta={"domain":domain},
                                     headers=self.list_headers)
        lis = div.ul.findAll("li")
        for li in lis:
            item = ScientificAchievementsItem()
            detailUrl = li.a.get("href")
            title = ""
            transferMode = ""
            achievementStage = ""
            applicationIndustry = ""
            whoIsFinsh = ""
            area = ""
            finishOrg = ""

            span2 = li.find("span",{"class":"hur2"})
            if span2 != None:
                hur2as = span2.findAll("span")
                if hur2as != None:
                    title = hur2as[0].getText()
                    transferMode = hur2as[1].em.getText()
                    achievementStage = hur2as[3].em.getText()
                    applicationIndustry = hur2as[4].em.getText()
                    whoIsFinsh = hur2as[5].em.getText()

            span3 = li.find("span",{"class":"hur3"})
            if span3 != None:
                hur3s = span3.findAll("span")
                if hur3s != None:
                    area = hur3s[0].getText()
                    finishOrg = hur3s[1].getText()
            item['title'] = title
            item['transferMode'] = transferMode
            item['domain'] = domain
            item['achievementStage'] = achievementStage
            item['applicationIndustry'] = applicationIndustry
            item['whoIsFinsh'] = whoIsFinsh
            item['area'] = area
            item['finishOrg'] = finishOrg

            yield scrapy.Request(url=self.detail_url_base+detailUrl,
                                 method="GET",headers=self.list_headers,
                                 meta={"item":item},callback=self.detail_parse,
                                 encoding="utf-8")

    def detail_parse(self,response):
        url = response.url
        item = response.meta['item']
        soup = BeautifulSoup(response.text,"lxml")
        patentNo = ""
        resultContent = ""
        achievementDomain = ""

        mainDivs = soup.findAll("div",{"class":"main"})

        if mainDivs != None:
            for mainDiv in mainDivs:
                if mainDiv.find("div",{"class":"dx_DlbR"}) != None:

                    detailDiv = mainDiv.find("div",{"class":"xb_ga clearfix"})
                    if detailDiv != None:
                        mesDiv = detailDiv.find("div",{"class":"xb_gaa"})
                        if mesDiv != None:
                            dbrDiv = mesDiv.find("div",{"class":"dx_DlbR"})
                            if dbrDiv != None:
                                pps = dbrDiv.findAll("p")
                                if pps != None:
                                    patentNo = "" if pps[1].em.getText() == None else pps[1].em.getText()
                                    achievementDomain = "" if pps[3].em.getText() == None else pps[3].em.getText()

                    dlakDiv = mainDiv.find("div",{"class":"dx_Dlak"})
                    if dlakDiv != None:
                        conDiv = dlakDiv.find("div",{"class":"dx_Dlc"})
                        if conDiv != None:
                            conps = conDiv.findAll("p")
                            for p in conps:
                                resultContent += p.getText().strip()

        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['url'] = url
        item['patentNo'] = patentNo
        item['achievementDomain'] = achievementDomain
        item['resultContent'] = resultContent.replace(")","）").replace("(","（").replace("\n","")
        item['createTime'] = now
        item['updateTime'] = now
        yield item
