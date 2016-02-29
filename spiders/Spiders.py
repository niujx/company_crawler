# -*- coding: utf-8 -*-
import json

import scrapy
# 拉勾网的爬虫
from scrapy.loader import ItemLoader

from items import LagouItem


class Lagou(scrapy.Spider):
    name = "lagou"
    allowed_domains = ['www.lagou.com']
    start_urls = [
    ]

    def start_requests(self):
        for i in xrange(1, 20):
            url = 'http://www.lagou.com/gongsi/2-0-0.json?first=false&havemark=0&pn=' + str(i) + '&sortField=0'
            yield self.make_requests_from_url(url)

    def parse(self, response):
        datas = json.loads(response.body, encoding='utf-8')
        for info in datas['result']:
            company_id = info['companyId']
            company_detail = 'http://www.lagou.com/gongsi/' + str(company_id) + '.html'
            yield scrapy.Request(company_detail, callback=self.parse_detail)

    @staticmethod
    def parse_detail(response):
        if not response.status == 200:
            return

        lagou_pipline = ItemLoader(item=LagouItem(), response=response)
        lagou_pipline.add_xpath('company_name', '/html/body/div[3]/div/div/div[1]/h1/a')
        return lagou_pipline.load_item()
