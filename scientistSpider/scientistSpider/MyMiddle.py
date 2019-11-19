# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         MyMiddle
# Description:  
# Author:       forwork
# Date:         2018/12/19
#-------------------------------------------------------------------------------
import random
# from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

ips = [
'HTTP://112.85.170.204:9999',
'HTTPS://122.193.245.47:9999',
'HTTP://171.80.2.45:9999',
'HTTP://121.233.251.50:9999',
'HTTPS://58.253.159.251:9999',
'HTTPS://117.85.82.158:53128',
'HTTPS://119.254.94.114:45691',
'HTTPS://171.80.115.234:9999',
'HTTPS://171.38.26.227:8123',
'HTTP://112.85.128.149:9999',
'HTTPS://223.241.79.127:8010',
'HTTP://118.190.95.43:9001',
'HTTP://140.143.58.5:8080',
'HTTP://112.85.129.25:9999',
'HTTP://111.26.9.26:80',
'HTTP://59.37.33.62:50686',
'HTTP://39.137.69.7:80',
'HTTP://112.85.168.127:9999',
'HTTP://119.36.161.174:80',
'HTTP://116.196.91.182:3128',
'HTTP://27.38.96.157:9797',
'HTTP://112.91.224.33:8000',
'HTTP://183.234.241.105:8118',
'HTTP://112.87.69.43:9999',
'HTTP://39.137.77.66:80',
'HTTP://221.218.102.146:41891',
'HTTP://221.6.32.214:41816',
'HTTP://59.49.72.137:80',
'HTTP://112.87.70.105:9999',
'HTTP://119.180.135.147:8060',
'HTTP://113.65.5.5:8118',
'HTTP://183.30.204.113:9999',
'HTTP://124.156.108.71:82',
'HTTP://119.36.161.174:80',
'HTTP://118.190.145.138:9001',
'HTTP://27.188.65.244:8060',
'HTTP://183.234.241.105:8118',
'HTTP://218.241.219.226:9999',
'HTTP://124.156.181.130:9999',
'HTTP://117.191.11.109:8080',
'HTTP://59.32.37.208:61234',
'HTTP://112.87.68.102:9999',
'HTTP://163.204.242.27:9999',
'HTTP://112.87.70.116:9999',
'HTTP://43.255.228.150:3128',
'HTTP://118.190.145.138:9001',
'HTTP://222.223.203.104:8060',
'HTTP://111.63.135.109:80',
'HTTP://39.137.69.9:80',
'HTTP://42.51.42.201:808',
'HTTP://113.247.252.114:9090',
'HTTP://60.212.195.113:8060',
'HTTP://183.233.90.6:8080',
'HTTP://27.40.145.171:9999',
'HTTP://112.85.130.39:9999',
'HTTP://111.11.100.13:8060',
'HTTP://119.176.96.134:9999',
'HTTP://112.87.70.134:9999',
'HTTP://117.191.11.74:8080',
'HTTP://36.99.16.241:82',
'HTTP://221.206.100.133:54781',
'HTTP://112.87.70.240:9999',
'HTTP://120.237.156.43:8088',
'HTTP://49.51.133.212:8081',
'HTTP://118.144.149.206:3128',
'HTTP://218.75.69.50:37339',
'HTTP://180.160.62.190:8118',
'HTTP://121.204.150.152:8118',
'HTTP://27.208.65.165:8060',
'HTTP://117.127.16.208:8080',
'HTTP://47.94.89.87:3128',
'HTTP://139.129.207.72:808',
'HTTP://112.85.168.125:9999',
'HTTP://58.217.94.5:8060',
'HTTP://122.226.135.89:808',
'HTTP://175.17.98.101:8080',
'HTTP://121.69.37.6:9797',
'HTTP://171.80.113.248:9999',
'HTTP://112.85.169.1:9999',
'HTTP://101.4.136.34:8080',
'HTTP://60.212.196.166:8060',
'HTTP://122.193.244.132:9999',
'HTTP://27.42.168.46:34426',
'HTTP://47.95.254.18:3128',
'HTTP://183.136.177.77:3128',
'HTTP://117.191.11.110:8080',
'HTTP://47.94.89.87:3128',
'HTTP://221.1.200.242:42135',
'HTTP://183.146.213.56:80',
'HTTP://112.84.178.21:8888',
'HTTP://182.92.105.136:3128',
'HTTP://119.41.236.180:8010',
'HTTP://111.202.37.195:43787',
'HTTP://116.196.81.58:3128',
'HTTP://120.194.18.90:81',
'HTTP://39.137.107.98:80',
'HTTP://183.161.29.127:8060',
'HTTP://118.24.246.249:80',
'HTTP://117.68.237.92:8118'
]

argents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
]

# 随机生成UserAgent
class UserAgentMiddlewares(UserAgentMiddleware):

    def process_request(self,request,spider):
        argent = random.choice(argents)
        if argent:
            print('User-Agent:',argent)
            request.headers.setdefault('User-Agent', argent)

#随机生成代理（逻辑：从代理池中 随机 获取使用次数较少的代理 返回）
# 目前没有使用，购买代理   使用代理商提供API获取
class ProxyMiddleware(object):

    def process_request(self,request,spider):
        proxy = random.choice(ips)
        proxy_host = proxy
        protocol = 'https' if 'HTTPS' in proxy_host else 'http'
        proxies = {protocol: proxy_host}
        response = requests.get('http://www.baidu.com', proxies=proxies, timeout=2)
        if response.status_code != 200:
            print("代理：：", proxy)
            request.meta['proxy'] = proxy
        else:
            self.process_request(request,spider)
