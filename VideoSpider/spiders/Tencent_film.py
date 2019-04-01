# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from VideoSpider.items import TvItem
from scrapy import log


class TententDetailSpider(scrapy.Spider):
    name = 'Tencent_film'
    allowed_domains = ['v.qq.com']
    start_urls = ['https://v.qq.com/x/list/movie?sort=19/']
    # custom_settings = {
    #     'LOG_FILE': name + '.log'
    # }

    # def make_requests_from_url(self, url):
    #     sql = "select url from film_url where flag = 0 and platform = 'tencent' limit 1"
    #     conn = getConn()
    #     cursor = conn.cursor()
    #     cursor.execute(sql)
    #     url = cursor.fetchone()[0]
    #     return Request(url=url, callback=self.parse_url, meta={'conn': conn}, dont_filter=True)

    # --------------------获取url部分------------
    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_film_main, dont_filter=True)

    # 电影部分
    def parse_film_main(self, response):
        areaList = response.css('.filter_line')[1].css('a::attr(href)').extract()
        areaList.remove(areaList[0])
        for areaurl in areaList:
            yield Request(url=parse.urljoin(response.url, areaurl), callback=self.parse_film_detail_url, dont_filter=True)
            pass

    def parse_film_detail_url(self, response):
        detail_urls = response.css('.figure_title a::attr(href)').extract()
        # detail_urls = ['https://v.qq.com/x/cover/4myi5m71d14pdmr.html', 'https://v.qq.com/x/cover/4myi5m71d14pdmr.html']
        for detail_url in detail_urls:
            yield Request(detail_url, callback=self.parse_url, meta={'url': detail_urls}, dont_filter=True)
        next_page = response.css('.page_next::attr(href)').extract()
        if next_page and 'java' not in next_page[0]:
            yield Request(parse.urljoin(response.url, next_page[0]), callback=self.parse_film_detail_url, dont_filter=True)

    def parse_url(self, response):
        id = response.url[response.url.rfind('/')+1:response.url.rfind('.')]
        url = 'https://v.qq.com/detail/' + id[0:1] + '/' + id + '.html'
        isVip = response.css('h4.tit::text')
        if isVip:
            isVip = 1
        else:
            isVip = 0
        playTimes = response.css('#mod_cover_playnum::text').extract()
        if playTimes:
            playTimes = playTimes[0]
            if '万' in playTimes:
                playTimes = playTimes[0:len(playTimes)-1]
            elif '亿' in playTimes:
                playTimes = int(float(playTimes[0:len(playTimes)-1])*10000)
            else:
                playTimes = float(playTimes[0:len(playTimes)-1])/10000
        else:
            playTimes = 0
        yield Request(url=url, callback=self.parse, meta={'realurl': response.url, 'id': id, 'isVip': isVip, 'playTimes': playTimes}, dont_filter=True)

    def parse(self, response):
        id = response.meta['id']
        name = response.css('meta[name="twitter:title"]::attr(content)').extract()[0].replace('\'', '')
        tag = response.css('.type_item')
        if len(tag) == 0:
            area = ''
            language = ''
            upTime = ''
        if len(tag) == 1:
            if tag[0].css('span::text').extract()[0].replace('　', '') == '地区:':
                area = tag[0].css('span::text').extract()[1]
                language = ''
                upTime = ''
            elif tag[0].css('span::text').extract()[0].replace('　', '') == '语言:':
                language = tag[0].css('span::text').extract()[1]
                area = ''
                upTime = ''
        if len(tag) == 2:
            area = tag[0].css('span::text').extract()[1]
            language = ''
            upTime = tag[1].css('span::text').extract()[1]
        elif len(tag) == 3:
            if tag[0].css('span::text').extract()[0].replace('　', '') == '地区:':
                area = tag[0].css('span::text').extract()[1]
                language = tag[1].css('span::text').extract()[1]
                upTime = tag[2].css('span::text').extract()[1]
            else:
                area = tag[1].css('span::text').extract()[1]
                language = ''
                upTime = tag[2].css('span::text').extract()[1]
            pass
        elif len(tag) == 4:
            area = tag[1].css('span::text').extract()[1]
            language = tag[2].css('span::text').extract()[1]
            upTime = tag[3].css('span::text').extract()[1]
            pass
        type_tag = ','.join(response.css('.tag::text').extract())
        people = response.css('span[_stat="info:actor_name"]::text').extract()
        director_flag = response.css('.director')
        if people:
            if director_flag:
                director = people[0].replace('\'', '')
                people.remove(people[0])
            else:
                director = ''
            actor = ','.join(people).replace('\'', '')
        else:
            director = ''
            actor = ''
        score = '/'.join(response.css('.score::text').extract())
        describe = response.css('._desc_txt_lineHight::text')
        if describe:
            describe = describe.extract()[0].replace('\r', '').replace('\'', '’').replace('\n', '')
        else:
            describe = ''
        isVip = response.meta['isVip']
        playTimes = response.meta['playTimes']
        recommend = ','.join(response.css('.figure_title a[href^="http://v.qq.com/detail/"]::attr(title)').extract()).replace('\'', '’')
        print(id)
        print(name)
        print(area)
        print(upTime)
        print(type_tag)
        print(director)
        print(actor)
        print(score)
        print(playTimes)
        print(isVip)
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
        item['language'] = language
        item['type_tag'] = type_tag
        item['playTimes'] = playTimes
        item['score'] = score
        item['director'] = director
        item['actor'] = actor
        item['describe'] = describe
        item['isVip'] = isVip
        item['comment'] = 0
        item['recommend'] = recommend
        item['platform'] = 'tencent'
        item['classify'] = 0
        yield item
        # conn = response.meta['conn']
        # cursor = conn.cursor()
        # cursor.execute(
        #     "insert into films_tencent values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', {11}, {12},'{13}')".format(
        #         id, name, upTime, area, language,type_tag, playTimes, score, director, actor, describe, isVip, 0, recommend)
        #             )
        # cursor.execute("update film_url set flag=1 where url = '{0}'".format(response.meta['realurl']))
        # conn.commit()
        # conn.close()
        # yield self.make_requests_from_url("goodGame")
