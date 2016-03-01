# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class Sqlite3DBItemPipline(object):
    def __int__(self):
        pass

    def process_item(self, item, spider):
        for k, v in item.iteritems():
            print "dict[%s]=" % k, v
