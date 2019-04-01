# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class YoukuUrlSpider(scrapy.Spider):
    name = 'YouKu_url'
    allowed_domains = ['https://list.youku.com/category/show/c_96_a__s_1_d_1.html.html?spm=a2h1n.8251845.filterPanel.5!2~1~3~A']
    start_urls = ['https://list.youku.com/category/show/c_96_a__s_1_d_1.html.html?spm=a2h1n.8251845.filterPanel.5!2~1~3~A/']

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_film_main, dont_filter=True)

    def parse_film_main(self, response):
        area_page = response.css('a[href^="//list.youku.com/category/show/c_96_s_1_d_1_a_"]')
        area_urls = area_page.css('::attr(href)').extract()
        areas = area_page.css('::text').extract()

        # area_urls = [
        #     '//list.youku.com/category/show/c_96_s_1_d_1_a_中国.html'
        # ]
        # areas = ['中国']
        for area_url, area in zip(area_urls, areas):
            yield Request(url='https:'+area_url, callback=self.parse_film_detail_url, meta={'area': area}, dont_filter=True)
        # print(area_url)
        # print(area)

    def parse_film_detail_url(self, response):
        area = response.meta.get('area')
        feature_urls = response.css('a[href^="//v.youku.com/v_show/id_"]::attr(href)').extract()
        nofeature_urls = response.css('a[href^="http://v.youku.com/v_show/id_"]::attr(href)').extract()
        feature_urls.extend(nofeature_urls)
        for i in range(0, len(feature_urls), 2):
            print(feature_urls)
            # item = UrlItem()
            # item['url'] = feature_urls[i]
            # item['area'] = area
            # item['platform'] = 'youku'
            # yield item
        next_page = response.css('li.next a::attr(href)').extract()
        if next_page:
            yield Request(url='https:' + next_page[0], callback=self.parse_film_detail_url, meta={'area': area}, dont_filter=True)
