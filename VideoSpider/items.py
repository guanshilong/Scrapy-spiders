# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RentItem(scrapy.Item):
    url = scrapy.Field()
    people = scrapy.Field()
    phone = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    way = scrapy.Field()
    nei_name = scrapy.Field()
    address = scrapy.Field()
    decoration = scrapy.Field()
    direction = scrapy.Field()
    area = scrapy.Field()

class TvItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    isFeature = scrapy.Field()
    area = scrapy.Field()
    language = scrapy.Field()
    type_tag = scrapy.Field()
    upTime = scrapy.Field()
    parts = scrapy.Field()
    updateTime = scrapy.Field()
    playTimes = scrapy.Field()
    score = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()
    describe = scrapy.Field()
    isVip = scrapy.Field()
    comment = scrapy.Field()
    recommend = scrapy.Field()
    platform = scrapy.Field()
    # 0电影 1电视剧 2动漫
    classify = scrapy.Field()


class TopItem(scrapy.Item):
    top = scrapy.Field()
    name = scrapy.Field()
    score = scrapy.Field()
    classify = scrapy.Field()
    platform = scrapy.Field()

