# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         strat
# Description:  
# Author:       forwork
# Date:         2018/12/19
#-------------------------------------------------------------------------------
import scrapy.cmdline as cmdline

# 启动 爬虫
cmdline.execute('scrapy crawl scientistSpider'.split())