#!/usr/bin/python
# -*- coding: utf-8 -*-


import fire
import tushare as ts
import pandas as pd


class StockReport(object):
    def get_new_stock_report(self):
        print "loading..."
        df = ts.get_stock_basics()
        writer = pd.ExcelWriter('stock.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        print "done"

def main():
    fire.Fire(StockReport)


if __name__ == "__main__":
    main()