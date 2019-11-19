# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class ZhilianEntpSpiderItem(Item):
    entpName = Field()
    url = Field()
    entpUi = Field()
    personScope = Field()
    entpType = Field()
    website = Field()
    address = Field()
    entpInfo = Field()
    highlight = Field()
    industry = Field()
    domain = Field()
    city = Field()
    area = Field()
    recordStatus = Field()

class ZhiLianPostSearchItem(Item):
    entpId = Field()
    entpName = Field()
    entpDomain = Field()
    entpIndentry = Field()
    url = Field()
    urlType = Field()
    updateTime = Field()
    recordState = Field()

class ZhiLianEntpStaySearchItem(Item):
    city = Field()
    area = Field()
    domain = Field()
    indentry = Field()
    url = Field()
    urlType = Field()
    updateTime = Field()
    recordState = Field()
