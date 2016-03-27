# -*- coding: utf-8 -*-
__author__ = 'yanshi'

from spiders.Spiders import Lagou,N36kr,ITjuzi
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(ITjuzi)
    process.start()


