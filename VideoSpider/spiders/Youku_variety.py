# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from VideoSpider.items import TvItem


class YoukuVarietySpider(scrapy.Spider):
    name = 'Youku_variety'
    allowed_domains = ['list.youku.com']
    start_urls = ['https://list.youku.com/category/show/c_85.html']

    def parse(self, response):
        area_page = response.css('a[href^="//list.youku.com/category/show/c_85_s_6_d_1_a_"]')
        area_urls = area_page.css('::attr(href)').extract()
        areas = area_page.css('::text').extract()
        for area_url, area in zip(area_urls, areas):
            yield Request(url='https:' + area_url, callback=self.parse_page_detail_url, meta={'area': area}, dont_filter=True)

    def parse_page_detail_url(self, response):
        area = response.meta['area']
        urls = response.css('a[href*="//v.youku.com/v_show/id_"]::attr(href)').extract()
        if not urls:
            urls = response.css('a[href^="//v.youku.com/show/id_"]::attr(href)').extract()
        urls = set(urls)
        for url in urls:
            if 'http' in url:
                yield Request(url=url.replace('http:', 'https:'), callback=self.parse_detail_info, meta={'area': area}, dont_filter=True)
            else:
                yield Request(url='https:' + url, callback=self.parse_detail_info, meta={'area': area}, dont_filter=True)
        next_page = response.css('li.next a::attr(href)').extract()
        if next_page:
            yield Request(url='https:' + next_page[0], callback=self.parse_page_detail_url, meta={'area': area},  dont_filter=True)

    def parse_detail_info(self, response):
        area = response.meta['area']
        tags = response.css('span[ data-sn="tags"] a::text').extract()
        if tags:
            tags = '/'.join(tags)
        else:
            tags = ''
        play_list = response.css('div[id^="listitem_page"] .item::attr(item-id)').extract()
        name = response.css('.title-wrap h1 span a::text').extract()
        if name:
            name = name[0]
        else:
            name = response.css('meta[name="irAlbumName"]::attr(content)').extract()[0]
        print('----------------------------------')
        print(name)
        print(area)
        print(tags)
        # for id in set(play_list):
        #     item = TvItem()
        #     item['id'] = id.replace('item_', '')
        #     item['name'] = name
        #     item['isFeature'] = 1
        #     item['upTime'] = ''
        #     item['area'] = area
        #     item['parts'] = len(play_list)
        #     item['updateTime'] = ''
        #     item['language'] = ''
        #     item['type_tag'] = tags
        #     item['playTimes'] = 0
        #     item['score'] = ''
        #     item['director'] = ''
        #     item['actor'] = ''
        #     item['describe'] = ''
        #     item['isVip'] = 1
        #     item['comment'] = 0
        #     item['recommend'] = ''
        #     item['platform'] = 'youku'
        #     item['sca_app_id'] = 5001
        #     item['cat1'] = '视频'
        #     item['cat2'] = '综艺'
        #     yield item