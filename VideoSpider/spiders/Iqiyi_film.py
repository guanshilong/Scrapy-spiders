# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
from VideoSpider.items import TvItem


class IqiyiFilmSpider(scrapy.Spider):
    name = 'Iqiyi_film'
    allowed_domains = ['www.iqiyi.com']
    start_urls = ['https://list.iqiyi.com/www/1/----------------iqiyi--.html']

    def parse(self, response):
        common = response.css('.mod_category_item')[2]
        area_urls = common.css('a::attr(href)').extract()
        # area_urls = ['1', '/www/1/1-------------24-1-1-iqiyi--.html']
        areas = common.css('a::text').extract()
        for (url, area) in zip(area_urls[1: len(area_urls)], areas[1: len(areas)]):
            yield Request(url=parse.urljoin(response.url, url), callback=self.parse_page_info, meta={'area': area},
                          dont_filter=True)

    def parse_page_info(self, response):
        detail_urls = response.css('div.site-piclist_pic a::attr(href)').extract()
        # detail_urls = ['https://www.iqiyi.com/v_19rrifvgmy.html', 'https://www.iqiyi.com/v_19rriful3v.html']
        for url in detail_urls:
            yield Request(url=url.replace('http', 'https'), callback=self.parse_info, meta={'area': response.meta['area']})
        nextpage = response.css('a[data-key="down"]::attr(href)').extract()
        if nextpage:
            yield Request(url=parse.urljoin(response.url, nextpage[0]), callback=self.parse_page_info,
                          meta={'area': response.meta['area']}, dont_filter=True)

    def parse_info(self, response):
        area = response.meta['area']
        updateTime = upTime = language = recommend = type_tag = play_times = score = ''
        id = response.url[response.url.rfind('_') + 1:response.url.rfind('.')]
        name = response.css('#widget-videotitle::text').extract()
        if name:
            name = name[0]
        else:
            name = response.css('meta[name="irTitle"]::attr(content)').extract()[0]
        director = response.css('a[itemprop="director"]::text').extract()
        director = ','.join(director)
        actor = response.css('a[itemprop="actor"]::text').extract()
        actor = ','.join(actor)
        describe = response.css('span.content-paragraph::text').extract()
        if describe:
            describe = describe[0]
        else:
            describe = ''
        is_vip = 0
        print('----------------------------------------')
        print(response.url)
        print(id)
        print(name)
        print(area)
        print(director)
        print(actor)
        print(describe)
        item = TvItem()
        item['id'] = id
        item['name'] = name
        item['isFeature'] = 1
        item['upTime'] = upTime
        item['area'] = area
        item['parts'] = 1
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
        item['classify'] = 0
        yield item
