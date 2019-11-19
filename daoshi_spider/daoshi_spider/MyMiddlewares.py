# _*_ coding=utf-8 _*_
import random
import time

from conda.gateways import logging
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware


#该文件主要用来随机选择UserAgent与代理（后期需要）
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

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

ips = ['HTTPS://119.101.113.123:9999',
'HTTP://119.101.118.87:9999',
'HTTPS://119.101.112.49:9999',
'HTTP://119.101.112.174:9999',
'HTTP://121.232.194.162:9999',
'HTTP://58.55.226.233:9999',
'HTTPS://111.181.116.158:9999',
'HTTPS://119.101.115.61:9999',
'HTTPS://119.101.116.158:9999',
'HTTPS://119.101.119.14:9999',
'HTTP://119.101.113.180:9999',
'HTTPS://222.189.190.110:9999',
'HTTP://121.61.0.162:9999',
'HTTP://119.101.118.3:9999',
'HTTPS://119.101.119.11:9999',
'HTTPS://113.122.171.161:9999',
'HTTPS://182.18.13.149:53281',
'HTTPS://58.17.125.215:53281',
'HTTP://124.207.82.166:8008',
'HTTPS://203.86.26.9:3128',
'HTTP://180.168.198.141:18118',
'HTTPS://163.125.18.182:8888',
'HTTP://119.145.2.99:44129',
'HTTP://123.161.19.38:9797',
'HTTPS://180.169.186.155:1080',
'HTTP://121.227.66.187:3128',
'HTTP://222.221.11.119:3128',
'HTTPS://218.22.7.62:53281',
'HTTPS://60.5.254.169:8081',
'HTTP://218.75.70.3:8118',
'HTTP://182.88.13.172:9797',
'HTTPS://113.116.147.68:9000',
'HTTPS://112.67.164.34:9797',
'HTTPS://119.101.112.49:9999',
'HTTPS://111.181.116.158:9999',
'HTTPS://119.101.116.158:9999',
'HTTPS://119.101.119.14:9999',
'HTTPS://222.189.190.110:9999',
'HTTPS://58.55.227.37:9999',
'HTTPS://119.101.119.11:9999',
'HTTPS://113.122.171.161:9999',
'HTTPS://221.233.45.3:9999',
'HTTPS://119.101.118.89:9999',
'HTTPS://119.101.116.33:9999',
'HTTPS://112.85.129.37:9999',
'HTTPS://119.101.113.176:9999',
'HTTPS://1.192.240.235:9999',
'HTTPS://119.102.133.233:9999',
'HTTPS://119.101.116.47:9999',
'HTTPS://119.101.117.135:9999',
'HTTPS://183.148.155.19:9999',
'HTTP://119.101.112.63:9999',
'HTTP://119.101.118.87:9999',
'HTTP://119.101.112.174:9999',
'HTTP://121.232.194.162:9999',
'HTTP://58.55.226.233:9999',
'HTTP://119.101.113.180:9999',
'HTTP://222.217.30.55:9999',
'HTTP://219.159.38.204:56210',
'HTTP://121.61.0.162:9999',
'HTTP://119.101.118.3:9999',
'HTTP://110.52.235.73:9999',
'HTTP://119.101.117.194:9999',
'HTTP://125.123.141.210:9999',
'HTTP://119.101.116.105:9999',
'HTTP://119.101.116.65:9999',
'HTTP://58.55.225.56:9999',
'HTTP://119.101.112.23:9999',
'HTTP://121.61.1.33:9999',
'HTTP://121.61.2.195:9999',
'HTTP://212.83.164.85:80',
'HTTPS://103.199.12.12:8080',
'HTTP://190.242.119.194:8085',
'HTTP://47.104.166.2:8080',
'HTTP://47.104.213.220:8080',
'HTTP://41.222.226.45:80',
'HTTP://196.13.208.23:8080',
'HTTP://41.222.226.47:80',
'HTTP://195.154.207.153:80',
'HTTP://167.114.250.199:9999',
'HTTP://39.108.136.37:80',
'HTTPS://27.54.248.42:8000',
'HTTP://115.159.31.195:8080',
'HTTP://39.137.46.72:8080',
'HTTP://39.137.69.10:8080',
'HTTP://39.137.69.7:8080',
'HTTP://39.137.69.9:8080',
'HTTP://120.76.77.152:9999',
'HTTPS://117.139.126.236:53281',
'HTTP://183.237.206.92:53281',
'HTTP://60.255.186.169:8888',
'HTTPS://61.178.238.122:63000',
'HTTP://153.35.185.71:80',
'HTTPS://183.236.238.6:54152',
'HTTP://36.110.234.244:80',
'HTTP://222.173.90.162:8060',
'HTTP://183.230.177.140:8060',
'HTTP://61.150.113.27:8908',
'HTTP://60.30.19.131:10010',
'HTTP://60.208.44.228:80',
'HTTPS://66.103.174.65:60971',
'HTTP://125.209.116.182:31653',
'HTTP://222.135.78.190:8060',
'HTTPS://217.107.197.39:33628',
'HTTPS://89.109.12.82:47972',
'HTTPS://1.10.188.95:30593',
'HTTP://79.175.57.77:55477',
'HTTPS://187.1.43.246:53396',
'HTTP://43.231.215.247:35798',
'HTTPS://95.189.112.214:35508',
'HTTPS://122.49.115.2:34982',
'HTTPS://115.124.75.77:52928',
'HTTPS://1.179.203.89:30229',
'HTTPS://182.52.229.166:56480',
'HTTP://78.36.202.254:32337',
'HTTPS://118.174.232.187:40721',
'HTTP://195.205.201.118:61142',
'HTTPS://101.98.247.14:38203',
'HTTP://186.159.1.25:45334',
'HTTPS://128.75.239.122:4550',
'HTTPS://177.73.248.6:54381',
'HTTPS://213.109.15.231:53871',
'HTTPS://82.144.81.64:39632',
'HTTP://27.147.146.78:52220',
'HTTPS://182.52.51.36:52165',
'HTTPS://104.248.98.1:3128',
'HTTP://202.79.53.190:46734',
'HTTPS://125.40.238.181:56738',
'HTTPS://222.124.173.147:53281',
'HTTP://118.174.233.53:38697']

# 随机生成UserAgent
class UserAgentMiddlewares(object):

    def process_request(self,request,spider):
        argent = random.choice(argents)
        if argent:
            print('User-Agent:',argent)
            request.headers.setdefault('User-Agent', argent)


class ProxyMiddleware(object):

    def process_request(self,request,spider):
        proxy = random.choice(ips)
        if proxy:
            print("Proxy::",proxy)
            request.meta['proxy'] = proxy


class Process_Proxies(RetryMiddleware):
    logger = logging.getLogger(__name__)

    def dele_proxy(self, proxy, res=None):
        print('删除代理')
        if proxy:
            argents.remove(proxy)

    def process_response(self, request, response, spider):
        # if request.meta.get('dont_retry',False):
        #     return response
        # if response.status in self.retry_http_codes:
        if response.status != 200:
            print('状态码异常')
            reason = response_status_message(response.status)
            print("将要删除代理：：",request.meta['proxy'])
            self.dele_proxy(request.meta['proxy'], False)
            time.sleep(random.randint(3, 5))
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get('dont_retry', False):
            print("将要删除代理：：", request.meta['proxy'])
            self.dele_proxy(request.meta.get('proxy', False))
            time.sleep(random.randint(3, 5))
            self.logger.warning('连接异常,进行重试......')

            return self._retry(request, exception, spider)


