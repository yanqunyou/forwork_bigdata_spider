# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymysql

class DaoshiSpiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            port=3306,
            db='test',
            user='root',
            passwd='root',
            charset='utf8')
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 数据库的操作
        sqlStr ="""
        INSERT INTO `ga_talent` 
        (`url`, `tid`, `name`, `sex`, `org_name`, `title`,
         `domain`, `telephone`, `email`, `address`, `highest_edu`,
         `create_time`, `update_time`)
         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                     """
        try:
            # 插入数据
            self.cursor.execute(sqlStr,
                (item['url'],
                 item['tid'],
                 item['name'],
                 item['sex'],
                 item['orgName'],
                 item['title'],
                 item['domain'],
                 item['telephone'],
                 item['email'],
                 item['address'],
                 item['highestEdu'],
                 now,
                 now
                 ))
            # 提交sql语句
            self.connect.commit()
        except Exception as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里",item['url'])
