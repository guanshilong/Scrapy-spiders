# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy import Request
from VideoSpider.items import TvItem


class TencentNewsreelSpider(scrapy.Spider):
    name = 'Tencent_newsreel'
    allowed_domains = ['v.qq.com']
    start_urls = ['http://v.qq.com/x/list/doco']

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
                yield Request(url=newsreel_url, callback=self.parse_newsreel_info, meta={'channel': response.meta['channel']})
        next_page = response.css('.page_next::attr(href)').extract()
        if next_page and 'java' not in next_page[0]:
            yield Request(url=parse.urljoin(self.start_urls[0], next_page[0]), callback=self.parse_page_info, meta={'channel': response.meta['channel']}, dont_filter=True)

    def parse_newsreel_info(self, response):
        channel = response.meta['channel']
        name = play_times = ''
        detail_url = parse.urljoin(self.start_urls[0], response.css('.player_title a::attr(href)').extract()[0])
        name_pre = response.css('.player_title a::text').extract()
        if name_pre:
            name = name_pre[0]
        play_times_pre = response.css('#mod_cover_playnum::text').extract()
        if play_times_pre:
            play_times = play_times_pre[0]
        play_list = response.css('ul._hot_wrapper li.list_item::attr(id)').extract()
        yield Request(url=detail_url, callback=self.parse_detail_info, meta={'play_list': play_list, 'channel': channel, 'name': name, 'play_times': play_times}, dont_filter=True)

    def parse_detail_info(self, response):
        id = response.url[response.url.rfind('/') + 1:response.url.rfind('.')]
        play_list = response.meta['play_list']
        play_list.append(id)
        play_list = set(play_list)
        name = response.meta['name']
        area = response.meta['channel']
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
        # print(director)
        # print(actor)
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
            item['director'] = ''
            item['actor'] = ''
            item['describe'] = describe
            item['isVip'] = is_vip
            item['comment'] = 0
            item['recommend'] = recommend
            item['platform'] = 'tencent'
            item['classify'] = 3
            yield item
