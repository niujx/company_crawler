# -*- coding: utf-8 -*-
import scrapy


class LagouItem(scrapy.Item):
    company_name = scrapy.Field()
    product_name = scrapy.Field()
    trade = scrapy.Field()
    location = scrapy.Field()
    info = scrapy.Field()
    management_team = scrapy.Field()
    introduction = scrapy.Field()
    company_url = scrapy.Field()
    ext_info = scrapy.Field()