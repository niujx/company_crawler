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
        for i in xrange(1, 2):
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

        lagou_loader = ItemLoader(item=LagouItem(), response=response)
        lagou_loader.add_xpath('company_name', '//div[@class="company_main"]/h1/a/@title')
        lagou_loader.add_xpath('product_name', '//div[@id="company_products"]/div[@class="item_content"]//text()')
        lagou_loader.add_xpath('trade', '//div[@class="item_content"]/ul/li[1]/span/text()')
        lagou_loader.add_xpath('location', '//div[@class="item_content"]/ul/li[4]/span/text()')
        lagou_loader.add_xpath('stage', '//div[@class="item_content"]/ul/li[2]/span/text()')
        lagou_loader.add_xpath('management_team', '//ul[@class="manager_list"]/li//text()')
        lagou_loader.add_xpath('introduction', '//span[@class="company_content"]//text()')
        lagou_loader.add_xpath('company_url', '//div[@class="company_main"]/h1/a/@href')
        lagou_loader.add_xpath('ext_info', '//div[@id="history_container"]/div[@class="item_content"]//text()')
        lagou_loader.add_value('crawler_url', response.url)
        return lagou_loader.load_item()
