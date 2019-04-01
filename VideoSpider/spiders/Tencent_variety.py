# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
from VideoSpider.items import TvItem

class TencentVarietySpider(scrapy.Spider):
    name = 'Tencent_variety'
    allowed_domains = ['v.qq.com']
    start_urls = ['http://v.qq.com/x/list/variety']

    def parse(self, response):
        common = response.css('.filter_content')[0]
        channels = common.css('a::text').extract()
        channel_links = common.css('a::attr(href)').extract()
        for channel, channel_link in zip(channels[1: len(channels)], channel_links[1: len(channel_links)]):
            url = parse.urljoin(self.start_urls[0], channel_link)
            yield Request(url=url, callback=self.parse_page_info, meta={'channel': channel}, dont_filter=True)

    def parse_page_info(self, response):
        common = response.css('.figures_list')
        if common:
            newsreel_urls = common[0].css('.list_item .figure::attr(href)').extract()
            # newsreel_urls = ['https://v.qq.com/x/cover/jx7g4sm320sqm7i.html']
            for newsreel_url in newsreel_urls:
                yield Request(url=newsreel_url, callback=self.pase_variety_info, meta={'area': response.meta['channel']})
        next_page = response.css('.page_next::attr(href)').extract()
        if next_page and 'java' not in next_page[0]:
            yield Request(url=parse.urljoin(self.start_urls[0], next_page[0]), callback=self.parse_page_info, meta={'area': response.meta['channel']}, dont_filter=True)

    def pase_variety_info(self, response):
        area = response.meta['area']
        name = response.css('.player_title a::text').extract()[0]
        play_list = response.css('a[_stat="video-list-column:click"]::attr(href)').extract()
        play_list = [url[url.rfind('/') + 1: url.rfind('.')] for url in play_list]
        play_list.append(response.url[response.url.rfind('/') + 1: response.url.rfind('.')])
        tags = response.css('._video_tags a::text').extract()
        if tags:
            tags = '/'.join(tags)
        else:
            tags = ''
        print('-------------------------------------------')
        print(name)
        print(area)
        print(tags)
        for id in set(play_list):
            item = TvItem()
            item['id'] = id
            item['name'] = name
            item['isFeature'] = 1
            item['upTime'] = ''
            item['area'] = area
            item['parts'] = len(play_list)
            item['updateTime'] = ''
            item['language'] = ''
            item['type_tag'] = tags
            item['playTimes'] = 0
            item['score'] = ''
            item['director'] = ''
            item['actor'] = ''
            item['describe'] = ''
            item['isVip'] = 1
            item['comment'] = 0
            item['recommend'] = ''
            item['platform'] = 'tencent'
            item['sca_app_id'] = 5006
            item['cat1'] = '视频'
            item['cat2'] = '综艺'
            yield item


