# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy import Request
import json
import re
from VideoSpider.items import TvItem

class IqiyiTvSpider(scrapy.Spider):
    name = 'Iqiyi_tv'
    allowed_domains = ['list.iqiyi.com']
    start_urls = ['https://list.iqiyi.com/www/2/----------------iqiyi--.html']

    def parse(self, response):
        common = response.css('.mod_category_item')[2]
        area_urls = common.css('a::attr(href)').extract()
        # area_urls = ['1', '/www/2/15-------------24-1-1-iqiyi--.html']
        areas = common.css('a::text').extract()
        for (url, area) in zip(area_urls[1: len(area_urls)], areas[1: len(areas)]):
            yield Request(url=parse.urljoin(response.url, url), callback=self.parse_page_info, meta={'area': area},dont_filter=True)

    def parse_page_info(self, response):
        detail_urls = response.css('div.site-piclist_pic a::attr(href)').extract()
        # detail_urls = ['https://www.iqiyi.com/a_19rrhc4b55.html']
        for url in detail_urls:
            yield Request(url=url.replace('http', 'https'), callback=self.parse_detail_info, meta={'area': response.meta['area']}, dont_filter=True)
        nextpage = response.css('a[data-key="down"]::attr(href)').extract()
        if nextpage:
            yield Request(url=parse.urljoin(response.url, nextpage[0]), callback=self.parse_page_info, meta={'area': response.meta['area']}, dont_filter=True)

    def parse_detail_info(self, response):
        info = response.css('div.info-intro')
        if info:
            info = info[0]
            language = type_tag = ''
            url = info.css('a.info-intro-title::attr(href)').extract()
            # name = info.css('a.info-intro-title::text').extract()
            parts = response.css('.albumSubTab-container .title-update-num::text').extract()
            if parts:
                parts = parts[0]
            else:
                parts = 1
            if url:
                url = url[0]
            else:
                url = info.css('.info-intro a.albumPlayBtn::attr(href)').extract()
                # name = info.css('.info-intro a::text').extract()
                if url:
                    url = url[0]
                    # name = name[0]
            tab = info.css('.episodeIntro-line p ::text').extract()
            play_list = response.css('div[data-widget="albumlist-render"] .site-piclist_pic a.site-piclist_pic_link[href^="http"]::attr(href)').extract()
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
        elif 'dianshiju' in response.url:
            language = parts = type_tag = ''
            play_list = []
        else:
            url = response.css('.album-playArea a::attr(href)').extract()[0]
            parts = 0
            type_tag = '/'.join(response.css('p[itemprop="genre"] a::text').extract())
            language = response.css('p[itemprop="inLanguage"] a::text').extract()
            if language:
                language = language[0]
            else:
                language = ''
            play_list = []
        if 'http' in url:
            yield Request(url.replace('http:', 'https:'), callback=self.parse_info, meta={'area': response.meta['area'], 'language': language, 'parts': parts, 'type_tag': type_tag, 'play_list': play_list}, dont_filter=True)
        else:
            yield Request('https:' + url, callback=self.parse_info, meta={'area': response.meta['area'], 'language': language, 'parts': parts, 'type_tag': type_tag, 'play_list': play_list}, dont_filter=True)

    def parse_info(self, response):
        print(response.url)
        area = response.meta['area']
        # name = response.meta['name']
        # if not name:
        name = response.css('meta[name="irAlbumName"]::attr(content)').extract()[0]
        language = response.meta['language']
        type_tag = response.meta['type_tag']
        parts = response.meta['parts']
        play_list = response.meta['play_list']
        list_json = response.css('div[is="i71-playpage-sdrama-list"]').extract()
        if list_json:
            list_json = list_json[0]
            re_list = re.findall('"url":"http:[\s\S]+?"', list_json)
            play_list.extend(re_list)
        play_list.append(response.url)
        playList = []
        for url in play_list:
            itemId = url[url.rfind('_') + 1:url.rfind('.')]
            playList.append(itemId)
        playList = set(playList)
        is_vip = response.css('.qy-player-side-vip::attr(is-mixer-album)').extract()
        if is_vip:
            is_vip = is_vip[0]
            if 'true' in is_vip:
                is_vip = 1
            else:
                is_vip = 0
        else:
            is_vip = 0

        upTime = updateTime = recommend = play_times = score = ''
        id = response.url[response.url.rfind('_') + 1:response.url.rfind('.')]
        director = response.css('a[itemprop="director"]::text').extract()
        director = ','.join(director)
        actor = response.css('a[itemprop="actor"]::text').extract()
        actor = ','.join(actor)
        describe = response.css('span.content-paragraph::text').extract()
        if describe:
            describe = describe[0]
        else:
            describe = ''
        print('----------------------------------------')
        print(response.url)
        print(len(playList))
        print(id)
        print(name)
        print(language)
        print(type_tag)
        print(area)
        print(parts)
        print(director)
        print(actor)
        print(describe)
        print(is_vip)
        for id in playList:
            item = TvItem()
            item['id'] = id
            item['name'] = name
            item['isFeature'] = 1
            item['upTime'] = upTime
            item['area'] = area
            item['parts'] = parts
            item['updateTime'] = updateTime
            item['language'] = language
            item['type_tag'] = type_tag
            item['playTimes'] = play_times
            item['score'] = score
            item['director'] = director
            item['actor'] = actor
            item['describe'] = describe
            item['isVip'] = is_vip
            item['comment'] = 0
            item['recommend'] = recommend
            item['platform'] = 'iqiyi'
            item['classify'] = 1
            yield item

