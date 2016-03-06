from scrapy import signals
from db.databases import Sqlite3DB


class SpiderOpenCloseLogging(object):
    def __init__(self):
        self.sqlite3 = Sqlite3DB()

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_opened(self, spider):
        print  spider.name
        self.sqlite3.create_crawler_task(spider.name)

    def spider_closed(self, spider):
        print  spider.name
        self.sqlite3.update_task_state(spider.name)
