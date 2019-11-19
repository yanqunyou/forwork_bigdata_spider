# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class LuProfessorPipeline(object):
    def __init__(self):
        self.connect = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",
                        passwd="root",db="lupingtai",charset="utf8")
        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        strSql = """
        INSERT INTO `lp_professor` 
        (`name`, `domain`, `org_name`, `address`, `title`, 
        `position`, `introduction`, `company`, `phone`) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(strSql,{
                                    item['name'],
                                    item['domain'],
                                    item['orgName'],
                                    item['address'],
                                    item['title'],
                                    item['position'],
                                    item['introduction'],
                                    item['company'],
                                    item['phone']
                                        })
            self.connect.commit()
        except Exception as e:
            print e
