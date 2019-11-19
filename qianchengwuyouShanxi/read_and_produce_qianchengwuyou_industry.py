# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         read_and_produce_qianchengwuyou_industry
# Description:  
# Author:       forwork
# Date:         2019/9/27
#-------------------------------------------------------------------------------
import pymysql
import time
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType, Proxy
from selenium.webdriver.support.select import By
import random
import xlrd,xlwt
from xlutils.copy import copy


# file = 'C:\\Users\\forwork\\Desktop\\大数据平台数据分析及excel\\所有数据融合所需的操作\\前程无忧与拉钩的领域与智联领域的对应关系\\abb.xls'
file = 'E:\\PythonData\\领域对应关系.xls'
wb = xlrd.open_workbook(filename=file)#打开文件
sheet1 = wb.sheet_by_index(0)#通过索引获取表格
# rows = sheet1.row_values(2)#获取行内容
codes = sheet1.col_values(0)#获取列内容
industrys = sheet1.col_values(1)#获取列内容
domains = sheet1.col_values(2)#获取列内容

new_industrys = []

for i in range(len(industrys)):
    item = {}
    item['code'] = codes[i]
    item['industry'] = industrys[i]
    item['domain'] = domains[i]
    new_industrys.append(item)
print(new_industrys)


