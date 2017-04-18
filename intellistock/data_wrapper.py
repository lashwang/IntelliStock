#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logging
import time
from StringIO import StringIO

import arrow
import pandas as pd
import tushare as ts

import config as cf
from database import DataBase
from http_cache import HttpCache
from intellistock.trade.get_k_data import GetKData
from intellistock.trade.get_basic_info import GetBasicInfo
from intellistock.trade.trade_checking import TradeChecking
from intellistock.trade.get_new_stock_list import NewStockData

logger = logging.getLogger(__name__)




class DataWrapper:

    def interface_test(self):
        TradeChecking.check_is_trading()
        TradeChecking.get_all_trade_cal()
        stock_list = ['000001','300619','300414']
        for _code in stock_list:
            #GetBasicInfo.get_FHPG_info(_code)
            #GetBasicInfo.get_GBJG_info(_code)
            pass

        NewStockData.get_new_stock_data()








