#!/usr/bin/python
# -*- coding: utf-8 -*-

from intellistock.http_cache import HttpCache
import logging
import pandas as pd
from StringIO import StringIO


logger = logging.getLogger(__name__)


class TradeChecking(object):
    CHECK_IF_TRADING_URL = 'http://appqt.gtimg.cn/utf8/q=marketStat'
    TRADE_CHECK_INTERV = 10


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
    def get_all_trade_cal(self):
        data = HttpCache().Request('http://218.244.146.57/static/calAll.csv')
        df = pd.read_csv(StringIO(data))

        all_opened_cal = df.loc[df['isOpen'] == 1]
        cal_list = all_opened_cal['calendarDate'].tolist()

        logger.debug(cal_list)


