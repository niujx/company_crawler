# -*- coding: utf-8 -*-
import sys
from db.databases import Sqlite3DB

reload(sys)
sys.setdefaultencoding("utf-8")


class Sqlite3DBItemPipline(object):
    sqlite3 = Sqlite3DB()
    def process_item(self, item, spider):
        self.sqlite3.save_company_info(item);