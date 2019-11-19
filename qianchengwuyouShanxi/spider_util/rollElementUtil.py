# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         rollElementUtil.py
# Description:  
# Author:       forwork
# Date:         2019/7/23
#-------------------------------------------------------------------------------

class RollElementUtil(object):

    # 1.如果为true，元素的顶端将和其所在滚动区的可视区域的顶端对齐。
    def rollToView_top( self,driver,target):
        print("滑动到窗口顶部")
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", target)
        except Exception as e:
            print(e)

    # 2.如果为false，元素的底端将和其所在滚动区的可视区域的底端对齐。
    def rollToView_bottom(self,driver, target):
        print("滑动到窗口底部")
        try:
            driver.execute_script("arguments[0].scrollIntoView(false);", target)
        except Exception as e:
            print(e)

    # 3.滑动到页面顶部
    def rollToPage_head(self,driver, target):
        try:
            driver.execute_script("arguments[0].scrollTo(0,1);", target)
        except Exception as e:
            print(e)

    # 4.滑动到页面底部
    def rollToPage_deep(self, driver,target):
        try:
            driver.execute_script("arguments[0].scrollTo(0,10000);", target)
        except Exception as e:
            print(e)
