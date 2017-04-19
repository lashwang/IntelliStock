#!/usr/bin/python
# -*- coding: utf-8 -*-

from intellistock.http_cache import HttpCache
import logging
import pandas as pd
from StringIO import StringIO
import os
import arrow
import ast

logger = logging.getLogger(__name__)


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









