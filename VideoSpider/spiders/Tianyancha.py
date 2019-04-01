# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy import FormRequest
from urllib.request import urlretrieve
import re
import xml.etree.ElementTree as ET
import time


class TianyanchaSpider(scrapy.Spider):
    name = 'Tianyancha'
    allowed_domains = ['www.tianyancha.com']
    start_urls = ['https://www.tianyancha.com/robots.txt']

    def login(self, response):

        scrapy.FormRequest.from_response(
            response=response,
            formdata={'username': 'john', 'password': 'secret'},
            callback=self.after_login
        )

    def get_file(self):
        robots_path = self.crawler.settings.get('ROBOTS_PATH')
        file_path = self.crawler.settings.get('FILE_PATH')
        xml_path = self.crawler.settings.get('XML_PATH')
        urlretrieve(self.start_urls[0], robots_path)
        with open(robots_path) as fp:
            txt = fp.read()
        sitemap = re.search('https://[\s\S]*every_www.xml', txt)
        if sitemap:
            sitemap_url = sitemap.group()
            urlretrieve(sitemap_url, xml_path)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        file_list = []
        urls = []
        for every in root:
            tmp = every[0].text
            urls.append(tmp)
            name = file_path + tmp[tmp.rindex('/') + 1: len(tmp)]
            file_list.append(name)
        if len(file_list) > 3:
            for url, file in zip(urls, file_list):
                urlretrieve(url, file)
                time.sleep(10)
            return file_list
        else:
            self.get_file()
        return

    def start_requests(self):
        base_url = 'https://www.tianyancha.com/company/3300469281'
        for i in range(0, 11111):
            yield Request(url=base_url, callback=self.parse, dont_filter=True)
        # file_list = self.get_file()
        # for file in file_list:
        #     tree = ET.parse(file)
        #     root = tree.getroot()
        #     for every in root:
        #         url = every[0].text
        #         yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            print(response.css('.-striped-col tr')[2].css('td')[1].extract())
        except Exception as e:
            print(response.text)