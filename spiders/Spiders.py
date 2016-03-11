# -*- coding: utf-8 -*-
import json

import scrapy
# 拉勾网的爬虫
from scrapy.loader import ItemLoader
from items import LagouItem
import settings
import re
from db.databases import Sqlite3DB
from selenium import webdriver
import time


def findCompanyId(url):
    match = re.match(r'.*?(\d+).html', url)
    if match:
        return match.group(1)


class Lagou(scrapy.Spider):
    name = "lagou"
    allowed_domains = ['www.lagou.com']
    start_urls = [
    ]
    sqlite3 = Sqlite3DB()

    def start_requests(self):
        # self.sqlite3.create_crawler_task('lagou')
        for i in xrange(1, 21):
            url = 'http://www.lagou.com/gongsi/2-0-0.json?first=false&havemark=0&pn=' + str(i) + '&sortField=0'
            yield self.make_requests_from_url(url)

    def parse(self, response):
        datas = json.loads(response.body, encoding='utf-8')
        for info in datas['result']:
            company_id = info['companyId']
            if self.sqlite3.exists('lagou', company_id):
                continue
            company_detail = 'http://www.lagou.com/gongsi/' + str(company_id) + '.html'
            yield scrapy.Request(company_detail, callback=self.parse_detail)

    @staticmethod
    def parse_detail(response):
        if not response.status == 200:
            return

        lagou_loader = ItemLoader(item=LagouItem(), response=response)
        lagou_loader.add_value('company_id', findCompanyId(response.url))
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
        lagou_loader.add_value('crawler_spider', 'lagou')
        return lagou_loader.load_item()


class N36kr(scrapy.Spider):
    name = '36kr'
    allowed_domains = ['36kr.com']
    start_urls = []
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'passport.36kr.com'
    }

    def start_requests(self):
        browser = webdriver.Firefox()
        browser.get('http://36kr.com/')
        browser.find_element_by_link_text('登录/注册').click()
        browser.find_element_by_name('username').send_keys('qianglin@k2vc.com')
        browser.find_element_by_name('password').send_keys('0322zhang')
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/form/button').click()
        time.sleep(30)
        print 'start cookie'
        browser.close()
        for i in xrange(1, 21):
            yield scrapy.Request(url='https://rong.36kr.com/api/company?fincestatus=1&page='+str(i)+'&type=0',
                                 cookies=browser.get_cookies(), callback=self.parse)

    def parse(self, response):
        datas = json.loads(response.body, encoding='utf-8')
        print datas['data']['page']['page']
