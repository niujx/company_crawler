# -*- coding: utf-8 -*-
import sqlite3

class Sqlite3ItemPipline(object):
    db = sqlite3.connect('db/crawler_db')

    def __int__(self):
        pass

    def process_item(self,item,spider):
        pass




