# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         parse_stay_spider_url
# Description:  
# Author:       forwork
# Date:         2019/7/26
#-------------------------------------------------------------------------------
import time
import pymysql

class LagouStaySpiderUrl(object):

    industrys = [
            {
                "code": "0002",
                "industry": "移动互联网",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0003",
                "industry": "电商",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0004",
                "industry": "金融",
                "domain": "金融业"
            },{
                "code": "0005",
                "industry": "企业服务",
                "domain": "商业服务"
            },{
                "code": "0006",
                "industry": "教育",
                "domain": "文体教育/工艺美术"
            },{
                "code": "0007",
                "industry": "文娱丨内容",
                "domain": "文化/传媒/娱乐/体育"
            },{
                "code": "0008",
                "industry": "游戏",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0009",
                "industry": "消费生活",
                "domain": "贸易/批发/零售/租赁业"
            },{
                "code": "0010",
                "industry": "硬件",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0011",
                "industry": "社交",
                "domain": "商业服务"
            },{
                "code": "0012",
                "industry": "旅游",
                "domain": "服务业"
            },{
                "code": "0013",
                "industry": "体育",
                "domain": "文化/传媒/娱乐/体育"
            },{
                "code": "0014",
                "industry": "汽车丨出行",
                "domain": "交通/运输/物流/仓储"
            },{
                "code": "0015",
                "industry": "物流丨运输",
                "domain": "交通/运输/物流/仓储"
            },{
                "code": "0016",
                "industry": "医疗丨健康",
                "domain": "服务业"
            },{
                "code": "0017",
                "industry": "广告营销",
                "domain": "商业服务"
            },{
                "code": "0018",
                "industry": "数据服务",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0019",
                "industry": "信息安全",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0020",
                "industry": "人工智能",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0021",
                "industry": "区块链",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0022",
                "industry": "物联网",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0023",
                "industry": "VR丨AR",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0024",
                "industry": "软件开发",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0025",
                "industry": "通讯电子",
                "domain": "IT/通信/电子/互联网"
            },{
                "code": "0026",
                "industry": "房产家居",
                "domain": "房地产,建筑业"
            }]

    areas = [
        '离石区',
        '柳林县'
        ]
    baseUrl = "https://www.lagou.com/jobs/list_?px=new&hy={0}&city=吕梁&district={1}&isShowMoreIndustryField=true#filterBox"


    def __init__(self):
        self.connect  = pymysql.connect(host="192.168.1.214",
                        port=3306,
                        db='forwork_shanxi_ga',
                        user='developer',
                        passwd='123123',
                        charset='utf8')
        self.cursor = self.connect.cursor()

    def parseLagouStayUrl(self):

        for indury in self.industrys:
            industry = indury['industry']
            domain = indury['domain']
            for area in self.areas:
                item = {}
                staryUrl = self.baseUrl.format(industry,area)
                item['city'] = "吕梁"
                item['area'] = area
                item['industry'] = industry
                item['domain'] = domain
                item['url'] = staryUrl
                item['urlType'] = "0"
                item['recordState'] = "1"
                self.saveStayUrl(item)

    def saveStayUrl(self,item):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            sqlStr = """
            INSERT INTO  lagou_stay_url  
            (`city`, `area`, `domain`, `industry`, `url`, `url_type`, `record_state`, `update_time`) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
            """
            self.cursor.execute(sqlStr,(
                item['city'],
                item['area'],
                item['domain'],
                item['industry'],
                item['url'],
                item['urlType'],
                item['recordState'],
                now,
            ))
        except Exception as e:
            self.connect.rollback()
        finally:
            self.connect.commit()


if __name__ == "__main__":
    spider = LagouStaySpiderUrl()
    spider.parseLagouStayUrl()
