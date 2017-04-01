#!/usr/bin/python
# -*- coding: utf-8 -*-

from http_cache import HttpCache
import json
import os
import time
import logging
import config as cf
import pandas as pd
import tushare as ts
from StringIO import StringIO
from database import DataBase
import dataset

logger = logging.getLogger(__name__)




class DataWrapper:

    CACHE_TIMEOUT_TABLE = {
        'trade_check':10
    }

    STOCK_CALENDER_TABLE = "stock_calender"


    def __init__(self):
        self.cache_engine = HttpCache()

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


    def check_is_trading(self):
        url = cf.CHECK_IF_TRADING_URL
        timeout = DataWrapper.CACHE_TIMEOUT_TABLE['trade_check']
        data = self.cache_engine.Request(url,True,timeout)

        logger.debug(str(data))
        logger.debug(data)

        data = data.split('=')[1]
        data = data.split('"')[1]
        data = data.split('|')[2]
        data = data.split('_')[1]

        if data == 'close':
            logger.debug('trade closed')
            return False

        if data == 'open':
            logger.debug('trade opening')
            return True

        return False

    def get_all_trade_cal(self):
        data = self.cache_engine.Request('http://218.244.146.57/static/calAll.csv')
        df = pd.read_csv(StringIO(data))

        all_opened_cal = df.loc[df['isOpen'] == 1]
        cal = all_opened_cal['calendarDate'].tolist()

        logger.debug(cal)

        db = DataBase.get_db_connection()
        with db:
            table = db[DataWrapper.STOCK_CALENDER_TABLE]
            for date in cal:
                table.upsert(dict(cal=date),['cal'])











