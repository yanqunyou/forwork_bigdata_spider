# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         start
# Description:  
# Author:       forwork
# Date:         2019/1/3
#-------------------------------------------------------------------------------
from scrapy import cmdline

# 启动 爬虫
cmdline.execute('scrapy crawl vipIrtreeSpider'.split())