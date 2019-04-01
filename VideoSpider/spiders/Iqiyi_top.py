# -*- coding: utf-8 -*-
import scrapy
from VideoSpider.items import TopItem


class IqiyiTopSpider(scrapy.Spider):
    name = 'Iqiyi_top'
    allowed_domains = ['v.iqiyi.com']
    start_urls = ['https://v.iqiyi.com/index/dianshiju/index.html'
                  , 'https://v.iqiyi.com/index/dianying/index.html'
                  , 'https://v.iqiyi.com/index/dongman/index.html'
                  ]

    def parse(self, response):
        common = response.css('tr[data-ranklist-elem="item"]')
        if 'dianying' in response.url:
            classify = 'movie'
        elif 'dianshi' in response.url:
            classify = 'tv'
        elif 'dongman' in response.url:
            classify = 'anime'
        names = common.css('a.item_name::text').extract()
        scores = common.css('span.item_num::text').extract()
        scores = [i.replace(',', '') for index, i in enumerate(scores) if index % 3 == 0]
        for pos, name in enumerate(names):
            print('------------------------------------------')
            print((pos + 1, name, classify, scores[pos]))
            item = TopItem()
            item['top'] = pos + 1
            item['name'] = name
            item['score'] = scores[pos]
            item['classify'] = classify
            item['platform'] = 'Iqiyi'
            # yield item

