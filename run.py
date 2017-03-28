#!/usr/bin/python
# -*- coding: utf-8 -*-


import fire
import tushare as ts
import pandas as pd
import mail as mail
import configuration as cf
import os
import json
import lxml.html
from lxml import etree
import time
import httpCache as cache

class StockReport(object):

    def _read_basic_stock_from_file(self):
        df = pd.read_csv('data/all.csv', dtype={'code':'object'})
        df.set_index('code')
        return df

    def _read_baisc_stock_from_network(self):
        df = ts.get_stock_basics()
        return df
        
    def _get_time_str(self,time):
        time = str(time)
        timeToMarket = time[0:4] + '-' + time[4:6] + '-' + time[6:8]
        return timeToMarket


    def _get_basic_stock_list(self):
        df = self._read_basic_stock_from_file()
        self.new_stock_list = df.filter(items=['code','outstanding','totals','timeToMarket'])


    def __init__(self):
        try:
            os.mkdir(cf.EXPORT_PATH_DIR)
        except Exception, error:
            print str(error)

        self.writer = pd.ExcelWriter(cf.EXPORT_XLS_FILE_PATH, engine='xlsxwriter')
        self.cache_engine = cache.HttpCache()

    def send_mail(self,files=None):
        mail_ = mail.Mail()
        mail_.send_email(files)


    def _get_xingu_url(self,_page = 1,_page_size = cf.QQ_XINGU_DEFAULT_PAGE_SIZE):
        return cf.QQ_XINGU_URL.format(_page,_page_size)

    def _get_xingu_list(self,_page = 1):
        url = self._get_xingu_url(_page)
        lines = self.cache_engine.Request(url)
        if len(lines) < 100:  # no data
            return None
        lines = lines.split('=')[1]
        js = json.loads(lines)
        print js
        data = pd.DataFrame(js['data']['data'])
        totalPages = js['data']['totalPages']
        return {'totalPages':totalPages,'data':data}



    def get_new_stock_report(self):
        pageIndex = 1
        totalPages = 0
        data = pd.DataFrame()
        while True:
            ret = self._get_xingu_list(pageIndex)
            if pageIndex == 1:
                totalPages = ret['totalPages']
                print totalPages
            data = data.append(ret['data'])
            if pageIndex >= totalPages:
                print 'get all pages, page index:{}, total pages:{}'.format(pageIndex,totalPages)
                break
            else:
                pageIndex = pageIndex+1
                time.sleep(cf.REQUEST_DELAY)

        data.to_excel(self.writer, sheet_name=u'次新股')
        self.writer.save()




        # # 未上市新股
        # self.stokc_untrade = self.new_stock_list[self.new_stock_list.timeToMarket == 0]
        # self.stokc_untrade.to_excel(self.writer, sheet_name=u'未上市新股',encoding='GBK')
        #
        # # 筛选最近一年上市的新股
        # df = self.new_stock_list[self.new_stock_list.timeToMarket > 20160801]
        # df.to_excel(self.writer, sheet_name=u'次新股',encoding='GBK')
        #
        # for index, row in df.iterrows():
        #     code = row.code
        #     timeToMarket = self._get_time_str(row.timeToMarket)
        #     df = ts.get_k_data(code)
        #     df.to_excel(self.writer, sheet_name=code,encoding='GBK')
        #     break
        #
        # self.writer.save()

        return os.path.abspath(cf.EXPORT_XLS_FILE_PATH)

    def run(self):
        export_xls_path = self.get_new_stock_report()
        f = [export_xls_path]
        self.send_mail(f)

def main():
    fire.Fire(StockReport)


if __name__ == "__main__":
    main()