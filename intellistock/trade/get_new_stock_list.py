#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from intellistock.http_cache import HttpCache
import json
import pandas as pd
import time
from intellistock import config as cf

logger = logging.getLogger(__name__)



class NewStockData(object):
    QQ_XINGU_URL = 'http://web.ifzq.gtimg.cn/stock/xingu/xgrl/xgql?' \
                   'type=all&page={}&psize={}&col=sgrq&order=desc&_var=v_xgql'
    QQ_XINGU_DEFAULT_PAGE_SIZE = 100

    NEW_STOCK_HEADERS = ["fxj","fxsyl","fxzs","mzyqy","sclx","sgdm","sgrq","sgsx","ssrq","wsfx","zqdm","zqjc","zql"]
    NEW_STOCK_HEADERS_TRANS = [u"发行价", u"发行市盈率", u"发行总数", u"每中一签约", u"发行地", u"申购代码", u"申购日期",
                               u"申购上限", u"上市日期", u"网上发行", u"中签代码",u"股票简称", u"中签率"]

    NEW_STOCK_OUTPUT_HEADERS = [u"申购日期",u"股票简称",u"中签代码",u"发行价",u"发行市盈率",u"网上发行",u"发行总数"]


    def __init__(self):
        pass

    @classmethod
    def _get_new_stock_url(cls,_page = 1,_page_size = QQ_XINGU_DEFAULT_PAGE_SIZE):
        return cls.QQ_XINGU_URL.format(_page,_page_size)

    @classmethod
    def _normalize_output_data(cls,df):
        df.columns = cls.NEW_STOCK_HEADERS_TRANS
        df = df[cls.NEW_STOCK_OUTPUT_HEADERS]
        return df


    @classmethod
    def _get_new_stock_list(cls,_page = 1):
        url = cls._get_new_stock_url(_page)
        lines = HttpCache().Request(url)
        if len(lines) < 100:  # no data
            return None
        lines = lines.split('=')[1]
        js = json.loads(lines)
        #logging.debug(js)
        data = pd.DataFrame(js['data']['data'])
        totalPages = js['data']['totalPages']
        return {'totalPages':totalPages,'data':data}

    @classmethod
    def _get_new_stock_data(cls):
        pageIndex = 1
        totalPages = 0
        ret = cls._get_new_stock_list(pageIndex)
        totalPages = ret['totalPages']
        df = ret['data']
        logging.debug(totalPages)

        while pageIndex < totalPages:
            pageIndex = pageIndex + 1
            ret = cls._get_new_stock_list(pageIndex)
            df = df.append(ret['data'])
            time.sleep(cf.REQUEST_DELAY)

        df = cls._normalize_output_data(df)
        logging.debug(df)
        return df

    @classmethod
    def get_new_stock_data(cls):
        return cls._get_new_stock_data()