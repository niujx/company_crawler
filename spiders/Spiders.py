# -*- coding: utf-8 -*-
import json

import scrapy
# 拉勾网的爬虫
from scrapy.loader import ItemLoader
from items import LagouItem
import os
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


industry_mapping = {
    'CONSUMER_LIFESTYLE': u'消费生活',
    'E_COMMERCE': u'电子商务',
    'SOCIAL_NETWORK': u'社交网络',
    'INTELLIGENT_HARDWARE': u'智能硬件',
    'MEDIA': u'媒体门户',
    'SOFTWARE': u'工具软件',
    'FINANCE': u'金融',
    'MEDICAL_HEALTH': u'医疗健康',
    'SERVICE_INDUSTRIES': u'企业服务',
    'TRAVEL_OUTDOORS': u'旅游户外',
    'PROPERTY_AND_HOME_FURNISHINGS': u'房产家居',
    'CULTURE_SPORTS_ART': u'数字娱乐',
    'EDUCATION_TRAINING': u'在线教育',
    'AUTO': u'汽车交通 ',
    'OTHER': u' 其他 ',
    'LOGISTICS': u'物流',
}

class N36kr(scrapy.Spider):
    name = '36kr'
    allowed_domains = ['36kr.com']
    start_urls = []
    introductions = ['competitor', 'dataLights', 'projectAdvantage', 'projectPlan', 'scale']
    addresses = ['address1', 'address2', 'address3']
    companys = ['intro', 'story']
    city_dict = {}
    a_b_c_dict = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'passport.36kr.com'
    }

    def start_requests(self):
        self._load_city_dict()
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
            yield scrapy.Request(url='https://rong.36kr.com/api/company?fincestatus=1&page=' + str(i) + '&type=0',
                                 cookies=browser.get_cookies(), callback=self.parse)

    def parse(self, response):
        if not response.status == 200:
            return
        datas = json.loads(response.body, encoding='utf-8')
        for all_info in datas['data']['page']['data']:
            company = all_info['company']
            financing = all_info['financing']
            founder = all_info['founder']
            kr36_loader = ItemLoader(item=LagouItem(), response=response)
            kr36_loader.add_value('company_id', str(company['id']))
            kr36_loader.add_value('company_name', company['fullName'])
            kr36_loader.add_value('product_name', company['name'])
            kr36_loader.add_value('trade', industry_mapping[company['industry']])
            kr36_loader.add_value('location', self._get_address_test(self.addresses, company))
            kr36_loader.add_value('stage', self.a_b_c_dict[financing['phase']])
            kr36_loader.add_value('management_team', "".join([str(f['name']).strip() for f in founder if f['name']]))
            kr36_loader.add_value('introduction', self._get_text(self.companys, company))
            if company.has_key('website'):
                kr36_loader.add_value('company_url', company['website'])
            kr36_loader.add_value('ext_info', self._get_text(self.introductions, financing))
            kr36_loader.add_value('crawler_url', 'https://rong.36kr.com/company/%s/overview' % company['id'])
            kr36_loader.add_value('crawler_spider', '36kr')
            yield kr36_loader.load_item()

    def _get_text(self, keys, info):
        result = []
        for key in keys:
            if info.has_key(key):
                result.append(str(info[key]))
        return "|".join(result) if len(result) > 0 else ''

    def _get_address_test(self, keys, info):
        result = []
        for key in keys:
            if info.has_key(key):
                city_info = self.city_dict[info[key]]
                result.append(city_info['name'])
        return "|".join(result) if len(result) > 0 else ''

    def _load_city_dict(self):
        with open(os.environ['PYTHONPATH'] + '/resource/36kr_city.json', 'r') as f:
            city_data = json.load(f, encoding='utf8')
        for city in city_data:
            self.city_dict[city['id']] = city

    def _a_b_c_dict(self):
        with open(os.environ['PYTHONPATH'] + '/resource/a_b_c.json','r') as f:
            a_b_c_data  = json.load(f,encoding='utf8')

        for abc in a_b_c_data:
            self.a_b_c_dict[abc['value']] = abc['desc']



