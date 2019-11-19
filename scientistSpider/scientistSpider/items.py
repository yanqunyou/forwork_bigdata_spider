# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoordinateItem(scrapy.Item):
    uri = scrapy.Field()
    coordinate = scrapy.Field()


class PaperItem(scrapy.Item):
    uri = scrapy.Field()
    paperName = scrapy.Field()
    paperAuthor = scrapy.Field()
    quoteNum = scrapy.Field()
    periodical = scrapy.Field()


class PatentItem(scrapy.Item):
    uri = scrapy.Field()
    pathentName = scrapy.Field()
    pathentNo = scrapy.Field()
    pathentTime = scrapy.Field()


class ProjectItem(scrapy.Item):
    uri = scrapy.Field()
    projectName = scrapy.Field()
    projectLeader = scrapy.Field()
    projectLeaderOrg = scrapy.Field()
    projectFund = scrapy.Field()
    projectKeyword = scrapy.Field()


class SelfItem(scrapy.Item):
    uri = scrapy.Field()
    domain = scrapy.Field()
    tagCloud = scrapy.Field()
    pageUrl = scrapy.Field()
    scName = scrapy.Field()
    scOrg = scrapy.Field()
    scDomain = scrapy.Field()
    urlIspersistence = scrapy.Field()
    urlIsgather = scrapy.Field()
    paperNum = scrapy.Field()
    quoteRate = scrapy.Field()
    HFactor = scrapy.Field()
    tagCloud = scrapy.Field()


class TeamItem(scrapy.Item):
    uri = scrapy.Field()
    tUrl = scrapy.Field()
    tName = scrapy.Field()
    tOrg = scrapy.Field()
    tHFactor = scrapy.Field()
    tNum = scrapy.Field()


class TagItem(scrapy.Item):
    uri = scrapy.Field()
    tags = scrapy.Field()
