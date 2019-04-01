# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from VideoSpider.items import TvItem


class YoukuDetailSpider(scrapy.Spider):
    name = 'Youku_film'
    allowed_domains = ['list.youku.com']
    start_urls = [
            'https://list.youku.com/category/show/c_96_a__s_1_d_1.html.html?spm=a2h1n.8251845.filterPanel.5!2~1~3~A/']
    # custom_settings = {
    #     'LOG_FILE': name + '.log'
    # }
    # def make_requests_from_url(self, url):
    #     sql = "select url,area from film_url where flag = 0 and platform = 'youku' limit 1"
    #     conn = getConn()
    #     cursor = conn.cursor()
    #     cursor.execute(sql)
    #     reslut = cursor.fetchall()
    #     for i in reslut:
    #         url = i[0]
    #         area = i[1]
    #     print(url)
    #     print('============================================')
    #     # url = '//v.youku.com/v_show/id_XMzc5Njc5NjQ3Mg==.html?spm=a2h1n.8251845.0.0'
    #     # url = '//v.youku.com/v_show/id_XMTM5OTY1NTI4MA==.html?spm=a2h1n.8251845.0.0'
    #     # area = 'china'
    #     if 'http' in url:
    #         return Request(url=url, callback=self.parse_url,
    #                        meta={'conn': conn, 'area': area, 'isFeature': 0, 'realurl': url}, dont_filter=True)
    #     else:
    #         return Request(url='https:' + url, callback=self.parse_url,
    #                        meta={'conn': conn, 'area': area, 'isFeature': 1, 'realurl': url}, dont_filter=True)

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_film_main, dont_filter=True)

    def parse_film_main(self, response):
        area_page = response.css('a[href^="//list.youku.com/category/show/c_96_s_1_d_1_a_"]')
        area_urls = area_page.css('::attr(href)').extract()
        areas = area_page.css('::text').extract()
        for area_url, area in zip(area_urls, areas):
            yield Request(url='https:' + area_url, callback=self.parse_film_detail_url, meta={'area': area},
                          dont_filter=True)

    def parse_film_detail_url(self, response):
        area = response.meta.get('area')
        feature_urls = response.css('a[href^="//v.youku.com/v_show/id_"]::attr(href)').extract()
        nofeature_urls = response.css('a[href^="http://v.youku.com/v_show/id_"]::attr(href)').extract()
        feature_urls.extend(nofeature_urls)
        for i in range(0, len(feature_urls), 2):
            detail_url = feature_urls[i]
            if 'http' in detail_url:
                yield Request(url=detail_url, callback=self.parse_url,
                              meta={'area': area, 'isFeature': 0, 'realurl': detail_url}, dont_filter=True)
            else:
                yield Request(url='https:' + detail_url, callback=self.parse_url,
                              meta={'area': area, 'isFeature': 1, 'realurl': detail_url}, dont_filter=True)
        next_page = response.css('li.next a::attr(href)').extract()
        if next_page:
            yield Request(url='https:' + next_page[0], callback=self.parse_film_detail_url, meta={'area': area},
                          dont_filter=True)

    def parse_url(self, response):
        # 有些预告片没有详情链接就放弃爬取
        true_url = response.css('code#bpmodule-playpage-righttitle-code a::attr(href)')
        if true_url:
            if '==' in response.url:
                id = response.url[response.url.rfind('id_') + 3: response.url.rfind('=') + 1]
            else:
                id = response.url[response.url.rfind('id_') + 3: response.url.rfind('.')]
            true_url = true_url.extract()[0]
            area = response.meta['area']
            isFeature = response.meta['isFeature']
            realurl = response.meta['realurl']
            name = response.css('span#subtitle::text').extract()[0]
            if ' ' in name:
                name = name.split(' ')[0]
            type_tag = '/'.join(response.css('a.v-tag::text').extract())
            link_films = response.css('li.yk-col4 a:nth-child(1)::attr(title)').extract()
            link_films = ','.join(link_films[0:5])
            yield Request(url='https:' + true_url, callback=self.parse_detail,
                          meta={'id': id, 'name': name, 'area': area, 'type_tag': type_tag, 'link_films': link_films,
                                'isFeature': isFeature, 'realurl': realurl}, dont_filter=True)
        else:
            return

    def parse_detail(self, response):
        print('------------------parse_detail-----------------------------')
        id = response.meta['id']
        info = response.css('.s-body li')
        info_text = info.css('::text').extract()
        playTimes = comment = 0
        for text in info_text:
            if '播放数' in text:
                playTimes = int(text.split('：')[1].replace(',', '')) / 10000
            if '评论：' in text:
                comment = text.split('：')[1].replace(',', '')
            if '导演：' in text:
                inx = info_text.index(text)
                director = info_text[inx + 1].replace('\'', '’')
                if info_text[inx + 2] == '/':
                    director = director + '/' + info_text[inx + 3].replace('\'', '’')
        name = response.meta['name'].replace('\'', '’')
        area = response.meta['area']
        upTime = '/'.join(info.css('span.pub::text').extract())
        actor = info.css('li.p-performer::attr(title)').extract()[0].replace('\'', '’')
        score = info.css('span.star-num::text').extract()
        score.extend(info.css('i.db-icon-sm + span::text').extract())
        score = '/'.join(score)
        type_tag = response.meta['type_tag']
        isFeature = response.meta['isFeature']
        is_vip = response.css('.vip-free')
        if is_vip:
            isVip = 1
        else:
            isVip = 0
        recommend = response.meta['link_films'].replace('\'', '‘')
        describe = response.css('span.intro-more::text').extract()[0].replace('\r', '').replace('\'', '’').replace('\n', '')
        print(id)
        print(name)
        print(isFeature)
        print(area)
        print(upTime)
        print(type_tag)
        print(director)
        print(actor)
        print(score)
        print(playTimes)
        print(isVip)
        print(comment)
        print(recommend)
        print(describe)

        item = TvItem()
        item['id'] = id
        item['name'] = name
        item['isFeature'] = 1
        item['upTime'] = upTime
        item['area'] = area
        item['parts'] = 1
        item['updateTime'] = ''
        item['language'] = ''
        item['type_tag'] = type_tag
        item['playTimes'] = playTimes
        item['score'] = score
        item['director'] = director
        item['actor'] = actor
        item['describe'] = describe
        item['isVip'] = isVip
        item['comment'] = comment
        item['recommend'] = recommend
        item['platform'] = 'youku'
        item['classify'] = 0
        yield item

        # conn = response.meta['conn']
        # cursor = conn.cursor()
        # cursor.execute(
        #     "insert into films_all values('{0}', '{1}', {2}, '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', {12}, {13}, '{14}')".format(
        #         id, name, isFeature, upTime, area, '', type_tag, playTimes, score, director, actor, describe, is_vip,
        #         comment, recommend)
        # )
        # cursor.execute("update film_url set flag=1 where url = '{0}'".format(response.meta['realurl']))
        # conn.commit()
        # conn.close()
        # yield self.make_requests_from_url("goodGame")
        pass
