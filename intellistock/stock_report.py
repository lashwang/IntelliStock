#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import time

import pandas as pd
import tushare as ts

import config as cf, http_cache as cache, mail
import logging
import file_utils

logger = logging.getLogger(__name__)

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
        file_utils.mkdir(cf.EXPORT_PATH_DIR)
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
        logging.debug(js)
        data = pd.DataFrame(js['data']['data'])
        totalPages = js['data']['totalPages']
        return {'totalPages':totalPages,'data':data}


    def _get_xinggu_data(self):
        pageIndex = 1
        totalPages = 0
        data = pd.DataFrame()
        while True:
            ret = self._get_xingu_list(pageIndex)
            if pageIndex == 1:
                totalPages = ret['totalPages']
                logging.debug(totalPages)
            data = data.append(ret['data'])
            if pageIndex >= totalPages:
                logging.debug('get all pages, page index:{}, total pages:{}'.format(pageIndex,totalPages))
                break
            else:
                pageIndex = pageIndex+1
                time.sleep(cf.REQUEST_DELAY)

        return data

    def _analyse_xingu_report(self):
        data = self._get_xinggu_data()

        return data


    def generate_xingu_report(self):
        data = self._analyse_xingu_report()

        data.to_excel(self.writer, sheet_name=u'次新股')
        self.writer.save()


        return os.path.abspath(cf.EXPORT_XLS_FILE_PATH)

    def run(self):
        export_xls_path = self.get_new_stock_report()
        f = [export_xls_path]
        self.send_mail(f)