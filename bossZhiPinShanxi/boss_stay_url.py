# _*_ coding=utf-8 _*_
import pymysql
import json
import time

baseUrl ="https://www.zhipin.com/i{0}-c101101100/b_{1}"

areas = [
    "汾阳市",
    "离石区",
    "文水县",
    "孝义市",
    "交城县",
    "兴县",
    "柳林县",
    "中阳县",
    "岚县",
    "方山县"
]

industrys = [{"key": "100001", "domain": "互联网/IT/电子/通信", "industry": "互联网/电子商务"},
             {"key": "100002", "domain": "互联网/IT/电子/通信", "industry": "网络游戏"},
             {"key": "100003", "domain": "文化/体育/娱乐", "industry": "媒体/出版/影视/文化传播"},
             {"key": "100004", "domain": "专业服务", "industry": "广告/会展/公关"},
             {"key": "100005", "domain": "互联网/IT/电子/通信", "industry": "IT服务(系统/数据/维护)"},
             {"key": "100006", "domain": "卫生及社会工作", "industry": "医疗/护理/美容/保健/卫生服务"},
             {"key": "100007", "domain": "生活服务", "industry": "生活服务"},
             {"key": "100008", "domain": "互联网/IT/电子/通信", "industry": "互联网/电子商务"},
             {"key": "100009", "domain": "生活服务", "industry": "旅游/度假"},
             {"key": "100010", "domain": "互联网/IT/电子/通信", "industry": "IT服务(系统/数据/维护)"},
             {"key": "100011", "domain": "文化/体育/娱乐", "industry": "媒体/出版/影视/文化传播"},
             {"key": "100012", "domain": "教育培训/科研", "industry": "教育/培训/院校"},
             {"key": "100013", "domain": "互联网/IT/电子/通信", "industry": "通信/电信/网络设备"},
             {"key": "100014", "domain": "专业服务", "industry": "专业服务/咨询(财会/法律/人力资源等)"},
             {"key": "100015", "domain": "专业服务", "industry": "外包服务,中介服务"},
             {"key": "100016", "domain": "互联网/IT/电子/通信", "industry": "IT服务(系统/数据/维护)"},
             {"key": "100018", "domain": "互联网/IT/电子/通信", "industry": "计算机硬件"},
             {"key": "100019", "domain": "互联网/IT/电子/通信", "industry": "通信/电信/网络设备"},
             {"key": "100020", "domain": "互联网/IT/电子/通信", "industry": "互联网/电子商务"},
             {"key": "100021", "domain": "互联网/IT/电子/通信", "industry": "计算机软件"},
             {"key": "100024", "domain": "互联网/IT/电子/通信", "industry": "通信/电信/网络设备"},
             {"key": "100101", "domain": "专业服务", "industry": "广告/会展/公关"},
             {"key": "100206", "domain": "金融业", "industry": "基金/证券/期货/投资"},
             {"key": "100502", "domain": "交通运输/仓储/物流", "industry": "物流/仓储"},
             {"key": "100504", "domain": "批发/零售/贸易", "industry": "贸易/进出口"},
             {"key": "100601", "domain": "专业服务", "industry": "专业服务/咨询(财会/法律/人力资源等)"},
             {"key": "100702", "domain": "房地产,建筑业", "industry": "房地产/建筑/建材/工程"},
             {"key": "100801", "domain": "制造业", "industry": "汽车/摩托车"},
             {"key": "101304", "domain": "农/林/牧/渔", "industry": "其他"}]


class BossStayUrl(object):

    def __init__(self):
        self.connect = pymysql.connect(host="192.168.1.214",port=3306,user="developer",password="123123",db="forwork_shanxi_ga",charset="utf8")
        self.cursor = self.connect.cursor()

    # baseUrl ="https://www.zhipin.com/i{0}-c101200100/b_{1}"
    def parseStayUrl(self):
        for ind in industrys:
            for ct in areas:
                stayItem = {}
                code = ind['key']
                domain = ind['domain']
                industry = ind['industry']
                area = ct
                url = baseUrl.format(code,area)
                stayItem['url'] = url
                stayItem['area'] = area
                stayItem['industry'] = industry
                stayItem['domain'] = domain
                stayItem['city'] = "吕梁"
                stayItem['code'] = code
                stayItem['urlType'] = "0"
                stayItem['recordState'] = "1"
                print(stayItem)
                self.saveStayUrl(stayItem)

    def saveStayUrl(self,stayItem):
        now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        saveSql = """
        INSERT INTO `forwork_shanxi_ga`.`boss_stay_url` 
        ( `city`, `area`, `domain`, `industry`, `url`,
         `url_type`, `record_state`, `update_time`)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
        """
        try:
            self.cursor.execute(saveSql,(
                stayItem['city'],
                stayItem['area'],
                stayItem['domain'],
                stayItem['industry'],
                stayItem['url'],
                stayItem['urlType'],
                stayItem['recordState'],
                now
            ))
        except Exception as e:
            self.connect.rollback()
            print(e)
        finally:
            self.connect.commit()


if __name__ == "__main__":
    bossStayUrl = BossStayUrl()
    bossStayUrl.parseStayUrl()
    bossStayUrl.connect.close()
