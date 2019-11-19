# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class LuProfessorItem(scrapy.Item):
    name = scrapy.Field()
    domain = scrapy.Field()
    orgName = scrapy.Field()
    address = scrapy.Field()
    title = scrapy.Field()
    position = scrapy.Field()
    introduction = scrapy.Field()
    company = scrapy.Field()
    phone = scrapy.Field()
