# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from VideoSpider.items import TvItem

class A163NewsSpider(scrapy.Spider):
    name = '163_news'
    allowed_domains = ['news.163.com']
    start_urls = ['http://news.163.com/']

    def parse(self, response):
        urls = response.css('a[href*="163."][href$="html"]::attr(href)').extract()
        for url in urls:
            # yield Request(url, callback=self.parse_title, dont_filter=True)
            pass
        catagory_urls = response.css('div.ns_area a::attr(href)').extract()
        catagory_urls.remove('http://news.163.com/special/wangsansanhome/')
        for url in catagory_urls:
            # yield Request(url, callback=self.parse_catagory, dont_filter=True)
            pass

    def parse_title(self, response):
        name = response.css('title::text').extract()
        if name:
            name = name[0]
            name = name[0: name.find('_')]
            id = response.url[response.url.rfind('/') + 1: response.url.rfind('.')]
            item = TvItem()
            item['id'] = id
            item['name'] = name
            item['isFeature'] = 1
            item['upTime'] = ''
            item['area'] = ''
            item['parts'] = 1
            item['updateTime'] = ''
            item['language'] = ''
            item['type_tag'] = ''
            item['playTimes'] = ''
            item['score'] = ''
            item['director'] = ''
            item['actor'] = ''
            item['describe'] = ''
            item['isVip'] = 0
            item['comment'] = 0
            item['recommend'] = ''
            item['platform'] = '163'
            item['classify'] = 0
            yield item


    def parse_catagory(self, response):
        urls = response.css('a[href*="163."][href$="html"]::attr(href)').extract()
        for url in urls:
            yield Request(url, callback=self.parse_title, dont_filter=True)

