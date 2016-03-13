# -*- coding: utf-8 -*-
import xlwt
import StringIO
from db.databases import Sqlite3DB
import re


class export_to_excel(object):
    def export(self, crawler, today):
        wb = xlwt.Workbook()
        wb.encoding = 'utf8'
        ws = wb.add_sheet('crawler company info')
        i = 0
        for head in heads[crawler]:
            ws.write(0, i, head)
            i += 1

        sql = sqls[crawler]
        infos = Sqlite3DB().find_today_company_info(sql, crawler, today)
        count = len(infos)
        print count
        for i in xrange(1, count + 1):
            j = 0
            for value in infos[i - 1]:
                value = value.strip()
                if j == 3:
                    trades = value.split(',')
                    if trades[0]:
                        ws.write(i, 3, trades[0])
                    if len(trades) > 1:
                        ws.write(i, 4, trades[1])
                    j += 2
                elif j == 7:
                    teams = re.split('\\s+', value)
                    if len(teams) > 1:
                        ws.write(i, 7, teams[0])
                        ws.write(i, 8, teams[1])
                        ws.write(i, 9, "".join(teams[2:]))
                    else:
                        ws.write(i, 7, "")
                        ws.write(i, 8, "")
                        ws.write(i, 9, "")
                    j += 3
                else:
                    ws.write(i, j, value)
                    j += 1

        sio = StringIO.StringIO()
        wb.save(sio)
        return sio.getvalue()


heads = {'lagou': [
    u'公司名称', u'产品名称', u'项目简介', u'行业1', u'行业2', u'爬取的URL', u'阶段和投资信息', u'管理团队1', u'职位1', u'管理团队',
    u'所在地', u'公司网址', u'扩展信息'
]}

sqls = {'lagou':
            'select company_name,product_name,introduction,trade,crawler_url,stage,management_team,location,company_url,ext_info'
            ' from company_crawler where crawler_spider="%s" and date(create_time)="%s"'
        }

if __name__ == '__main__':
    export_to_excel().export('lagou', '2016-03-13')
