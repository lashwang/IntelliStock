#!/usr/bin/python
# -*- coding: utf-8 -*-

from intellistock.http_cache import HttpCache
import logging
import pandas as pd
from StringIO import StringIO
import os
import arrow
import ast
from intellistock.trade import *


logger = logging.getLogger(__name__)


class StockCalDay(SpiderBase):
    name = __name__
    CAL_DAY_URL = 'http://vaserviece.10jqka.com.cn/mobilecfxf/data/json_{year}.txt'

    def __init__(self,cal):
        self._cal = arrow.get(cal, 'YYYY-MM-DD')
        super(StockCalDay, self).__init__()

        self.cache_timeout = 7*24


    def _get_start_url(self):
        url = self.cls.CAL_DAY_URL.format(year=self._cal.year)
        return url


    def _parse(self, data):
        self._cal_list = ast.literal_eval(data)
        self._trade_day = self._check_trading_day()

    def _check_trading_day(self):
        date_str = self._cal.format('MMDD')

        if date_str in self._cal_list:
            return True

        return False

    @run_once
    def is_trading_day(self):
        return self._trade_day




class StockTradeTime(SpiderBase):
    name = __name__
    CHECK_IF_TRADING_URL = 'http://appqt.gtimg.cn/utf8/q=marketStat'

    def __init__(self):
        super(StockTradeTime,self).__init__()
        self.cache_timeout = 1

    def _get_start_url(self):
        return StockTradeTime.CHECK_IF_TRADING_URL

    def _parse(self, data):
        data = data.split('=')[1]
        data = data.split('"')[1]
        data = data.split('|')[2]
        data = data.split('_')[1]

        if data == 'close':
            logger.debug('trade closed')
            self._trading = False
        elif data == 'open':
            logger.debug('trade opening')
            self._trading = True
        else:
            raise ValueError("unknow http response{}".format(data))

    @run_once
    def is_trading_time(self):
        return self._trading










