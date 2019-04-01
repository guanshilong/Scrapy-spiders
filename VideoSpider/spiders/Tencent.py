# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse


class TencentSpider(scrapy.Spider):
    name = 'Tencent'
    allowed_domains = ['https://v.qq.com/x/list/movie?sort=19']
    start_urls = ['https://v.qq.com/x/list/movie?sort=19/']

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_film_main, dont_filter=True)

    # 电影部分
    # 获取电影地区链接
    def parse_film_main(self, response):
        areaList = response.css('.filter_line')[1].css('a::attr(href)').extract()
        areas = response.css('.filter_line')[1].css('a::text').extract()
        areaList.remove(areaList[0])
        areas.remove(areas[0])
        # areaList = [
        #             'https://v.qq.com/x/list/movie?offset=0&iarea=1'
        #             # , 'https://v.qq.com/x/list/movie?offset=0&iarea=2'
        #             ]
        # areas = [
        #     '内地'
        #     # , '香港'
        #         ]
        for areaurl, area in zip(areaList, areas):
            print(parse.urljoin(response.url, areaurl))
            yield Request(url=parse.urljoin(response.url, areaurl), callback=self.parse_film_detail_url, meta={'area':area}, dont_filter=True)
            pass

    def parse_film_detail_url(self, response):
        detail_urls = response.css('.figure_title a::attr(href)').extract()
        area = response.meta.get('area')
        for detail_url in detail_urls:
            # item = UrlItem()
            # item['url'] = detail_url
            # item['area'] = area
            # item['platform'] = 'tencent'
            # yield item
            pass
        next_page = response.css('.page_next::attr(href)').extract()
        if next_page:
            yield Request(parse.urljoin(response.url, next_page[0]), callback=self.parse_film_detail_url, meta={'area':area}, dont_filter=True)


