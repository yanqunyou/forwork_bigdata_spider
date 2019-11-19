# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class VipirtreePipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='192.168.1.213',
            port=3306,
            db='test',
            user='developer',
            passwd='123123',
            charset='utf8')
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        print("添加到数据库：：：", item)
        # 数据库的操作
        sqlStr = """
                    INSERT INTO `vip_irtree` 
                    (`url`, `name`, `org`, `paper_rank`, `quote_rank`, `paper_num`,
                     `quote_num`, `hfactor`, `bdhx`, `ndhx`, `rdfybkzl`, `study_theme`, 
                     `study_subject`, `main_docum`, `url_isgather`, `url_ispersistence`) 
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        try:
            # 插入数据
            self.cursor.execute(sqlStr,
                (item['url'],
                 item['name'],
                 item['org'],
                 item['paperRank'],
                 item['quoteRank'],
                 item['paperNum'],
                 item['quoteNum'],
                 item['hfactor'],
                 item['bdhx'],
                 item['ndhx'],
                 item['rdfybkzl'],
                 item['studyTheme'],
                 item['studySubject'],
                 item['mainDocum'],
                 "1",
                 "1"
                 ))
            # 提交sql语句
            self.connect.commit()
        except Exception as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里",item['url'])