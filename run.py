# -*- coding: utf-8 -*-
__author__ = 'yanshi'

from spiders.Spiders import Lagou
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


process = CrawlerProcess(get_project_settings())

process.crawl(Lagou)
process.start()  # the script will block here until the crawling is finished
