# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
import re
from VideoSpider.items import TvItem

class IqiyiVarietySpider(scrapy.Spider):
    name = 'Iqiyi_variety'
    allowed_domains = ['list.iqiyi.com']
    start_urls = ['http://list.iqiyi.com/www/6/----------------iqiyi--.html']

    def parse(self, response):
        common = response.css('.mod_category_item')[1]
        area_urls = common.css('a::attr(href)').extract()
        areas = common.css('a::text').extract()
        for (url, area) in zip(area_urls[1: len(area_urls)], areas[1: len(areas)]):
            yield Request(url=parse.urljoin(response.url, url), callback=self.parse_page_info, meta={'area': area}, dont_filter=True)


    def parse_page_info(self, response):
        detail_urls = response.css('div.site-piclist_pic a::attr(href)').extract()
        for url in detail_urls:
            yield Request(url=url.replace('http:', 'https:'), callback=self.parse_detail_info, meta={'area': response.meta['area']}, dont_filter=True)
        nextpage = response.css('a[data-key="down"]::attr(href)').extract()
        if nextpage:
            yield Request(url=parse.urljoin(response.url, nextpage[0]), callback=self.parse_page_info, meta={'area': response.meta['area']}, dont_filter=True)

    def parse_detail_info(self, response):
        start_url = response.css('div.intro-btns a::attr(href)').extract()
        info = response.css('div.info-intro')
        if info:
            info = info[0]
            language = type_tag = ''
            url = info.css('a.info-intro-title::attr(href)').extract()
            parts = response.css('.albumSubTab-container .title-update-num::text').extract()
            if parts:
                parts = parts[0]
            else:
                parts = 0
            if url:
                url = url[0]
            else:
                url = info.css('.info-intro a::attr(href)').extract()
                if url:
                    url = url[0]
            tab = info.css('.episodeIntro-line p ::text').extract()
            for text in tab:
                if '语言' in text:
                    language = tab[tab.index(text) + 1]
                if '类型' in text:
                    inx = tab.index(text) + 1
                    type_tag = tab[inx]
                    while True:
                        inx = inx + 1
                        if '/' in tab[inx]:
                            type_tag = type_tag + '/' + tab[inx+1]
                            inx = inx + 1
                        else:
                            break
        if start_url:
            start_url = start_url[0]
        else:
            return
        if 'http' not in start_url:
            yield Request(url='https:'+start_url, callback=self.parse_detail, meta={'area': response.meta['area'], 'language': language, 'type_tag': type_tag},dont_filter=True)
        else:
            yield Request(url=start_url.replace('http:', 'https:'), callback=self.parse_detail, meta={'area': response.meta['area'], 'language': language, 'type_tag': type_tag}, dont_filter=True)

    def parse_detail(self, response):
        area = response.meta['area']
        tags = response.meta['type_tag']
        language = response.meta['language']
        name = response.css('meta[name="irAlbumName"]::attr(content)').extract()[0]
        list_json = response.css('div[is="i71-playpage-source-list"]').extract()
        if list_json:
            list_json = list_json[0]
            play_list = re.findall('"url":"http:[\s\S]+?"', list_json)
        play_list.append(response.url)
        playList = []
        for url in play_list:
            itemId = url[url.rfind('_') + 1:url.rfind('.')]
            playList.append(itemId)
        print('----------------------------------')
        print(name)
        print(area)
        print(tags)
        for id in set(playList):
            item = TvItem()
            item['id'] = id
            item['name'] = name
            item['isFeature'] = 1
            item['upTime'] = ''
            item['area'] = area
            item['parts'] = len(play_list)
            item['updateTime'] = ''
            item['language'] = language
            item['type_tag'] = tags
            item['playTimes'] = 0
            item['score'] = ''
            item['director'] = ''
            item['actor'] = ''
            item['describe'] = ''
            item['isVip'] = 1
            item['comment'] = 0
            item['recommend'] = ''
            item['platform'] = 'iqiyi'
            item['sca_app_id'] = 5018
            item['cat1'] = '视频'
            item['cat2'] = '综艺'
            # yield item
