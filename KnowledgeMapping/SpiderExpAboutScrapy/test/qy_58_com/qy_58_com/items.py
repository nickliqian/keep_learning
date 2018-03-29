# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Qy58ComItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    reg_number = scrapy.Field()
    contact_person = scrapy.Field()
    company_person = scrapy.Field()
    contact_phone = scrapy.Field()
    company_type = scrapy.Field()
    company_site = scrapy.Field()
    company_scale = scrapy.Field()
    company_address = scrapy.Field()
    company_business = scrapy.Field()
