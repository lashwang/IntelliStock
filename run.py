#!/usr/bin/python
# -*- coding: utf-8 -*-


import fire
import tushare as ts
import pandas as pd


class StockReport(object):

    def read_baisc_stock_from_file(self):
        df = pd.read_csv('data/all.csv', dtype={'code':'object'})
        df.set_index('code')
        return df

    def read_baisc_stock_from_file(self):
        df = ts.get_stock_basics()
        


    def __init__(self):
        self.writer = pd.ExcelWriter('stock.xlsx', engine='xlsxwriter')
        df = self.read_baisc_stock_from_file()
        self.new_stock_list = df.filter(items=['code','outstanding','totals','timeToMarket'])
        self.new_stock_list.set_index('code')





    def get_new_stock_report(self):
        self.new_stock_list.to_excel(self.writer, sheet_name='Sheet1')
        self.writer.save()

def main():
    fire.Fire(StockReport)


if __name__ == "__main__":
    main()