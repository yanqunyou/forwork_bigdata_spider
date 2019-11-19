# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         zhilian_entp_spider
# Description:  
# Author:       forwork
# Date:         2019/7/19
#-------------------------------------------------------------------------------
import hashlib
import random

import scrapy
from scrapy import Request
import time
import json
from bs4 import BeautifulSoup
from zhilian_entp_spider.items import ZhilianEntpSpiderItem as EntpItem

from zhilian_entp_spider.pipelines import ZhilianEntpSpiderPipeline

def splitJointSearchUrl(url):
    # 1、生成一个随机32位数id
    md5 = hashlib.md5()
    id = str(random.random())
    md5.update(id.encode('utf-8'))
    random_id = md5.hexdigest()
    # 2、生成当前时间戳
    now_time = int(time.time() * 1000)
    # 3、生成随机6位数
    randomnumb = int(random.random() * 1000000)
    # 组合代码
    x_zp_page_request_id = str(random_id) + '-' + str(now_time) + '-' + str(randomnumb)
    url_v = round(random.random(), 8)
    url = url+"&x_zp_page_request_id="+x_zp_page_request_id+"&_v="+str(url_v)
    return url

class ZhilianEntpSpider(scrapy.Spider):

    name = "zhilian_entp_spider11111"
    host = "https://fe-api.zhaopin.com"
    allowed_domains = ['zhaopin.com']
    # custom_settings = {
    #     'LOG_LEVEL': 'INFO',  # 减少Log输出量，仅保留必要的信息
    #     # ...... 在爬虫内部用custom_setting可以让这个配置信息仅对这一个爬虫生效
    # }
    start_urls = [
    ]

    zhilianEntpSpiderPipeline = ZhilianEntpSpiderPipeline()
    def parse(self, response):

        yield Request(url=response.url, callback=self.parseSearchList,meta={},dont_filter=True)

    def parseSearchList(self,response):
        response.request.headers.getlist("Cookie")
        result = json.loads(response.text, encoding='utf-8')
        code = result.get('code')
        data = result.get('data').get('results')
        print(code)
        print(data)