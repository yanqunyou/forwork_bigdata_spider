# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         dateFormatUtil
# Description:  
# Author:       forwork
# Date:         2019/7/25
#-------------------------------------------------------------------------------
import time
class  DateFormatUtil(object):

    # 输入字符串：7月20日 或  10:20  转出：2019-07-04 08:20:00
    def dateFormat4ZhilianPost(self, replaceTmp):
        try:
            if "月" in replaceTmp:
                timeDs = replaceTmp.split("月")
                month = timeDs[0].strip()
                date = timeDs[1].split("日")[0].strip()
                year = str(time.localtime().tm_year)
                timeStr = year + "-" + month + "-" + date + " 8:20"
            else:
                year = str(time.localtime().tm_year)
                month = str(time.localtime().tm_mon)
                date = str(time.localtime().tm_mday)
                timeDs = replaceTmp.split(":")
                hours = timeDs[0]
                minute = timeDs[1]
                timeStr = year + "-" + month + "-" + date + " " + hours + ":" + minute
            timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M")
            replaceTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
        except Exception as e:
            replaceTime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            print("生成职位修改时间报错啦！ ", e)
        finally:
            return replaceTime

    # 输入：7-28 输出 2019-07-28 10:00:00
    def dateFormat4WuyouPost(self,replaceTmp):
        timeDs = replaceTmp.split("-")
        month = timeDs[0].strip()
        date = timeDs[1].strip()
        year = str(time.localtime().tm_year)
        timeStr = year + "-" + month + "-" + date + " 10:00"
        timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M")
        replaceTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
        return replaceTime

