# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         start
# Description:  
# Author:       forwork
# Date:         2019/7/19
#-------------------------------------------------------------------------------
import scrapy.cmdline as cmdline
# 启动 爬虫
cmdline.execute('scrapy crawl zhilian_entp_spider'.split())