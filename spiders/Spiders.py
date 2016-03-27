# -*- coding: utf-8 -*-
import json

import scrapy
# 拉勾网的爬虫
from scrapy.loader import ItemLoader
from items import LagouItem
import os
import re
from db.databases import Sqlite3DB
from scrapy import Selector
from selenium import webdriver
import time


def findCompanyId(url):
    match = re.match(r'.*?(\d+).*', url)
    if match:
        return match.group(1)


# 1 初创型
# 2 成长型
# 3 成熟型
# 4 已上市
# 1 2 3 4  状态
# 24 25 33 27 29 45 31 28 47 行业了 领域
# 2 3 214 212 6 251 79 184 297 129 197 80 4 5 167 149 111 128 148 43 215 84 217 229 98 87 44 8 281 7 234 57 248 230 223 272 70 19 101 156 81 153 314 132

class Lagou(scrapy.Spider):
    name = "lagou"
    allowed_domains = ['www.lagou.com']
    start_urls = [
    ]
    sqlite3 = Sqlite3DB()
    citys = [2, 3, 214, 212, 6, 251, 79, 184, 297, 129, 197, 80, 4, 5, 167, 149, 111, 128, 148, 43, 215, 84, 217, 229,
             98, 87, 44, 8, 281, 7, 234, 57, 248, 230, 223, 272, 70, 19, 101, 156, 81, 153, 314, 132]
    types = [1, 2, 3, 4]
    channels = [24, 25, 33, 27, 29, 45, 31, 28, 47]
    cookies = {}

    def start_requests(self):
        browser = webdriver.Firefox()
        browser.get('http://www.lagou.com/')
        time.sleep(10)
        print 'start cookie'
        browser.close()
        self.cookies = browser.get_cookies()
        for city in self.citys:
            for type in self.types:
                for channel in self.channels:
                    filename = str(city) + '-' + str(type) + '-' + str(channel)
                    print filename
                    for i in xrange(1, 21):
                        url = 'http://www.lagou.com/gongsi/' + filename + '.json?first=false&havemark=0&pn=' + str(
                            i) + '&sortField=0'
                        yield scrapy.Request(url=url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        try:
            datas = json.loads(response.body, encoding='utf-8')
            for info in datas['result']:
                company_id = info['companyId']
                if self.sqlite3.exists('lagou', company_id):
                    continue
                company_detail = 'http://www.lagou.com/gongsi/' + str(company_id) + '.html'
                yield scrapy.Request(company_detail, cookies=self.cookies, callback=self.parse_detail)
        except:
            print 'error', response.url
            print  response.body

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
# https://rong.36kr.com/api/company?city=101&fincephase=ANGEL&fincestatus=1&industry=E_COMMERCE&page=2&type=2

kr_city = [101, 109, 21903, 21901, 21101, 22301, 102, 122, 112, 134, 113, 128, 119, 120, 124, 121, 103, 116, 108, 117,
           118, 107, 110, 114, 106,
           105, 130, 129, 115, 104, 127, 123, 126, 133, 131, 125, 111]
kr_fincephase = ['CONSUMER_LIFESTYLE', 'E_COMMERCE', 'SOCIAL_NETWORK', 'INTELLIGENT_HARDWARE', 'MEDIA', 'SOFTWARE',
                 'FINANCE', 'MEDICAL_HEALTH', 'SERVICE_INDUSTRIES'
    , 'TRAVEL_OUTDOORS', 'PROPERTY_AND_HOME_FURNISHINGS', 'CULTURE_SPORTS_ART', 'EDUCATION_TRAINING', 'AUTO', 'OTHER',
                 'LOGISTICS']

kr_a_b_c = ['ANGEL', 'PRE_A', 'A', 'A_PLUS', 'B', 'B_PLUS', 'C', 'D', 'E', 'IPO']


class N36kr(scrapy.Spider):
    name = '36kr'
    allowed_domains = ['36kr.com']
    start_urls = []
    introductions = ['competitor', 'dataLights', 'projectAdvantage', 'projectPlan', 'scale']
    addresses = ['address1', 'address2', 'address3']
    companys = ['intro', 'story']
    city_dict = {}
    a_b_c_dict = {}
    sqlite3 = Sqlite3DB()
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
        self._a_b_c_dict()
        browser = webdriver.Firefox()
        browser.get('http://36kr.com/')
        browser.find_element_by_link_text('登录/注册').click()
        time.sleep(3)
        browser.find_element_by_name('username').send_keys('qianglin@k2vc.com')
        browser.find_element_by_name('password').send_keys('0322zhang')
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/form/button').click()
        time.sleep(30)
        cookies = browser.get_cookies()
        print 'start cookie'
        browser.close()

        # https://rong.36kr.com/api/company?city=101&fincestatus=1&page=2&type=2
        for city in kr_city:
            for i in xrange(1, 6):
                yield scrapy.Request(
                    url='https://rong.36kr.com/api/company?city=' + str(city) + '&fincestatus=1&page=' + str(
                        i) + '&type=2',
                    cookies=cookies, callback=self.parse)

    def parse(self, response):
        if not response.status == 200:
            return
        datas = json.loads(response.body, encoding='utf-8')
        for all_info in datas['data']['page']['data']:
            company = all_info['company']
            financing = all_info['financing']
            founder = all_info['founder']
            if self.sqlite3.exists('36kr', str(company['id'])):
                continue

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
                try:
                    city_info = self.city_dict[int(info[key])]
                    result.append(city_info['name'])
                except:
                    print 'error', info

        return "|".join(result) if len(result) > 0 else ''

    def _load_city_dict(self):
        with open(os.environ['PYTHONPATH'] + '/resource/36kr_city.json', 'r') as f:
            city_data = json.load(f, encoding='utf8')
        for city in city_data:
            self.city_dict[city['id']] = city

    def _a_b_c_dict(self):
        with open(os.environ['PYTHONPATH'] + '/resource/a_b_c.json', 'r') as f:
            a_b_c_data = json.load(f, encoding='utf8')

        for abc in a_b_c_data:
            self.a_b_c_dict[abc['value']] = abc['desc']


class ITjuzi(scrapy.Spider):
    name = 'itjuzi'
    start_urls = []
    allowed_domains = ['itjuzi.com']
    sqlite3 = Sqlite3DB()
    heades = {'Referer': 'http://itjuzi.com/company?sortby=foundtime',
              'Origin': 'http://itjuzi.com',
              'Connection': 'keep-alive',
              'Accept-Encoding': 'gzip, deflate, br',
              'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}

    cookies = {}

    def start_requests(self):
        browser = webdriver.Firefox()
        browser.get('https://www.itjuzi.com/')
        browser.find_element_by_link_text('登录').click()
        time.sleep(3)
        browser.find_element_by_id('create_account_email').send_keys('279806846@qq.com')
        browser.find_element_by_id('create_account_password').send_keys('0322zhang')
        browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div/div[2]/div/form/div[3]/button').click()
        time.sleep(30)
        print 'start cookie'
        browser.close()
        self.cookies = browser.get_cookies()
        yield scrapy.Request("http://itjuzi.com/company?sortby=foundtime&page=1", cookies=self.cookies,
                             headers=self.heades,
                             callback=self._request_generator)

    def _request_generator(self, response):
        count = Selector(text=response.body).xpath(
            '//div[@class="ui-pagechange for-sec-bottom"]/a[8]/@data-ci-pagination-page').extract()
        count = int(count[0])
        print count
        for i in xrange(1, count):
            url = 'http://itjuzi.com/company?sortby=foundtime&page=' + str(i)
            yield scrapy.Request(url=url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):

        urls = Selector(text=response.body).xpath('//i[@class="cell pic"]/a/@href').extract()
        for url in urls:
            if self.sqlite3.exists('itjuzi', findCompanyId(response.url)):
                continue
            yield scrapy.Request(url=url, cookies=self.cookies, callback=self.pasreContext)

    def pasreContext(self, response):
        if not response.status == 200:
            return
        # html body div.brand-wrap h3.no-data span.sub-title
        itjuzi_loader = ItemLoader(item=LagouItem(), response=response)
        itjuzi_loader.add_value('company_id', findCompanyId(response.url))
        itjuzi_loader.add_xpath('company_name', '//div[@class="des-more"]/div/span/text()')
        itjuzi_loader.add_xpath('product_name', '//div[@class="rowhead"]//b/text()')
        itjuzi_loader.add_xpath('trade', '//div[@class="tagset dbi c-gray-aset"]/a/span/text()')
        itjuzi_loader.add_xpath('location', '//span[@class="loca c-gray-aset"]//text()')
        itjuzi_loader.add_xpath('stage', '//span[@class="round"]/a/text()')
        itjuzi_loader.add_xpath('management_team', '//ul[@class="list-prodcase limited-itemnum"]//p/text()')
        itjuzi_loader.add_xpath('introduction', '//div[@class="des"]/text()')
        itjuzi_loader.add_xpath('company_url', '//a[@class="weblink"]/@href')
        itjuzi_loader.add_xpath('ext_info', '//div[@class="block block-v"]/span/text()')
        itjuzi_loader.add_value('crawler_url', response.url)
        itjuzi_loader.add_value('crawler_spider', 'itjuzi')
        return itjuzi_loader.load_item()
