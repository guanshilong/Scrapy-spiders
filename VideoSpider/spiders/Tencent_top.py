# -*- coding: utf-8 -*-
import scrapy
from VideoSpider.items import TopItem

class TencentTopSpider(scrapy.Spider):
    name = 'Tencent_top'
    allowed_domains = ['v.qq.com']
    start_urls = ['https://v.qq.com/x/rank/']

    def parse(self, response):
        common = response.css('.mod_row_movie')
        for i in common:
            classify = i.css('.mod_row_movie::attr(id)').extract()[0]
            catas = i.css('a[_stat="rank_title"]::text').extract()
            tops = i.css('.mod_rank_list')
            for cata, top in zip(catas, tops):
                # area_ids = top.css('span.num::text').extract()
                names = top.css('.figure_title a::text').extract()
                names.extend(top.css('span.name::text').extract())
                for pos, name in enumerate(names):
                    print('------------------------------------------')
                    print((pos + 1, name, cata + '/' + classify))
                    item = TopItem()
                    item['top'] = pos + 1
                    item['name'] = name
                    item['score'] = 0
                    item['classify'] = cata + '/' + classify
                    item['platform'] = 'Tencent'
                    # yield item




