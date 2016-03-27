# -*- coding: utf-8 -*-
__author__ = 'yanshi'

from spiders.Spiders import Lagou,N36kr,ITjuzi
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def start_crawler():
    print 'start crawler'
    process = CrawlerProcess(get_project_settings())
    process.crawl(Lagou)
    process.crawl(N36kr)
    process.crawl(ITjuzi)

    process.start()
if __name__ == '__main__':
    start_crawler()
