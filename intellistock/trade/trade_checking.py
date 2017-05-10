#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast

import arrow

from intellistock.trade import *
from operator import itemgetter


logger = logging.getLogger(__name__)


class StockCalDay(SpiderBase):
    name = __name__
    YEAR_START = 2005
    CAL_DAY_URL = 'http://vaserviece.10jqka.com.cn/mobilecfxf/data/json_{year}.txt'

    def __init__(self,**kwargs):
        super(StockCalDay, self).__init__(**kwargs)
        self.cache_timeout = 30 * 24
        self.year_start = self.cls.YEAR_START
        self.year_index = self.year_start
        self.year_end = arrow.now().year
        self.cal_list = {}


    def _get_start_url(self):
        url = self.cls.CAL_DAY_URL.format(year=self.year_start)
        return url


    def _parse(self, data):
        cal_list = ast.literal_eval(data)
        self.cal_list[self.year_index] = cal_list
        self.year_index = self.year_index + 1
        if self.year_index > self.year_end:
            return

        return self.cls.CAL_DAY_URL.format(year=self.year_index)

    def _on_parse_finished(self):
        pass


    def _parser_date_param(self,date):
        if date is None:
            a = arrow.now()
        else:
            a = arrow.get(date,'YYYY-MM-DD')

        return a

    def check_trading_day(self,date=None):
        '''
        check if the given date is the trading day.
        :param date:YYYY-MM-DD, 
        :return: 
        '''


        a = self._parser_date_param(date)

        date_str = a.format('MMDD')
        if date_str in self.cal_list[a.year]:
            return True
        return False

    def get_last_trading_day(self,date=None):
        a = self._parser_date_param(date)
        #a = a.replace(days=-1)
        year = a.year
        mmdd = None

        date_str = a.format('MMDD')

        if date_str <= self.cal_list[a.year][0]:
            year = a.year - 1
            mmdd = self.cal_list[a.year - 1][-1]

        if date_str > self.cal_list[a.year][-1]:
            mmdd = self.cal_list[a.year][-1]


        for index,key in enumerate(self.cal_list[year]):
            if key >= date_str:
                mmdd = self.cal_list[year][index-1]
                break

        if mmdd is None:
            raise ValueError

        return "{}-{}-{}".format(year,mmdd[0:2],mmdd[2:4])


    def get_cal_list(self):
        return self.cal_list



class StockTradeTime(SpiderBase):
    name = __name__
    CHECK_IF_TRADING_URL = 'http://appqt.gtimg.cn/utf8/q=marketStat'

    def __init__(self):
        super(StockTradeTime,self).__init__()
        self.cache_timeout = 1

    def _get_start_url(self):
        return self.cls.CHECK_IF_TRADING_URL

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










