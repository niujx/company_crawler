import sqlite3
from collections import defaultdict
from datetime import date

class Sqlite3DB(object):
    connection = sqlite3.connect('../resource/company_crawler.db')

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

    def create_crawler_test(self, crawler_spider):
        sql = "insert into crawler_task (crawler_spider,create_time,state) " \
              "values ('%s',DATETIME('NOW'),'1')" % (crawler_spider)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def update_task_state(self, crawler_spider):
        sql = "update crawler_task set state= '2' where crawler_spider='%s' and date(create_time) ='%s'" % (crawler_spider,str(date.today()))
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()


if __name__ == "__main__":
    print Sqlite3DB().update_task_state('lagou')
    print date.today()
