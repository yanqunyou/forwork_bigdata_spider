# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

import requests
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.exceptions import CloseSpider


class ZhilianEntpSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.


    def process_spider_input(self, response, spider):
        if not 200 <= response.status <= 300:
            raise CloseSpider('爬虫异常,退出!  %s' % response.url)
        return None

    def process_spider_output(self, response, result, spider):
        for res in result:
            yield res

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ZhilianEntpSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

ips = [
'HTTP://117.191.11.73:80',
'HTTP://39.137.168.230:8080',
'HTTP://116.114.19.211:443',
'HTTP://122.13.248.215:8888',
'HTTP://125.67.25.83:37403',
'HTTP://202.112.51.51:8082',
'HTTP://118.190.19.118:808',
'HTTP://120.79.184.62:8080',
'HTTP://115.53.19.140:9999',
'HTTP://115.196.88.247:8118',
'HTTP://106.2.238.2:3128',
'HTTP://106.14.206.26:8118',
'HTTP://120.27.210.60:8080',
'HTTP://119.180.141.31:8060',
'HTTP://123.56.12.242:3128',
'HTTP://113.120.34.0:9999',
'HTTP://117.127.0.202:80',
'HTTP://117.68.190.32:8118',
'HTTP://113.121.20.138:9999',
'HTTP://183.146.213.56:80',
'HTTP://121.40.90.189:8001',
'HTTP://47.98.237.129:80',
'HTTP://113.121.22.222:61234',
'HTTP://117.191.11.107:80',
'HTTP://47.98.237.129:80',
'HTTP://122.4.28.134:9999',
'HTTP://60.9.1.250:80',
'HTTP://118.31.67.240:3128',
'HTTP://27.42.168.46:42057',
'HTTP://123.207.217.104:1080',
'HTTP://115.213.63.104:53281',
'HTTP://117.186.214.74:9999',
'HTTP://119.41.236.180:8010',
'HTTP://220.180.156.53:8060',
'HTTP://120.27.210.60:8080',
'HTTP://222.175.171.6:8080',
'HTTP://113.120.33.116:9999',
'HTTP://118.180.166.195:8060',
'HTTP://118.181.226.216:58654',
'HTTP://113.128.11.136:9999',
'HTTP://175.17.2.123:8080',
'HTTP://47.96.135.84:80',
'HTTP://112.84.178.21:8888',
'HTTP://218.60.8.99:3129',
'HTTP://106.75.211.89:8080',
'HTTP://117.62.93.54:8118',
'HTTP://203.130.46.108:9090',
'HTTP://119.51.168.129:8080',
'HTTP://59.127.168.43:3128',
'HTTP://60.191.134.164:9999',
'HTTP://27.188.65.244:8060',
'HTTP://183.146.213.157:80',
'HTTP://119.179.151.250:8060',
'HTTP://118.190.145.138:9001',
'HTTP://210.26.49.88:3128',
'HTTP://222.223.182.66:8000',
'HTTP://113.65.33.24:3128',
'HTTP://118.190.19.118:808',
'HTTP://117.127.16.207:80',
'HTTP://117.127.16.207:80',
'HTTP://118.24.246.249:80',
'HTTP://60.2.44.182:52143',
'HTTP://47.107.233.107:80',
'HTTP://222.89.32.178:9999',
'HTTP://122.4.40.247:9999',
'HTTP://183.57.36.87:8888',
'HTTP://117.191.11.75:80',
'HTTP://182.150.35.76:80',
'HTTP://27.191.234.69:9999',
'HTTP://36.25.243.50:80',
'HTTP://122.4.40.247:9999',
'HTTP://39.137.69.6:80',
'HTTP://36.7.89.233:8060',
'HTTP://61.128.208.94:3128',
'HTTP://123.207.178.146:9999',
'HTTP://115.159.31.195:8080'
]


argents = [
"HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1"
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
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
class ProxyMiddleware(HttpProxyMiddleware):

    def process_request(self,request,spider):
        proxy = random.choice(ips)
        proxy_host = proxy
        protocol = 'https' if 'HTTPS' in proxy_host else 'http'
        proxies = {protocol: proxy_host}
        try:
            response = requests.get('https://www.baidu.com', proxies=proxies, timeout=2)
            if response.status_code == 200:
                print("代理：：", proxy)
                request.meta['proxy'] = proxy
            else:
                print("请求失败：：")
                print(response.content)
                self.process_request(request,spider)
        except Exception as e:
            print(e)
            self.process_request(request,spider)
