#!/usr/bin/python
# -*- coding: utf-8 -*-


import fire
import tushare as ts
import pandas as pd
import mail as mail
import configuration as cf
import os


class StockReport(object):

    def _read_baisc_stock_from_file(self):
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


    def __init__(self):
        try:
            os.mkdir(cf.EXPORT_PATH_DIR)
        except Exception, error:
            print str(error)

        self.writer = pd.ExcelWriter(cf.EXPORT_XLS_FILE_PATH, engine='xlsxwriter')
        df = self._read_baisc_stock_from_file()
        self.new_stock_list = df.filter(items=['code','outstanding','totals','timeToMarket'])




    def send_mail(self,files=None):
        mail_ = mail.Mail()
        mail_.send_email(files)



    def get_new_stock_report(self):
        # 未上市新股
        self.stokc_untrade = self.new_stock_list[self.new_stock_list.timeToMarket == 0]
        self.stokc_untrade.to_excel(self.writer, sheet_name=u'未上市新股',encoding='GBK')

        # 筛选最近一年上市的新股
        df = self.new_stock_list[self.new_stock_list.timeToMarket > 20160801]
        df.to_excel(self.writer, sheet_name=u'次新股',encoding='GBK')

        for index, row in df.iterrows():
            code = row.code
            timeToMarket = self._get_time_str(row.timeToMarket)
            df = ts.get_k_data(code)
            df.to_excel(self.writer, sheet_name=code,encoding='GBK')
            break

        self.writer.save()

        return os.path.abspath(cf.EXPORT_XLS_FILE_PATH)

    def run(self):
        export_xls = self.get_new_stock_report()
        f = [export_xls]
        self.send_mail(f)

def main():
    fire.Fire(StockReport)


if __name__ == "__main__":
    main()