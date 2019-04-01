# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from VideoSpider.items import TopItem
import time
import json


class YoukuTopSpider(scrapy.Spider):
    name = 'Youku_top'
    allowed_domains = ['top.youku.com']
    start_urls = ['http://top.youku.com/rank?spm=a2ha1.12325017.m_2544.5~1~3!6~8!2~A']

    def start_requests(self):
        types = [{
            'name': 'tv',
            'type': 1,
            'id': '97'
        }, {
            'name': 'movie',
            'type': 1,
            'id': '96'
        }, {
            'name': 'variety',
            'type': 1,
            'id': '85'
        }, {
            'name': 'anime',
            'type': 1,
            'id': '100'
        }, {
            'name': 'newsreel',
            'type': 1,
            'id': '84'
        }]

        rankUrl = 'http://index.api.youku.com'
        for i in types:
            h = i['type']
            cata = i['name']
            d = '700009' if 1 == h else '700008'
            s = ''
            o = i['id']
            timestamp = int(time.time() * 1000)
            url = rankUrl + '/getData?num=' + d + '&orderPro=vv&startindex=1&endindex=30&' + s + 'channelId=' + o + '&dateDim=d' + '&jsoncallback=jQuery111207513656543054685_' + str(timestamp) + '&jsonp&_=' + str(timestamp + 1)
            yield Request(url=url, meta={'cata': cata}, dont_filter=True)

    def parse(self, response):
        cata = response.meta['cata']
        txt = response.text
        result = txt[txt.index('(') + 1: txt.rindex(')')]
        result = json.loads(result)
        data = result['result']['data']
        for pos, top in enumerate(data):
            print('------------------------------')
            name = top['title']
            print((pos + 1, name, cata))
            item = TopItem()
            item['top'] = pos + 1
            item['name'] = name
            item['score'] = 0
            item['classify'] = cata
            item['platform'] = 'Youku'
            yield item

