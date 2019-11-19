# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scientistSpider.items import PaperItem, CoordinateItem
from scientistSpider.items import PatentItem
from scientistSpider.items import ProjectItem
from scientistSpider.items import SelfItem
from scientistSpider.items import TeamItem
from scientistSpider.items import TagItem
import time
import pymysql

class ScientistspiderPipeline(object):
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

        # 论文
        if isinstance(item, PaperItem):

            strSql = """
                       INSERT INTO `sc_paper`
                       (`uri`, `paper_name`,`paper_author`,`quote_num`,`periodical`)
                        VALUES 
                       (%s,%s,%s,%s,%s)
                     """
            try:
                # 插入数据
                self.cursor.execute(strSql,
                                    (item['uri'],
                                     item['paperName'],
                                     item['paperAuthor'],
                                     item['quoteNum'],
                                     item['periodical']
                                     ))
                # 提交sql语句
                self.connect.commit()
            except Exception as e:
                print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
        # 专利
        if isinstance(item, PatentItem):

            strSql = """
                   INSERT INTO `sc_patent`
                   (`uri`, `pathent_name`,`pathent_no`,`pathent_time`)
                    VALUES 
                   (%s,%s,%s,%s)
                   """
            try:
                # 插入数据
                self.cursor.execute(strSql,
                                    (item['uri'],
                                     item['pathentName'],
                                     item['pathentNo'],
                                     item['pathentTime']
                                     ))
                # 提交sql语句
                self.connect.commit()
            except Exception as e:
                print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
        # 项目
        if isinstance(item, ProjectItem):

            strSql = """
                        INSERT INTO `sc_project`
                        (`uri`, `project_name`,`project_leader`,`project_leader_org`, `project_fund`,`project_keyword`) 
                        VALUES 
                        (%s,%s,%s,%s,%s,%s)
                        """
            try:
                # 插入数据
                self.cursor.execute(strSql,
                                    (item['uri'],
                                     item['projectName'],
                                     item['projectLeader'],
                                     item['projectLeaderOrg'],
                                     item['projectFund'],
                                     item['projectKeyword']
                                     ))
                # 提交sql语句
                self.connect.commit()
            except Exception as e:
                print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")

            pass
        # 科学家
        if isinstance(item, SelfItem):
            strSql = """
            INSERT INTO `sc_self` 
            (`page_url`, `domain`,`uri`, `tag_cloud`, `sc_name`, `sc_org`, `sc_domain`, 
            `paper_num`,`quote_rate`,`H_factor`,`url_isgather`,`url_ispersistence`) 
            VALUES 
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            try:
                # 插入数据
                self.cursor.execute(strSql,
                                (item['pageUrl'],
                                 item['domain'],
                                 item['uri'],
                                 item['tagCloud'],
                                 item['scName'],
                                 item['scOrg'],
                                 item['scDomain'],
                                 item['paperNum'],
                                 item['quoteRate'],
                                 item['HFactor'],
                                 item['urlIsgather'],
                                 item['urlIspersistence']
                     ))
                # 提交sql语句
                self.connect.commit()
            except Exception as e:
                print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")

        # 团队
        if isinstance(item, TeamItem):
            strSql = """
                       INSERT INTO `sc_team` 
                       (`uri`, `t_url`,`t_name`, `t_org`, `t_h_factor`,`t_num`)  VALUES 
                       (%s,%s,%s,%s,%s,%s)
                       """
            try:
                # 插入数据
                self.cursor.execute(strSql,
                                    (item['uri'],
                                     item['tUrl'],
                                     item['tName'],
                                     item['tOrg'],
                                     item['tHFactor'],
                                     item['tNum']
                                     ))
                # 提交sql语句
                self.connect.commit()
            except Exception as e:
                print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")

        # 云标签
        if isinstance(item, TagItem):
            strSql = """
                       UPDATE `sc_self` SET `tag_cloud`=(%s) WHERE `uri` = (%s)
                       """
            try:
                # 插入数据
                self.cursor.execute(strSql,
                                    (item['uri'],
                                     item['tags']
                                     ))
                # 提交sql语句
                self.connect.commit()
            except Exception as e:
                print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")