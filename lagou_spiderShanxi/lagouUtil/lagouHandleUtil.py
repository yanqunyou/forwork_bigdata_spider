# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         lagouHandleUtil
# Description:  
# Author:       forwork
# Date:         2019/7/29
#-------------------------------------------------------------------------------
from selenium import webdriver


class LagouHandleUntl(object):

    def switch_SearchPage_To_EntpPage(self,driver):
        allHandles = driver.window_handles
        if len(allHandles) == 2:
            driver.switch_to.window(allHandles[-1])
        # 将多余的窗口关闭
        elif len(allHandles) > 2:
            for hd in allHandles:
                if hd != allHandles[0] and hd != allHandles[-1]:
                    driver.switch_to.window(hd)
                    driver.close()
            # 将窗口转换到最后一个窗口
            driver.switch_to.window(allHandles[-1])

    def switch_EntpPage_To_SearchPage(self,driver):
        allHandles = driver.window_handles
        for hd in allHandles:
            if hd != allHandles[0]:
                driver.switch_to.window(hd)
                driver.close()
        # 将窗口转换到最后一个窗口
        driver.switch_to.window(allHandles[0])

    def switch_EntpPage_To_Post(self,driver):
        allHandles = driver.window_handles
        if len(allHandles)==3:
            driver.switch_to.window(allHandles[2])
        else:
            for hd in allHandles:
                if hd != allHandles[0] and hd != allHandles[1] and hd != allHandles[-1]:
                    driver.switch_to.window(hd)
                    driver.close()
            driver.switch_to.window(allHandles[-1])

    def switch_Post_To_Entp(self,driver):
        allHandles = driver.window_handles
        for hd in allHandles:
            if hd != allHandles[0] and hd != allHandles[1]:
                driver.switch_to.window(hd)
                driver.close()
        driver.switch_to.window(allHandles[1])





