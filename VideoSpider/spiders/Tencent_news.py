# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class TencentNewsSpider(scrapy.Spider):
    name = 'Tencent_news'
    allowed_domains = ['news.qq.com']
    start_urls = ['https://news.qq.com/']

    def parse(self, response):
        urls = set(response.css('a[href*="qq."][href*="htm"][href*="http"]::attr(href)').extract())
        for url in urls:
            yield Request(url, callback=self.parse_title, dont_filter=True)

    def parse_title(self, response):
        name = response.css('title::text').extract()[0]
        name = name[0: name.find('_')].replace(' ', '')
        id = response.url[response.url.rfind('/')+1: response.url.rfind('.')]
        print((name, response.url))

