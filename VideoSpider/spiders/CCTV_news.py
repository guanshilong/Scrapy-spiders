# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from VideoSpider.items import TvItem

class CctvNewsSpider(scrapy.Spider):
    name = 'CCTV_news'
    allowed_domains = ['news.cctv.com']
    start_urls = ['http://news.cctv.com/']

    def parse(self, response):
        common = response.css('div.top_nav a')
        urls = common.css('::attr(href)').extract()
        urls[0] = 'http://news.cctv.com/'
        del urls[3]
        catalogys = common.css('::text').extract()
        del catalogys[3]
        for (url, cat) in zip(urls, catalogys):
            yield Request(url=url, callback=self.parse_info, meta={'cat': cat}, dont_filter=True)

    def parse_info(self, response):
        urls = response.css('a[href*="news.cctv.com"]::attr(href)').extract()
        if 'jiankang' in response.url:
            urls = response.css('a[href*="jiankang.cctv.com"]::attr(href)').extract()
        if 'sannong' in response.url:
            urls = response.css('a[href*="sannong.cctv.com"]::attr(href)').extract()
        if 'jingji' in response.url:
            urls = response.css('a[href*="jingji.cctv.com"]::attr(href)').extract()
        if 'sports' in response.url:
            urls = response.css('a[href*="sports.cctv.com"]::attr(href)').extract()
            urls.extend(response.css('a[href*="tv.cctv.com"]::attr(href)').extract())
        urls = set(urls)
        urls = [url for url in urls if 'index' not in url and not url.endswith('/') and url.endswith('html')]
        for url in urls:
            yield Request(url=url, callback=self.parse_title, meta={'cat': response.meta['cat']}, dont_filter=True)
        pass

    def parse_title(self, response):
        name = response.css('title::text').extract()[0].partition('_')[0]
        id = response.url[response.url.rfind('/') + 1: response.url.rfind('.')]
        print((name, id))
        item = TvItem()
        item['id'] = id
        item['name'] = name
        item['isFeature'] = 1
        item['upTime'] = ''
        item['area'] = ''
        item['parts'] = 1
        item['updateTime'] = ''
        item['language'] = ''
        item['type_tag'] = response.meta['cat']
        item['playTimes'] = 0
        item['score'] = ''
        item['director'] = ''
        item['actor'] = ''
        item['describe'] = ''
        item['isVip'] = 1
        item['comment'] = 0
        item['recommend'] = ''
        item['platform'] = 'cctv'
        item['sca_app_id'] = 5018
        item['cat1'] = '新闻'
        item['cat2'] = '新闻'
        # yield item