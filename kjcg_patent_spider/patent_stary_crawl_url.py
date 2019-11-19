# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         testKjcg
# Description:  
# Author:       forwork
# Date:         2019/8/12
#-------------------------------------------------------------------------------
import scrapy
from bs4 import BeautifulSoup
import time
import requests
import random
import json
import pymysql

baseUrl = "http://list.kjcg123.com:8080/wokejinews/news/queryAll"
basePtUrl = "http://list.kjcg123.com:8080/wokejinews/news/detail.html?type=2&id="

proxies = {
    "http":"117.191.11.79:80"
}

headers = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection":"keep-alive",
    "Content-Length":"59",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Host":"list.kjcg123.com:8080",
    "Origin":"http://list.kjcg123.com:8080",
    "Referer":"http://list.kjcg123.com:8080/wokejinews/news/list?type=1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest"
}

cookies = {
    "JSESSIONID":"6B237F358DD08BC606DE5C66BFCB60BC",
    "Hm_lvt_d11e62e2e2c8d774bb326bab95dd0a4d":"1565260336,1565573152"
}

params = {
    "title":"",
    "addr":"",
    "type":"2",  # 专利
    "category":"", # 类别（领域）
    "currentpage":"0",
    "countperpage":"10"
}

categorys = {
    "B110000":"电子信息技术",
    "B120000":"生物与新医药技术",
    "B130000":"航空航天技术",
    "B140000":"新材料技术",
    "B150000":"高新技术服务业及公共事业",
    "B160000":"新能源及节能技术",
    "B170000":"资源与环境工程技术",
    "B180000":"高端装备与先进制造",
    "B190000":"化学与化学工程技术",
    "B200000":"现代农业与食品产业技术",
    "B990000":"其他"
    }


mysqlContent = pymysql.connect(host='192.168.1.214',port=3306,db='forwork_ga',user='spider',passwd='123456',charset='utf8')
mysqlCursor = mysqlContent.cursor()


def insertAlonePatent(url):
    insertStr = """
            INSERT INTO `forwork_ga`.`alone_patent` (`url`) VALUES (%s)
    """

    try:
        mysqlCursor.execute(insertStr,(
            url
        ))
    except Exception as e:
        mysqlContent.rollback()
        print(e)
    finally:
        mysqlContent.commit()


cateKeys = list(categorys.keys())

for i in range(len(cateKeys)):
    for j in range(100):
        time.sleep(random.randint(3,6))
        # categorys.get(cateKeys[i])
        params.update({"category":cateKeys[i].replace("B","")})
        params.update({"currentpage":str(j)})
        print(params)
        response = requests.post(baseUrl,data=params,proxies= proxies,cookies=cookies,headers=headers)
        print(response.status_code)
        if response.status_code == 200 and response.text != None:
            result = json.loads(response.text)
            print(result)
            if 0 == result['code']:
                dataList = result['datas']
                if None != dataList and len(dataList)>0:
                    print("有结果1")
                    for pt in dataList:
                        id = pt['id']
                        url = basePtUrl+ str(id)
                        insertAlonePatent(url)
                else:
                    break
                    print("没有结果1")

            else:
                break
                print("没有结果")

