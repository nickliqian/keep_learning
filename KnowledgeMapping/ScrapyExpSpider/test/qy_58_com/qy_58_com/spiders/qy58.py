# -*- coding: utf-8 -*-
import scrapy


class Qy58Spider(scrapy.Spider):
    name = 'qy58'
    allowed_domains = ['qy.58.com']
    start_urls = ['http://qy.58.com/']

    def parse(self, response):
        pass
