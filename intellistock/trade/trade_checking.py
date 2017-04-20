#!/usr/bin/python
# -*- coding: utf-8 -*-

from intellistock.http_cache import HttpCache
import logging
import pandas as pd
from StringIO import StringIO
import os
import arrow
import ast
from intellistock.trade import SpiderBase, run


logger = logging.getLogger(__name__)


class StockCalDay(SpiderBase):
    name = __name__
    CAL_DAY_URL = 'http://vaserviece.10jqka.com.cn/mobilecfxf/data/json_{year}.txt'

    def __init__(self,cal):
        self._cal = arrow.get(cal, 'YYYY-MM-DD')
        super(StockCalDay, self).__init__()

    def _get_start_url(self):
        url = StockCalDay.CAL_DAY_URL.format(year=self._cal.year)
        return url


    def _on_response(self,data):
        self._cal_list = ast.literal_eval(data)
        self._trade_day = self._check_trading_day()

    def _check_trading_day(self):
        date_str = self._cal.format('MMDD')

        if date_str in self._cal_list:
            return True

        return False

    @run
    def is_trading_day(self):
        return self._trade_day




class StockTradeTime(SpiderBase):
    name = __name__
    CHECK_IF_TRADING_URL = 'http://appqt.gtimg.cn/utf8/q=marketStat'

    def __init__(self):
        super(StockTradeTime,self).__init__()

    def _get_start_url(self):
        return StockTradeTime.CHECK_IF_TRADING_URL

    def _on_response(self, data):
        data = data.split('=')[1]
        data = data.split('"')[1]
        data = data.split('|')[2]
        data = data.split('_')[1]

        if data == 'close':
            logger.debug('trade closed')
            self._trading = False

        if data == 'open':
            logger.debug('trade opening')
            self._trading = True

        self._trading = False

    @run
    def is_trading(self):
        return self._trading

class TradeChecking(object):
    CHECK_IF_TRADING_URL = 'http://appqt.gtimg.cn/utf8/q=marketStat'
    TRADE_CHECK_INTERV = 10
    CAL_CSV_PATH = os.path.join(os.path.dirname(__file__) ,"calAll_2017.csv")
    TRADING_CAL_URL = 'http://vaserviece.10jqka.com.cn/mobilecfxf/data/json_{year}.txt'


    @classmethod
    def check_is_trading(cls):
        url = cls.CHECK_IF_TRADING_URL
        timeout = cls.TRADE_CHECK_INTERV
        data = HttpCache().Request(url,True,timeout)

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

    @classmethod
    def check_trading_day(cls,date):
        dt = arrow.get(date,'YYYY-MM-DD')
        url = cls.TRADING_CAL_URL.format(year=dt.year)

        data = HttpCache().Request(url, cache_timeout_minute=(24*7))
        cal_list = ast.literal_eval(data)

        logging.debug(data)

        date_str = dt.format('MMDD')

        if date_str in cal_list:
            return True

        return False









