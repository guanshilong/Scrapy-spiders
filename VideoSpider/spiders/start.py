# -*- coding: utf-8 -*-
import scrapy
from scrapy.cmdline import execute
from scrapy_splash import SplashRequest
from scrapy import Request


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['detail.tmall.com']
    start_urls = ['https://www.baidu.com']
    # 测试scrapy-splash
    # custom_settings = {
    #     'DOWNLOADER_MIDDLEWARES': {
    #         'scrapy_splash.SplashCookiesMiddleware': 723,
    #         'scrapy_splash.SplashMiddleware': 725,
    #         'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    #     },
    #     'SPLASH_URL': 'http://192.168.157.99:8050',
    #     'SPIDER_MIDDLEWARES': {
    #         'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    #     },
    #     'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    #     'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage'
    # }

    # 测试scrapy-proxies
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
           'scrapy_proxies.RandomProxy': 100,
        },
        'PROXY_LIST': '../utils/list.txt',
        'PROXY_MODE': 0,
        'RETRY_TIMES': 10
    }

    def start_requests(self):
        # yield SplashRequest(self.start_urls[0], callback=self.parse)
        yield Request(self.start_urls[0], callback=self.parse, dont_filter=True)

    def parse(self, response):
        title = response.css('title::text').extract()
        print(title)

#   def parse(self, response):
#        yield scrapy.FormRequest.from_response(
#             response,
#             formid='fm1',
#             formdata={'username': '15662730751', 'password': '20110109'},
#             clickdata={'nr': 9},
#             callback=self.after_login
#         )
#
#     def after_login(self, response):
#         print(response.text)

    if __name__ == "__main__":
        execute("scrapy crawl Tianyancha".split(" "))
        pass