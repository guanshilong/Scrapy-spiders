# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent
import pymysql
import requests


class VideospiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

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


class VideospiderDownloaderMiddleware(object):
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


# class MyUserAgentMiddleware(UserAgentMiddleware):
#     '''
#     设置User-Agent
#     '''
#
#     def __init__(self, ua):
#         ua.update()
#         self.ua = ua
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(ua=UserAgent())
#
#     def process_request(self, request, spider):
#         request.headers['User-Agent'] = self.ua.random
#         pass


class MyProxyMiddleware(object):
    # def __init__(self, host, db, user, password, port):
    #     self.conn = pymysql.connect(host=host,
    #                                 database=db,
    #                                 user=user,
    #                                 password=password,
    #                                 port=port,
    #                                 charset='utf8')
    #     self.ip = self.get_ip()
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     host = crawler.settings.get('MYSQL_HOST')
    #     db = crawler.settings.get('MYSQL_DBNAME')
    #     user = crawler.settings.get('MYSQL_USER')
    #     password = crawler.settings.get('MYSQL_PASSWD')
    #     port = crawler.settings.get('MYSQL_PORT')
    #     return cls(host, db, user, password, port)
    #
    # def get_ip(self):
    #     cursor = self.conn.cursor()
    #     cursor.execute('select ip from proxy order by rand() limit 1')
    #     ip = cursor.fetchone()
    #     if ip:
    #         judge = self.judge_ip(ip[0])
    #         print(ip[0])
    #         if judge:
    #             return ip[0]
    #         else:
    #             self.get_ip()
    #     else:
    #         return ''
    #
    # def judge_ip(self, ip):
    #     # 判断ip是否可用
    #     http_url = 'http://www.baidu.com'
    #     try:
    #         proxy_dict = {
    #             "http": ip,
    #         }
    #         response = requests.get(http_url, proxies=proxy_dict)
    #         print(response.status_code)
    #     except Exception as e:
    #         print("invalid ip and port")
    #         self.delete_ip(ip)
    #         return False
    #     else:
    #         code = response.status_code
    #         if code in (200, 299):
    #             print(f"effective ip,code is {code}")
    #             return True
    #         else:
    #             print("invalid ip and port")
    #             self.delete_ip(ip)
    #             return False
    #
    # def delete_ip(self, ip):
    #     # 从数据库中删除无效的ip
    #     delete_sql = f"delete from proxy where ip='{ip}'"
    #     cursor = self.conn.cursor()
    #     cursor.execute(delete_sql)
    #     self.conn.commit()
    #     return True

    def process_request(self, request, spider):
        # get_ip = GetIp()
        # request.meta['proxy'] = get_ip.get_random_ip()
        # request.meta['proxy'] = self.ip
        # print(get_ip.get_random_ip())
        request.meta["proxy"] = 'http://221.5.80.66:3128'
        # request.meta["proxy"] = 'http://113.200.56.13:8010'
        # request.meta["proxy"] = 'http://45.115.171.30:47949'
        # request.meta['proxy'] = 'http://101.37.79.125:3128'
        # 在MySQL统一管理代理IP
        # if self.ip:
            # request.meta['proxy'] = self.ip
        # request.meta['splash']['args']['proxy'] = 'http://114.116.10.21:3128'
        pass