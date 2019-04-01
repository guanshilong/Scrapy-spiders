# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
from VideoSpider.items import TvItem


class TencentTvSpider(scrapy.Spider):
    name = 'Tencent_tv'
    allowed_domains = ['v.qq.com']
    start_urls = ['http://v.qq.com/x/list/tv']

    def parse(self, response):
        common = response.css('.filter_content')[1]
        areas = common.css('a::text').extract()
        area_links = common.css('a::attr(href)').extract()
        for area, area_link in zip(areas[1: len(areas)], area_links[1: len(area_links)]):
            url = parse.urljoin(self.start_urls[0], area_link)
            yield Request(url=url, callback=self.parse_page_info, meta={'area': area}, dont_filter=True)

    def parse_page_info(self, response):
        common = response.css('.figures_list')
        if common:
            tv_urls = common[0].css('.list_item .figure::attr(href)').extract()
            # tv_urls = ['https://v.qq.com/x/cover/sdp001274zzbw54.html']
            for tv_url in tv_urls:
                yield Request(url=tv_url, callback=self.parse_tv_info, meta={'area': response.meta['area']})
        next_page = response.css('.page_next::attr(href)').extract()
        if next_page and 'java' not in next_page[0]:
            yield Request(url=parse.urljoin(self.start_urls[0], next_page[0]), callback=self.parse_page_info, meta={'area': response.meta['area']}, dont_filter=True)

    def parse_tv_info(self, response):
        area = response.meta['area']
        detail_url = parse.urljoin(self.start_urls[0], response.css('.player_title a::attr(href)').extract()[0])
        name = response.css('.player_title a::text').extract()[0]
        all = response.css('.director ::text').extract()
        all_spilt = ''.join(all).replace('   ', '').partition(' 演员:')
        director = all_spilt[0].replace('导演:', '').replace(' ', '')
        actor = all_spilt[2].replace(' ', '').replace('\n', '')
        play_times = response.css('#mod_cover_playnum::text').extract()[0]
        play_list = response.css('span[_stat="videolist:click"]::attr(id)').extract()
        if not play_list:
            play_list = response.css('ul#_pic_title_list_ul li.list_item::attr(id)').extract()
        yield Request(url=detail_url, callback=self.parse_detail_info, meta={'play_list': play_list, 'area': area, 'name': name, 'director': director, 'actor': actor, 'play_times': play_times}, dont_filter=True)

    def parse_detail_info(self, response):
        id = response.url[response.url.rfind('/') + 1:response.url.rfind('.')]
        play_list = response.meta['play_list']
        play_list.append(id)
        play_list = set(play_list)
        name = response.meta['name']
        area = response.meta['area']
        director = response.meta['director']
        actor = response.meta['actor']
        score = '/'.join(response.css('.video_score span.score::text').extract())
        is_vip = response.css('img[alt="VIP"]').extract()
        describe = language = parts = up_time = update_time = ''
        describe_tag = response.css('span._desc_txt_lineHight::text').extract()
        if describe_tag:
            describe = describe_tag[0]
        recommend = ','.join(r for r in response.css('._recom_list .figure_title a::text').extract() if name not in r)
        play_times = response.meta['play_times']
        if '万' in play_times:
            play_times = play_times[0:len(play_times)-1]
        elif '亿' in play_times:
            play_times = int(float(play_times[0:len(play_times)-1])*10000)
        elif int(play_times) == 0:
            play_times = play_times
        elif play_times:
            play_times = float(play_times[0:len(play_times)-1])/10000
        else:
            play_times = ''
        if is_vip:
            is_vip = 1
        else:
            is_vip = 0
        type_tag = '/'.join(response.css('.tag_list a::text').extract())
        all_type_cf = response.css('.type_item span::text').extract()
        for index, cf in enumerate(all_type_cf):
            cf = cf.replace('　', '')
            if '语言' in cf:
                language = all_type_cf[index + 1]
            elif '总集数:' == cf:
                parts = all_type_cf[index + 1]

            elif '出品时间:' == cf:
                up_time = all_type_cf[index + 1]
            elif cf == u'更新时间:':
                update_time = all_type_cf[index + 1]
        print('------------------------------------------------------------')
        print(response.url)
        print('len:', len(play_list))
        print(id)
        print(name)
        print(area)
        print(is_vip)
        print(type_tag)
        print(language)
        print(score)
        print(parts)
        print(play_times)
        print(up_time)
        print(director)
        print(actor)
        print(update_time)
        print(recommend)
        print(describe)
        for id in play_list:
            item = TvItem()
            item['id'] = id
            item['name'] = name
            item['isFeature'] = 1
            item['upTime'] = up_time
            item['area'] = area
            item['parts'] = parts
            item['updateTime'] = update_time
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
            item['platform'] = 'tencent'
            item['classify'] = 1
            yield item