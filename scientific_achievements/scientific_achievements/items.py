# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 成果item
class ScientificAchievementsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    transferMode = scrapy.Field() # 成果转让方式
    domain = scrapy.Field() # 按照领域来搜索条件
    achievementDomain = scrapy.Field() # 成果详情中技术领域（细分）
    achievementStage = scrapy.Field() # 成果阶段
    applicationIndustry = scrapy.Field() # 应用行业
    whoIsFinsh = scrapy.Field() # 成果完成方
    area = scrapy.Field() # 成果完成机构所在地区
    finishOrg = scrapy.Field() # 成果完成机构
    resultContent = scrapy.Field() # 成果内容简介
    patentNo = scrapy.Field() # 专利号
    createTime = scrapy.Field()
    updateTime = scrapy.Field()

class ImageItem(scrapy.Item):
    url = scrapy.Field()
    picture = scrapy.Field()
    pictureName = scrapy.Field()
    picturePath = scrapy.Field()




