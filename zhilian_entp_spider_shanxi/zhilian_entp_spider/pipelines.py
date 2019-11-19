# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

import pymysql

class ZhilianEntpSpiderPipeline(object):

    def __init__(self):
        self.connect = pymysql.Connect(host="192.168.1.214",port=3306,user="spider",passwd="123456",db="forwork_ga",charset="utf8")
        self.cursor = self.connect.cursor()

    def getFirstUrl(self):
        sqlStr = "SELECT * FROM zhilian_entp_stay_url WHERE record_state = '1' ORDER BY update_time ASC LIMIT 1 "
        result = []
        try:
            self.cursor.execute(sqlStr)
            result = self.cursor.fetchone()
            self.connect.close()
        except Exception as e:
            print("获取URL失败！",e)
        finally:
            return result

    # 通过企业名称查询数据库
    def existEntpFromDB(self, entpName):
        searchSql = "SELECT id,entp_info,city,area,person_scope,`domain`,industry FROM zhilian_entp where entp_name =%s; " % entpName
        items = []
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

    # 职位列表信息入库(先判断库里有没有相关信息，有了修改，没有添加)
    def saveSearchPostUrl(self, postSearchItem):
        entpId = postSearchItem['entpId']
        searchSql = "SELECT * FROM zhilian_post_stay_url WHERE entp_id = %s;" % entpId
        saveSql = """
        INSERT INTO `zhilian_post_stay_url` 
            (`entp_id`, `entp_name`, `entp_domain`, `entp_indentry`, `url`, `url_type`, `update_time`, `record_state`) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        updateSql = """
        UPDATE zhilian_post_stay_url
        SET `entp_domain` = %s,entp_indentry = %s,url = %s where entp_id = %s;
        """
        try:
            self.cursor.execute(searchSql)
            results = self.cursor.fetchone()
            if None == results:
                self.cursor.execute(saveSql,(
                    postSearchItem['entpId'],
                    postSearchItem['entpName'],
                    postSearchItem['entpDomain'],
                    postSearchItem['entpIndentry'],
                    postSearchItem['url'],
                    postSearchItem['urlType'],
                    postSearchItem['updateTime'],
                    postSearchItem['recordState']
                ))
            else:
                self.cursor.execute(updateSql, (
                    postSearchItem['entpDomain'],
                    postSearchItem['entpIndentry'],
                    postSearchItem['url'],
                    postSearchItem['entpId']
                ))
            self.connect.commit()
        except Exception as e:
            print(e)

    def updateEntp(self, items):
        searchSql = (
            "UPDATE zhipin_entp SET `domain` = %s,industry = %s,entp_info = %s,city = %s,area=%s,person_scope = %s,highlight = %s where id = %s")

        try:
            self.cursor.execute(searchSql, (
                items['domain'],
                items['industry'],
                items['entpInfo'],
                items['city'],
                items['area'],
                items['personScope'],
                items['highlight'],
                items['id']
            ))
            self.connect.commit()
        except Exception as e:
            print(e)

    # 企业信息存入数据库
    def saveEntp(self, entpItem):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        sqlStr = """
        INSERT INTO `forwork_ga`.`zhilian_entp`
        (`entp_name`, `url`,`website`, `address`, `entp_info`, `entp_type`,`entp_ui`, 
        `highlight`, `industry`,  `person_scope`, `domain`, `record_status`, 
        `city`, `area`, `create_time`, `update_time`) 
        VALUES (%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s)
        """
        try:
            self.cursor.execute(sqlStr, (
                entpItem['entpName'], entpItem['url'], entpItem['website'], entpItem['address'],
                entpItem['entpInfo'], entpItem['entpType'], entpItem['entpUi'],
                entpItem['highlight'], entpItem['industry'], entpItem['personScope'], entpItem['domain'], '0',
                entpItem['city'], entpItem['area'], now, now
            ))
            self.connect.commit()
        except Exception as e:
            print(e)



