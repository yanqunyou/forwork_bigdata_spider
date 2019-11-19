# -*- coding: utf-8 -*-
import scrapy


class LupingtaiProfessorSpider(scrapy.Spider):
    name = 'lupingtai_professor'
    allowed_domains = ['http://www.qiyekexie.com']
    start_urls = ['http://http://www.qiyekexie.com/']

    def parse(self, response):
        pass
