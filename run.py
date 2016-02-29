# -*- coding: utf-8 -*-
__author__ = 'yanshi'

from spiders.Spiders import Lagou
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Lagou)
process.start()  # the script will block here until the crawling is finished
