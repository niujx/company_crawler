# -*- coding: utf-8 -*-
import xlwt
import StringIO


class export_to_excel(object):
    def export(self, crawler):
        wb = xlwt.Workbook()
        wb.encoding = 'utf8'
        ws = wb.add_sheet('crawler company info')
        i = 0
        for head in heads[crawler]:
            ws.write(0, i, head)
            i += 1

        sio = StringIO.StringIO()
        wb.save(sio)
        return sio.getvalue()


heads = {'lagou': [
    u'公司名称', u'公司名称', u'行业', u'所在地', u'阶段和投资信息', u'管理团队', u'项目简介', u'公司网址', u'扩展信息'
]}

if __name__ == '__main__':
    export_to_excel().export('lagou')
