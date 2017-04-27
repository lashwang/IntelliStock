#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

import tushare as ts

logger = logging.getLogger(__name__)


class GetTopList(object):
    def __init__(self):
        pass

    def get_longhu_list(self):
        #http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,sortType=,startDate=2017-03-27,endDate=2017-03-27,gpfw=0,js=vardata_tab_1.html
        df = ts.top_list('2017-03-27')
        logger.debug(df)
