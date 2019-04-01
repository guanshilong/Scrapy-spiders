# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy import Request
from scrapy_splash import SplashRequest
from VideoSpider.items import RentItem

class BjSpider(scrapy.Spider):
    name = 'bj'
    allowed_domains = ['bj.01fy.cn']
    start_urls = ['http://bj.01fy.cn/rent/list_2.html']

    custom_settings = {
        'DOWNLOAD_DELAY' : 5,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPLASH_URL': 'http://192.168.157.99:8050',
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage'
    }

    def start_requests(self):
        yield SplashRequest(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        urls = response.css('a[href^="house"]::attr(href)').extract()
        for url in set(urls):
            yield SplashRequest(url=parse.urljoin(self.start_urls[0], url), callback=self.parse_txt, dont_filter=True)
        next = response.css('.pager a')
        for i in next:
            if '下一页' in i.css('::text').extract():
                url = i.css('::attr(href)').extract()[0]
                yield SplashRequest(parse.urljoin(self.start_urls[0], url), callback=self.parse, dont_filter=True)

    def parse_txt(self, response):
        common = response.css('.cr_left dl')
        price = way = size = nei_name = address = decoration = direction = people = phone = ''
        for txt in common:
            name = txt.css('dt ::text').extract()[0]
            content = txt.css('dd ::text').extract()[0]
            if '价格' in name:
                price = content
            elif '方式' in name:
                way = content
            elif '面积' in name:
                size = content
            elif '名称' in name:
                nei_name = content
            elif '地址' in name:
                address = content
            elif '装修' in name:
                decoration = content
            elif '朝向' in name:
                direction = content
            elif '联' == name:
                if '个人' not in content:
                    return
                else:
                    people = content
            elif '电话' in name:
                phone = txt.css('dd span.redtelphone::text').extract()
                if phone:
                    phone = phone[0]
                    if '*' in phone:
                        return
                else:
                    return
        item = RentItem()
        item['url'] = response.url
        item['people'] = people
        item['phone'] = phone
        item['price'] = price
        item['size'] = size
        item['way'] = way
        item['nei_name'] = nei_name
        item['address'] = address
        item['decoration'] = decoration
        item['direction'] = direction
        item['area'] = 'bj'
        yield item
        print('------------------------------------------------')
        print(response.url)
        print(people)
        print(phone)
        print(price)
        print(size)
        print(way)
        print(nei_name)
        print(address)
        print(decoration)
        print(direction)




