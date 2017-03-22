#!/usr/bin/python
# -*- coding: utf-8 -*-


import fire
import tushare as ts
import pandas as pd


class StockReport(object):

    global writer
    global new_stock_list

    def read_baisc_stock_from_file(self):
        df = pd.read_csv('data/all.csv', dtype={'code':'object'})
        df.set_index('code')
        return df

    def __init__(self):
        writer = pd.ExcelWriter('stock.xlsx', engine='xlsxwriter')
        df = self.read_baisc_stock_from_file()
        




    def get_new_stock_report(self):
        print "loading..."


def main():
    fire.Fire(StockReport)


if __name__ == "__main__":
    main()