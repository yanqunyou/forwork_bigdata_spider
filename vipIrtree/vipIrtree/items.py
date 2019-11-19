# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VipirtreeItem(scrapy.Item):
        url = scrapy.Field()
        name = scrapy.Field()
        org = scrapy.Field()
        paperRank = scrapy.Field()
        quoteRank = scrapy.Field()
        paperNum = scrapy.Field()
        quoteNum = scrapy.Field()
        hfactor = scrapy.Field()
        bdhx = scrapy.Field()
        ndhx = scrapy.Field()
        rdfybkzl = scrapy.Field()
        studyTheme = scrapy.Field()
        studySubject = scrapy.Field()
        mainDocum = scrapy.Field()