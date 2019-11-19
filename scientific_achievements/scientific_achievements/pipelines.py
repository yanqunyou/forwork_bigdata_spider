# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import Request

from scientific_achievements.items import ScientificAchievementsItem
import time

class ScientificAchievementsPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = "192.168.1.213",
            port = 3306,
            db = "wt_achievements",
            user = "developer",
            passwd = "123123",
            charset = "utf8"
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        print(item)
        strSql = """
           INSERT INTO `gather_achievement` (
            `url`,
            `title`,
            `transfer_mode`,
            `domain`,
            `achievement_domain`,
            `achievement_stage`,
            `application_industry`,
            `who_is_finish`,
            `achievement_area`,
            `finish_org`,
            `result_content`,
            `patent_no`,
            `create_time`,
            `update_time`)
        VALUES
	    ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(strSql,(item['url'],
                                 item['title'],
                                 item['transferMode'],
                                 item['domain'],
                                 item['achievementDomain'],
                                 item['achievementStage'],
                                 item['applicationIndustry'],
                                 item['whoIsFinsh'],
                                 item['area'],
                                 item['finishOrg'],
                                 item['resultContent'],
                                 item['patentNo'],
                                 item['createTime'],
                                 item['updateTime']))

            self.connect.commit()
        except Exception as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
