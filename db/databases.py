import sqlite3
from collections import defaultdict
from datetime import date
import os


class Sqlite3DB(object):
    path = os.environ['PYTHONPATH'] + '/resource/company_crawler.db'
    connection = None

    def __init__(self):
        self.connection = sqlite3.connect(self.path)

    def save_company_info(self, dict):
        sql = "insert into company_crawler (company_id,company_name,product_name,trade,location," \
              "stage,management_team,introduction,company_url,ext_info,crawler_url,create_time,crawler_spider)" \
              "values (:company_id,:company_name,:product_name,:trade,:location,:stage,:management_team," \
              ":introduction,:company_url,:ext_info,:crawler_url,DATETIME('NOW'),:crawler_spider)"

        cursor = self.connection.cursor()
        cursor.execute(sql, defaultdict(str, dict))
        self.connection.commit()
        cursor.close()

    def exists(self, crawler_spider, company_id):
        sql = "select id from company_crawler where crawler_spider='%s' and company_id='%s'" % (
            crawler_spider, company_id)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        exists = len(cursor.fetchall()) > 0
        cursor.close()
        return exists

    def create_crawler_task(self, crawler_spider):
        sql = "insert into crawler_task (crawler_spider,create_time,state) " \
              "values ('%s',DATETIME('NOW'),'1')" % (crawler_spider)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def update_task_state(self, crawler_spider):
        sql = "update crawler_task set state= '2' where crawler_spider='%s' and date(create_time) ='%s'" % (
            crawler_spider, str(date.today()))
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def find_today_company_info(self, sql, crawler_spider, today):
        cursor = self.connection.cursor()
        sql = sql % (crawler_spider, today)
        cursor.execute(sql)
        infos = cursor.fetchall()
        cursor.close()
        return infos

    def find_task_by_limit(self, limit):
        sql = "select id,crawler_spider,date(create_time) as today ,state from crawler_task order by id desc limit %s,%s" % (limit, 20)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        tasks = []
        for record in cursor.fetchall():
            task = dict()
            task['id'] = record[0]
            task['crawler_spider'] = record[1]
            task['today'] = record[2]
            task['state'] = record[3]
            tasks.append(task)
        cursor.close()
        return tasks
