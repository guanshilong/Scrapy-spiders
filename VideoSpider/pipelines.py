# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import datetime
from twisted.enterprise import adbapi
from VideoSpider.items import RentItem
from VideoSpider.items import TvItem

today = datetime.date.today()


class VideospiderPipeline(object):
    def process_item(self, item, spider):
        return item


class FilmPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls, crawler):
        '''
            1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
            2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
            3、可以通过类来调用，就像C.f()，相当于java中的静态方法
        '''
        dbparams = dict(
            host=crawler.settings['MYSQL_HOST'],  # 读取settings中的配置
            db=crawler.settings['MYSQL_DBNAME'],
            user=crawler.settings['MYSQL_USER'],
            passwd=crawler.settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False
        )
        # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        # 相当于dbpool付给了这个类，self中可以得到
        return cls(dbpool)

    def process_item(self, item, spider):
        if isinstance(item, TvItem):
            query = self.dbpool.runInteraction(self.do_insert_tv, item)
            query.addErrback(self.handle_error, item, spider)
        elif isinstance(item, RentItem):
            query = self.dbpool.runInteraction(self.do_insert_rent, item)
            query.addErrback(self.handle_error, item, spider)
        # if isinstance(item, FilmItem):
        #     # 调用插入的方法
        #     query = self.dbpool.runInteraction(self.do_insert_film, item)
        #     # 调用异常处理方法
        #     query.addErrback(self.handle_error, item, spider)
        # if isinstance(item, TvItem):
        #     query = self.dbpool.runInteraction(self.do_insert_tv, item)
        #     query.addErrback(self.handle_error, item, spider)
        return item

    def do_insert_tv(self, cursor, item):
        sql = '''insert into dw_video(op_time, id, name, isFeature, upTime, parts, updateTime, area, language, type, playTimes, score, director, actor, descri, isVip, comment, recommend, platform, classify) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'''
        params = (today, item['id'], item['name'], item['isFeature'], item['upTime'], item['parts'], item['updateTime'],
                  item['area'], item['language'], item['type_tag'],
                  item['playTimes'], item['score'], item['director'], item['actor'], item['describe'], item['isVip'],
                  item['comment'], item['recommend'], item['platform'], item['classify'])
        cursor.execute(sql, params)

    def do_insert_rent(self, cursor, item):
        sql = '''insert into rent(op_time, url, people, phone, price, size, way, nei_name, address, decoration, direction, area) 
              values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        params = (
        today, item['url'], item['people'], item['phone'], item['price'], item['size'], item['way'], item['nei_name'],
        item['address'], item['decoration'], item['direction'], item['area'])
        cursor.execute(sql, params)

    # 错误处理方法
    def handle_error(self, failue, item, spider):
        print(failue)
