# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         byCityParseSearchUrls
# Description:  智联招聘---这是根据特定的城市，生成职位搜索URL
# Author:       forwork
# Date:         2019/7/18
#-------------------------------------------------------------------------------
import hashlib
import random
import time
import pymysql
import logging
import requests
import json
import uuid


class QianChengwuyouParseSearchUrl(object):
    # 领域
    industrys = [ {
	'code': '01',
	'industry': '计算机软件',
	'domain': '互联网/IT/电子/通信'
}, {
	'code': '37',
	'industry': '计算机硬件',
	'domain': '互联网/IT/电子/通信'
}, {
	'code': '38',
	'industry': '计算机服务(系统、数据服务、维修)',
	'domain': '互联网/IT/电子/通信'
}, {
	'code': '31',
	'industry': '通信/电信/网络设备',
	'domain': '互联网/IT/电子/通信'
}, {
	'code': '39',
	'industry': '通信/电信运营、增值服务',
	'domain': '互联网/IT/电子/通信'
}, {
	'code': '32',
	'industry': '互联网/电子商务',
	'domain': '互联网/IT/电子/通信'
}, {
	'code': '40',
	'industry': '网络游戏',
	'domain': '互联网/IT/电子/通信'
}, {
	'code': '02',
	'industry': '电子技术/半导体/集成电路',
	'domain': '互联网/IT/电子/通信'
}, {
	'code': '35',
	'industry': '仪器仪表/工业自动化',
	'domain': '互联网/IT/电子/通信'
}, {
	'code': '41',
	'industry': '会计/审计',
	'domain': '专业服务'
}, {
	'code': '03',
	'industry': '金融/投资/证券',
	'domain': '金融业'
}, {
	'code': '42',
	'industry': '银行',
	'domain': '金融业'
}, {
	'code': '43',
	'industry': '保险',
	'domain': '金融业'
}, {
	'code': '62',
	'industry': '信托/担保/拍卖/典当',
	'domain': '金融业'
}, {
	'code': '04',
	'industry': '贸易/进出口',
	'domain': '批发/零售/贸易'
}, {
	'code': '22',
	'industry': '批发/零售',
	'domain': '批发/零售/贸易'
}, {
	'code': '05',
	'industry': '快速消费品(食品、饮料、化妆品)',
	'domain': '批发/零售/贸易'
}, {
	'code': '06',
	'industry': '服装/纺织/皮革',
	'domain': '制造业'
}, {
	'code': '44',
	'industry': '家具/家电/玩具/礼品',
	'domain': '批发/零售/贸易'
}, {
	'code': '60',
	'industry': '奢侈品/收藏品/工艺品/珠宝',
	'domain': '批发/零售/贸易'
}, {
	'code': '45',
	'industry': '办公用品及设备',
	'domain': '批发/零售/贸易'
}, {
	'code': '14',
	'industry': '机械/设备/重工',
	'domain': '制造业'
}, {
	'code': '33',
	'industry': '汽车及零配件',
	'domain': '制造业'
}, {
	'code': '08',
	'industry': '制药/生物工程',
	'domain': '制造业'
}, {
	'code': '46',
	'industry': '医疗/护理/卫生',
	'domain': '卫生及社会工作'
}, {
	'code': '47',
	'industry': '医疗设备/器械',
	'domain': '制造业'
}, {
	'code': '12',
	'industry': '广告',
	'domain': '专业服务'
}, {
	'code': '48',
	'industry': '公关/市场推广/会展',
	'domain': '专业服务'
}, {
	'code': '49',
	'industry': '影视/媒体/艺术/文化传播',
	'domain': '文化/体育/娱乐'
}, {
	'code': '13',
	'industry': '文字媒体/出版',
	'domain': '文化/体育/娱乐'
}, {
	'code': '15',
	'industry': '印刷/包装/造纸',
	'domain': '文化/体育/娱乐'
}, {
	'code': '26',
	'industry': '房地产',
	'domain': '房地产'
}, {
	'code': '09',
	'industry': '建筑/建材/工程',
	'domain': '建筑业'
}, {
	'code': '50',
	'industry': '家居/室内设计/装潢',
	'domain': '建筑业'
}, {
	'code': '51',
	'industry': '物业管理/商业中心',
	'domain': '房地产'
}, {
	'code': '34',
	'industry': '中介服务',
	'domain': '专业服务'
}, {
	'code': '07',
	'industry': '专业服务(咨询、人力资源、财会)',
	'domain': '专业服务'
}, {
	'code': '59',
	'industry': '外包服务',
	'domain': '专业服务'
}, {
	'code': '52',
	'industry': '检测，认证',
	'domain': '专业服务'
}, {
	'code': '18',
	'industry': '法律',
	'domain': '专业服务'
}, {
	'code': '23',
	'industry': '教育/培训/院校',
	'domain': '教育培训/科研'
}, {
	'code': '24',
	'industry': '学术/科研',
	'domain': '教育培训/科研'
}, {
	'code': '63',
	'industry': '租赁服务',
	'domain': '专业服务'
}, {
	'code': '11',
	'industry': '餐饮业',
	'domain': '生活服务'
}, {
	'code': '53',
	'industry': '酒店/旅游',
	'domain': '生活服务'
}, {
	'code': '17',
	'industry': '娱乐/休闲/体育',
	'domain': '文化/体育/娱乐'
}, {
	'code': '54',
	'industry': '美容/保健',
	'domain': '卫生及社会工作'
}, {
	'code': '27',
	'industry': '生活服务',
	'domain': '生活服务'
}, {
	'code': '21',
	'industry': '交通/运输/物流',
	'domain': '交通运输/仓储/物流'
}, {
	'code': '55',
	'industry': '航天/航空',
	'domain': '交通运输/仓储/物流'
}, {
	'code': '19',
	'industry': '石油/化工/矿产/地质',
	'domain': '能源/环保/矿产'
}, {
	'code': '16',
	'industry': '采掘业/冶炼',
	'domain': '能源/环保/矿产'
}, {
	'code': '36',
	'industry': '电气/电力/水利',
	'domain': '能源/环保/矿产'
}, {
	'code': '61',
	'industry': '新能源',
	'domain': '能源/环保/矿产'
}, {
	'code': '56',
	'industry': '原材料和加工',
	'domain': '能源/环保/矿产'
}, {
	'code': '28',
	'industry': '政府/公共事业',
	'domain': '公共管理/社会保障'
}, {
	'code': '57',
	'industry': '非营利组织',
	'domain': '公共管理/社会保障'
}, {
	'code': '20',
	'industry': '环保',
	'domain': '能源/环保/矿产'
}, {
	'code': '29',
	'industry': '农/林/牧/渔',
	'domain': '农/林/牧/渔'
}, {
	'code': '58',
	'industry': '多元化业务集团公司',
	'domain': '公共管理/社会保障'
}
]

    city = "吕梁"

    # re
    urlBase = "https://search.51job.com/list/211200,000000,0000,{0},9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="

    def __init__(self):
        self.connect = pymysql.connect(
            host='192.168.1.214',
            port=3306,
            db='forwork_shanxi_ga',
            user='developer',
            passwd='123123',
            charset='utf8')
        self.cursor = self.connect.cursor()


    def wuhanSearchUrls(self):
        for inItem in self.industrys:
            industryCode = inItem['code']
            industry = inItem['industry']
            domain = inItem['domain']
            item = {}
            item['city'] = self.city
            item['domain'] = domain
            item['industry'] = industry
            item['urlType'] = "0"
            item['url'] = self.urlBase.format(industryCode)
            item['recordState'] = "1"
            print(item)
            self.save(item)


    def save(self,item):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sqlStr = """
            INSERT INTO `qianchengwuyou_stay_url` 
            (`city`, `domain`, `industry`, `url`, `url_type`, `record_state`,`update_time`)
             VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(sqlStr,(
                item['city'],
                item['domain'],
                item['industry'],
                item['url'],
                item['urlType'],
                item['recordState'],
                now
            ))
            self.connect.commit()
        except Exception as e:
            print(e)


    def getFirstUrl(self):
        sqlStr = "SELECT * FROM qianchengwuyou_stay_url WHERE record_state = '1' ORDER BY update_time ASC LIMIT 1 "
        result = []
        try:
            self.cursor.execute(sqlStr)
            result = self.cursor.fetchone()
            self.connect.close()
        except Exception as e:
            print("获取URL失败！",e)
        finally:
            return result


if __name__ == "__main__":
    spider = QianChengwuyouParseSearchUrl()
    result = spider.wuhanSearchUrls()
