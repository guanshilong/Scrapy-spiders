# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import random
import time
from VideoSpider.items import TvItem

class SinaspiderSpider(scrapy.Spider):
    name = 'SinaSpider'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['https://news.sina.com.cn/']

    def parse(self, response):
        news_urls = response.css('a[href*="doc-"]::attr(href)').extract()
        # news_urls = ['https://news.sina.com.cn/w/2018-12-06/doc-ihmutuec6615582.shtml']
        for url in news_urls:
            yield Request(url, callback=self.parse_title, dont_filter=True)
            pass

        cat0 = [
                'https://news.sina.com.cn/china/',
                'https://sports.sina.com.cn',
                'https://finance.sina.com.cn',
                'https://tech.sina.com.cn',
                'https://mil.news.sina.com.cn'
                ]
        for url in cat0:
            yield Request(url, callback=self.parse_catagory, meta={'flag': 0}, dont_filter=True)
            pass
        cat1 = ['https://news.sina.com.cn/hotnews']
        for url in cat1:
            yield Request(url, callback=self.parse_catagory, meta={'flag': 1}, dont_filter=True)
            pass
        cat2 = ['https://cul.news.sina.com.cn']
        for url in cat2:
            yield Request(url, callback=self.parse_catagory, meta={'flag': 2}, dont_filter=True)
            pass
        cat3 = ['https://gov.sina.com.cn']
        for url in cat3:
            yield Request(url, callback=self.parse_catagory, meta={'flag': 3}, dont_filter=True)
            pass
        cat4 = ['https://ent.sina.com.cn']
        for url in cat4:
            yield Request(url, callback=self.parse_catagory, meta={'flag': 4}, dont_filter=True)
            pass
        cat5 = ['https://news.sina.com.cn/world/']
        for url in cat5:
            yield Request(url, callback=self.parse_cat5, meta={'flag': 6}, dont_filter=True)
            pass

        roll_urls = ['https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=1&r={0}&callback=jQuery31109829100847697814_{1}&_={1}'.format(random.random(),int(float(time.time())*1000))]
        print(roll_urls[0])
        for url in roll_urls:
            yield Request(url, callback=self.parse_cat5, meta={'flag': 5}, dont_filter=True)
            pass

    def parse_title(self, response):
        name = response.css('title::text').extract()[0].split('|')[0]
        id = response.url[response.url.rfind('/')+1: response.url.rfind('.')].replace('doc-i', '')
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
        item['platform'] = 'sina'
        item['classify'] = 0
        yield item
        print(name, id)

    def parse_catagory(self, response):
        flag = response.meta['flag']

        if flag == 0:
            common = response.css('li a[href*="doc-"]')
        elif flag == 1:
            common = response.css('td.ConsTi a[href*="doc-"]')
        elif flag == 2:
            common = response.css('.blk12 a[href*="doc-"]')
        elif flag == 3:
            common = response.css('dt a[href*="doc-"]')
        elif flag == 4:
            common = response.css('.seo_data_list li a[href*="doc-"]')
        urls = common.css('::attr(href)').extract()
        names = common.css('::text').extract()
        for (url, name) in zip(urls, names):
            id = url[url.rfind('/')+1: url.rfind('.')].replace('doc-i', '')
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
            item['platform'] = 'sina'
            item['classify'] = 0
            yield item

    def parse_cat5(self, response):
        flag = response.meta['flag']
        if flag == 5:
            for txt in response.text.split(','):
                if 'doc-' in txt:
                    url = txt.partition(':')[2].replace('"', '').replace('[', '').replace(']', '').replace('\\', '')
                    yield Request(url, callback=self.parse_title, dont_filter=True)
            pass
        else:
            news_urls = response.css('a[href*="doc-"]::attr(href)').extract()
            for url in news_urls:
                yield Request(url, callback=self.parse_title, dont_filter=True)
            pass