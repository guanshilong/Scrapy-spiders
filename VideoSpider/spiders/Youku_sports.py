# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from VideoSpider.items import TvItem
import re


class YouuSportsSpider(scrapy.Spider):
    name = 'Youku_sports'
    allowed_domains = ['list.youku.com']
    start_urls = ['https://list.youku.com/category/show/c_98.html']

    def parse(self, response):
        area_page = response.css('a[href^="//list.youku.com/category/show/c_98_s_6_d_1_g_"]')
        area_urls = area_page.css('::attr(href)').extract()
        areas = area_page.css('::text').extract()
        for area_url, area in zip(area_urls, areas):
            yield Request(url='https:' + area_url, callback=self.parse_page_detail_url, meta={'area': area}, dont_filter=True)

    def parse_page_detail_url(self, response):
        area = response.meta.get('area')
        sports_urls = response.css('a[href^="//v.youku.com/v_show/id_"]::attr(href)').extract()
        if not sports_urls:
            sports_urls = response.css('a[href^="//v.youku.com/show/id_"]::attr(href)').extract()
        sports_urls = [url for (index, url) in enumerate(sports_urls) if index % 2 == 0]
        for sports_url in sports_urls:
            yield Request(url='https:' + sports_url, callback=self.parse_sports_info, meta={'area': area, 'id': id}, dont_filter=True)
        next_page = response.css('li.next a::attr(href)').extract()
        if next_page:
            yield Request(url='https:' + next_page[0], callback=self.parse_page_detail_url, meta={'area': area},
                          dont_filter=True)

    def parse_sports_info(self, response):
        common = response.css('code#bpmodule-playpage-righttitle-code')
        detail_url = common.css('a::attr(href)').extract()
        if detail_url:
            # 有详情链接才爬取
            detail_url = detail_url[0]
            name = common.css('a::text').extract()[0]
            area = response.meta['area']
            parts = ''.join(response.css('.mr3 ::text').extract())
            parts = re.search(r'[0-9]+', parts).group()
            type_tag = '/'.join(response.css('a.v-tag::text').extract())
            if '==' in response.url:
                id = response.url[response.url.rfind('id_') + 3: response.url.rfind('=') + 1]
            else:
                id = response.url[response.url.rfind('id_') + 3: response.url.rfind('.')]
            play_list = response.css('div[id^="listitem_page"] .item-cover::attr(item-id)').extract()
            play_list.append('item_' + id)
            play_list = set(play_list)
            yield Request(url='https:' + detail_url, callback=self.parse_sports_detail,
                          meta={'play_list': play_list, 'name': name, 'area': area, 'type_tag': type_tag,'parts': parts}, dont_filter=True)

    def parse_sports_detail(self, response):
        play_list = response.meta['play_list']
        name = response.meta['name']
        director = actor = score = upTime = describe = update_time = ''
        area = response.meta['area']
        type_tag = response.meta['type_tag']
        recommend = ''
        parts = response.meta['parts']
        info = response.css('.s-body li')
        score_css = info.css('span.star-num::text').extract()
        if score_css:
            score = score_css[0]
        upTime_css = info.css('span.pub::text').extract()
        if upTime_css:
            upTime = upTime_css[0]
        renew = info.css('.p-renew::text').extract()
        describe_css = response.css('span.intro-more::text').extract()
        if describe_css:
            describe = describe_css[0].replace('\r', '').replace('\'', '’').replace('\n', '')
        if renew:
            update_time = renew[0].replace(' ', '')

        info_text = info.css('::text').extract()
        play_times = comment = 0
        for text in info_text:
            if '播放数' in text:
                play_times = int(text.split('：')[1].replace(',', '')) / 10000
            if '评论：' in text:
                comment = text.split('：')[1].replace(',', '')
            if '主持人：' in text:
                actor = text.replace('主持人：', '’').replace('\'', '’')
        is_vip = response.css('.vip-free')
        if is_vip:
            is_vip = 1
        else:
            is_vip = 0
        print('--------------------------------------------------------')
        print(response.url)
        print(name)
        print(area)
        print(type_tag)
        print(upTime)
        print(score)
        print('parts', parts)
        print('vip', is_vip)
        print('play', play_times)
        print('update', update_time)
        print('comment', comment)
        print('director', director)
        print('actor', actor)
        print('recommend', recommend)
        print(describe)
        print(play_list)
        for id in play_list:
            item = TvItem()
            item['id'] = id.replace('item_', '')
            item['name'] = name
            item['isFeature'] = 1
            item['upTime'] = upTime
            item['area'] = area
            item['parts'] = parts
            item['updateTime'] = update_time
            item['language'] = ''
            item['type_tag'] = type_tag
            item['playTimes'] = play_times
            item['score'] = score
            item['director'] = director
            item['actor'] = actor
            item['describe'] = describe
            item['isVip'] = is_vip
            item['comment'] = comment
            item['recommend'] = recommend
            item['platform'] = 'youku'
            item['sca_app_id'] = 5001
            item['cat1'] = '视频'
            item['cat2'] = '体育'
            yield item
