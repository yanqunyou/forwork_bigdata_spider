# _*_ coding=utf-8 _*_
import random

#该文件主要用来随机选择UserAgent与代理（后期需要）

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

ips = [
'HTTPS://183.148.153.200:9999',
'HTTPS://115.239.25.250:9999',
'HTTPS://116.209.55.238:9999',
'HTTPS://1.192.242.175:9999',
'HTTPS://121.63.199.122:9999',
'HTTPS://59.62.165.246:808',
'HTTP://110.52.235.203:9999',
'HTTP://125.123.137.255:9999',
'HTTP://112.85.169.16:9999',
'HTTP://116.209.57.100:9999',
'HTTPS://59.62.166.243:9999',
'HTTPS://121.61.3.61:9999',
'HTTPS://116.209.56.133:9999',
'HTTPS://1.192.241.26:9999',
'HTTPS://121.61.1.209:9999',
'HTTP://221.235.236.68:9999',
'HTTP://125.123.140.239:9999',
'HTTP://111.77.197.6:9999',
'HTTP://113.121.144.180:9999',
'HTTPS://125.123.143.35:9000',
'HTTP://115.171.203.201:9000',
'HTTP://219.159.38.201:56210',
'HTTPS://59.62.167.152:53281',
'HTTPS://118.81.45.146:9797',
'HTTPS://1.192.242.217:9999',
'HTTPS://125.123.143.251:9000',
'HTTPS://58.56.108.237:58690',
'HTTP://182.88.247.177:9797',
'HTTP://117.62.61.180:8118',
'HTTPS://1.48.150.26:8118',
'HTTP://112.95.22.127:8888',
'HTTP://14.118.130.214:8081',
'HTTP://180.140.191.233:36820',
'HTTPS://183.172.41.93:8118',
'HTTP://125.123.143.15:9000',
'HTTPS://125.123.142.108:9000',
'HTTP://118.24.127.171:8118',
'HTTPS://58.247.127.145:53281',
'HTTPS://115.239.25.250:9999',
'HTTPS://182.88.148.148:9797',
'HTTPS://116.209.55.238:9999',
'HTTPS://1.192.242.175:9999',
'HTTPS://121.63.199.122:9999',
'HTTPS://59.62.165.246:808',
'HTTPS://59.62.166.243:9999',
'HTTPS://121.61.3.61:9999',
'HTTPS://116.209.56.133:9999',
'HTTPS://1.192.241.26:9999',
'HTTPS://121.61.1.209:9999',
'HTTPS://115.151.3.167:9999',
'HTTPS://115.151.1.172:9999',
'HTTPS://117.91.232.234:9999',
'HTTPS://121.61.1.4:9999',
'HTTPS://116.209.57.26:9999',
'HTTPS://183.148.130.47:9999',
'HTTPS://115.151.7.118:53128',
'HTTPS://110.52.235.149:9999',
'HTTP://110.52.235.203:9999',
'HTTP://125.123.137.255:9999',
'HTTP://112.85.169.16:9999',
'HTTP://116.209.57.100:9999',
'HTTP://221.235.236.68:9999',
'HTTP://125.123.140.239:9999',
'HTTP://111.77.197.6:9999',
'HTTP://113.121.144.180:9999',
'HTTP://221.235.239.111:9999',
'HTTP://59.62.164.17:9999',
'HTTP://110.52.235.138:9999',
'HTTP://125.126.205.168:9999',
'HTTP://121.61.0.95:9999',
'HTTP://125.123.143.207:9999',
'HTTP://121.61.3.192:9999',
'HTTP://111.181.50.0:9999',
'HTTP://125.126.222.165:9999',
'HTTP://125.123.137.91:9999',
'HTTP://125.126.195.243:9999',
'HTTP://37.200.224.179:8080',
'HTTP://31.11.177.235:80',
'HTTP://195.154.207.153:80',
'HTTP://177.54.142.222:8080',
'HTTP://211.79.61.8:3128',
'HTTP://167.114.250.199:9999',
'HTTP://212.83.164.85:80',
'HTTP://182.73.25.217:80',
'HTTP://182.73.25.220:80',
'HTTP://190.242.119.194:8085',
'HTTP://196.13.208.23:8080',
'HTTP://120.76.77.152:9999',
'HTTP://47.94.230.42:9999',
'HTTPS://223.99.214.21:53281',
'HTTP://60.255.186.169:8888',
'HTTP://61.178.238.122:63000',
'HTTPS://223.223.187.195:80',
'HTTP://124.42.7.103:80',
'HTTP://153.35.185.71:80',
'HTTP://118.178.227.171:80',
'HTTPS://221.10.159.234:1337',
'HTTP://36.110.234.244:80',
'HTTPS://112.230.197.236:63000',
'HTTP://183.230.177.140:8060',
'HTTP://39.108.136.37:80',
'HTTP://115.159.31.195:8080',
'HTTPS://223.68.190.130:8181',
'HTTP://39.137.46.72:8080',
'HTTP://39.137.69.10:8080',
'HTTP://39.137.69.7:8080',
'HTTP://39.137.69.9:8080',
'HTTP://120.92.174.37:1080',
'HTTP://152.92.200.74:80',
'HTTPS://202.93.128.98:3128',
'HTTP://188.166.223.181:80',
'HTTPS://212.200.27.134:8080',
'HTTP://88.147.142.25:8080',
'HTTP://39.137.77.68:80',
'HTTP://39.137.77.68:8080',
'HTTP://39.137.77.67:8080',
'HTTP://39.137.77.66:8080',
'HTTPS://89.22.175.42:8080',
'HTTP://39.137.69.6:8080',
'HTTP://39.137.69.8:8080',
'HTTP://217.150.77.31:53281',
'HTTP://62.213.87.172:8080',
'HTTP://190.60.103.178:8080',
'HTTP://78.136.243.133:3128',
'HTTP://213.58.202.70:54214',
'HTTP://80.237.54.158:8080',
'HTTP://185.190.40.75:8080',
'HTTP://88.147.244.124:8080',
'HTTPS://96.80.89.69:8080',
'HTTP://139.162.3.174:8118',
'HTTP://139.59.153.59:80',
'HTTPS://88.147.159.167:53281',
'HTTP://43.250.81.138:8080',
'HTTPS://203.128.68.242:53281',
'HTTPS://87.228.103.111:8080',
'HTTP://47.52.231.140:8080',
'HTTPS://67.205.178.183:55555',
'HTTP://121.61.1.38:9999',
'HTTP://110.52.235.58:9999',
'HTTP://180.118.77.9:9999',
'HTTP://111.177.191.140:9999',
'HTTP://116.209.55.234:9999',
'HTTP://163.204.246.28:9999',
'HTTP://115.239.24.18:9999',
'HTTPS://36.7.128.146:52222',
'HTTPS://121.61.1.139:9999',
'HTTP://121.61.3.67:9999',
'HTTPS://115.46.68.40:8123',
'HTTP://124.205.155.154:9090',
'HTTP://116.209.59.69:9999',
'HTTP://47.110.235.39:3128',
'HTTP://111.177.186.175:9999',
'HTTP://60.173.244.133:35634',
'HTTP://180.118.77.10:9999',
'HTTP://221.2.174.3:8060',
'HTTP://220.180.50.14:53281',
'HTTP://125.123.142.23:9999',
'HTTP://58.54.137.79:9999',
'HTTP://122.116.67.146:39275',
'HTTP://183.172.168.156:8118',
'HTTP://116.209.54.167:9999',
'HTTP://43.248.124.224:3128',
'HTTP://111.177.174.119:9999',
'HTTP://116.209.52.229:9999',
'HTTP://116.209.53.206:9999',
'HTTP://47.99.247.192:8118',
'HTTP://116.209.56.44:9999',
'HTTP://117.191.11.108:80',
'HTTP://117.68.195.114:808',
'HTTP://221.2.174.6:8060',
'HTTP://124.128.76.142:8060',
'HTTP://119.28.203.242:8000',
'HTTP://116.209.56.40:9999',
'HTTP://114.219.27.57:8118',
'HTTP://101.132.139.130:808',
'HTTP://116.209.55.98:9999',
'HTTP://111.177.166.24:9999',
'HTTP://183.230.179.157:8060',
'HTTP://121.204.163.119:3128',
'HTTP://140.207.25.114:56954',
'HTTP://222.135.77.105:8060',
'HTTP://116.209.52.133:9999',
'HTTP://119.29.90.18:9999',
'HTTP://117.191.11.108:80',
'HTTP://116.209.54.225:9999',
'HTTP://59.37.33.62:50686',
'HTTP://111.177.160.103:9999',
'HTTP://183.230.175.93:8060',
'HTTP://111.177.174.103:9999',
'HTTP://117.191.11.104:8080',
'HTTP://121.61.0.84:9999',
'HTTP://116.209.57.239:9999',
'HTTP://121.61.2.131:9999',
'HTTP://121.61.0.83:9999',
'HTTP://117.191.11.71:80',
'HTTP://117.191.11.103:8080',
'HTTP://116.209.55.15:9999',
'HTTP://116.209.52.136:9999',
'HTTP://114.55.236.62:3128',
'HTTP://111.177.179.251:9999',
'HTTP://117.191.11.71:8080',
'HTTP://116.209.57.240:9999',
'HTTP://112.12.37.196:53281',
'HTTP://49.51.193.134:1080',
'HTTP://121.233.251.42:9999',
'HTTP://111.177.162.187:9999',
'HTTP://116.209.58.122:9999',
'HTTP://111.177.166.63:9999',
'HTTP://116.209.55.117:9999',
'HTTP://111.177.183.174:9999',
'HTTP://47.96.121.23:8123',
'HTTP://111.177.184.80:9999',
'HTTP://124.207.82.166:8008',
'HTTP://116.209.54.83:9999',
'HTTP://113.128.10.43:9999',
'HTTP://61.184.40.71:9999',
'HTTP://117.191.11.75:8080',
'HTTP://110.52.235.15:9999',
'HTTP://125.123.141.209:9999',
'HTTP://125.126.215.23:9999',
'HTTP://125.123.143.112:9999',
'HTTP://110.52.235.216:9999',
'HTTP://116.209.56.112:9999',
'HTTP://111.177.190.164:9999',
'HTTP://121.61.0.241:9999',
'HTTP://116.209.53.70:9999',
'HTTP://59.127.38.117:8080',
'HTTP://180.118.77.28:9999',
'HTTP://111.177.172.239:9999',
'HTTP://218.75.69.50:45918',
'HTTP://111.177.49.156:9999',
'HTTP://116.209.56.124:9999',
'HTTP://116.209.54.80:9999',
'HTTP://110.52.235.156:9999',
'HTTP://218.28.96.196:8060',
'HTTP://183.148.135.46:9999',
'HTTP://121.61.2.206:9999',
'HTTP://121.61.2.21:9999',
'HTTP://112.85.166.72:9999',
'HTTP://111.177.190.78:9999',
'HTTP://111.177.191.254:9999',
'HTTP://111.177.184.111:9999',
'HTTP://113.121.145.131:9999',
'HTTP://116.209.54.137:9999',
'HTTP://121.61.0.197:9999',
'HTTP://120.194.42.157:38185',
'HTTP://121.61.1.41:9999',
'HTTP://112.87.66.111:9999',
'HTTP://121.61.1.175:9999',
'HTTP://116.209.54.126:9999',
'HTTP://119.180.134.192:8060',
'HTTP://111.177.190.174:9999'
]

# 随机生成UserAgent
class UserAgentMiddlewares(object):

    def process_request(self,request,spider):
        argent = random.choice(argents)
        request.headers['User-Agent']=argent



class ProxyMiddleware(object):

    def process_request(self,request,spider):
        proxy = random.choice(ips)
        request.meta['proxy'] = proxy