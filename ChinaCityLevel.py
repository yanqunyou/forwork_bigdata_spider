# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         ChinaCityLevel

# Description:  中国城市分级别入库

# Author:       forwork
# Date:         2019/9/23
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

class ChinaCityLevelSpider(object):

    satrtUrl = "https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%9F%8E%E5%B8%82%E6%96%B0%E5%88%86%E7%BA%A7%E5%90%8D%E5%8D%95/12702007"

    firefoxPath = "D:\\software\\Firefox\\geckodriver.exe"

    def __init__(self):
        self.connect = pymysql.connect(host='192.168.1.214',
                                        port=3306,
                                        db='forwork_ga',
                                        user='developer',
                                        passwd='123123',
                                        charset='utf8')
        self.cursor = self.connect.cursor()

    def parse(self):

        citys = {
                    '玉溪市':'云南省',
                    '普洱市':'云南省',
                    '衡水市':'河北省',
                    '抚顺市':'辽宁省',
                    '四平市':'吉林省',
                    '汉中市':'陕西省',
                    '内江市':'四川省',
                    '漯河市':'河南省',
                    '新余市':'江西省',
                    '延安市':'陕西省',
                    '长治市':'山西省',
                    '云浮市':'广东省',
                    '昭通市':'云南省',
                    '达州市':'四川省',
                    '淮北市':'安徽省',
                    '濮阳市':'河南省',
                    '通化市':'吉林省',
                    '松原市':'吉林省',
                    '广元市':'四川省',
                    '鄂州市':'湖北省',
                    '荆门市':'湖北省',
                    '忻州市':'山西省',
                    '遂宁市':'四川省',
                    '朝阳市':'辽宁省',
                    '辽阳市':'辽宁省',
                    '广安市':'四川省',
                    '萍乡市':'江西省',
                    '阜新市':'辽宁省',
                    '吕梁市':'山西省',
                    '池州市':'安徽省',
                    '本溪市':'辽宁省',
                    '铁岭市':'辽宁省',
                    '自贡市':'四川省',
                    '白城市':'吉林省',
                    '白山市':'吉林省',
                    '雅安市':'四川省',
                    '酒泉市':'甘肃省',
                    '天水市':'甘肃省',
                    '晋城市':'山西省',
                    '随州市':'湖北省',
                    '临沧市':'云南省',
                    '鹤壁市':'河南省',
                    '安康市':'陕西省',
                    '庆阳市':'甘肃省',
                    '儋州市':'海南省',
                    '陇南市':'甘肃省',
                    '朔州市':'山西省',
                    '阳泉市':'山西省',
                    '张掖市':'甘肃省',
                    '辽源市':'吉林省',
                    '巴中市':'四川省',
                    '平凉市':'甘肃省',
                    '定西市':'甘肃省',
                    '商洛市':'陕西省',
                    '金昌市':'甘肃省',
                    '白银市':'甘肃省',
                    '铜川市':'陕西省',
                    '武威市':'甘肃省',
                    '海东市':'青海省',
                    '资阳市':'四川省',
                    '防城港市':'广西壮族自治区',
                    '呼伦贝尔市':'内蒙古自治区',
                    '葫芦岛市':'辽宁省',
                    '楚雄彝族自治州':'云南省',
                    '钦州市':'广西壮族自治区',
                    '黔西南布依族苗族自治州':'贵州省',
                    '湘西土家族苗族自治州':'湖南省',
                    '文山壮族苗族自治州':'云南省',
                    '贵港市':'广西壮族自治区',
                    '河池市':'广西壮族自治区',
                    '通辽市':'内蒙古自治区',
                    '凉山彝族自治州':'四川省',
                    '张家界市':'湖南省',
                    '来宾市':'广西壮族自治区',
                    '克拉玛依市':'新疆维吾尔自治区',
                    '崇左市':'广西壮族自治区',
                    '贺州市':'广西壮族自治区',
                    '锡林郭勒盟':'内蒙古自治区',
                    '巴彦淖尔市':'内蒙古自治区',
                    '兴安盟':'内蒙古自治区',
                    '鸡西市':'黑龙江省',
                    '迪庆藏族自治州':'云南省',
                    '攀枝花、阿坝藏族羌族自治州':'四川省',
                    '黑河市':'黑龙江省',
                    '双鸭山市':'黑龙江省',
                    '三门峡市':'河南省',
                    '乌兰察布市':'内蒙古自治区',
                    '伊犁哈萨克自治州':'新疆维吾尔自治区',
                    '哈密市':'新疆维吾尔自治区',
                    '海西蒙古族藏族自治州':'青海省',
                    '甘孜藏族自治州':'四川省',
                    '伊春市':'黑龙江省',
                    '乌海市':'内蒙古自治区',
                    '林芝市':'西藏自治区',
                    '怒江傈僳族自治州':'云南省',
                    '嘉峪关市':'甘肃省',
                    '鹤岗市':'黑龙江省',
                    '吴忠市':'宁夏回族自治区',
                    '昌吉回族自治州':'新疆维吾尔自治区',
                    '大兴安岭地区':'黑龙江省',
                    '巴音郭楞蒙古自治州':'新疆维吾尔自治区',
                    '日喀则市':'西藏自治区',
                    '阿拉善盟':'内蒙古自治区',
                    '阿克苏地区':'新疆维吾尔自治区',
                    '七台河市':'黑龙江省',
                    '石嘴山市':'宁夏回族自治区',
                    '吐鲁番市':'新疆维吾尔自治区',
                    '固原市':'宁夏回族自治区',
                    '山南市':'西藏自治区',
                    '临夏回族自治州':'甘肃省',
                    '喀什地区':'新疆维吾尔自治区',
                    '甘南藏族自治州':'甘肃省',
                    '昌都市':'西藏自治区',
                    '中卫市':'宁夏回族自治区',
                    '阿勒泰地区':'新疆维吾尔自治区',
                    '塔城地区':'新疆维吾尔自治区',
                    '博尔塔拉蒙古自治州':'新疆维吾尔自治区',
                    '海南藏族自治州':'青海省',
                    '克孜勒苏柯尔克孜自治州':'新疆维吾尔自治区',
                    '阿里地区':'西藏自治区',
                    '和田地区':'新疆维吾尔自治区',
                    '玉树藏族自治州':'青海省',
                    '那曲市':'西藏自治区',
                    '黄南藏族自治州':'青海省',
                    '海北藏族自治州':'青海省',
                    '果洛藏族自治州':'青海省',
                    '三沙市':'海南省'}


        keys = list(citys.keys())
        for i in range(len(keys)):
            item = {}
            item['city'] = keys[i]
            item['province'] = citys.get(keys[i])
            item['level'] = '5'
            self.save(item)

    def save(self,item):
        saveStr = "INSERT INTO `forwork_ga`.`china_city_level` (`city`, `province`, `city_level` ) VALUES (%s,%s,%s)"
        print(item)
        try:
            self.cursor.execute(saveStr,(
                item['city'],
                item['province'],
                item['level']
            ))
        except Exception as e:
            self.connect.rollback()
            print(e)
        finally:
            self.connect.commit()

if __name__ == "__main__":
    spider = ChinaCityLevelSpider()
    spider.parse()