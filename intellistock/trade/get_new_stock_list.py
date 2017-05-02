#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import pandas as pd

from intellistock.trade import *

logger = logging.getLogger(__name__)


class NewStockList(SpiderBase):
    name = "NewStockQQ"
    QQ_XINGU_URL = 'http://web.ifzq.gtimg.cn/stock/xingu/xgrl/xgql?' \
                   'type=all&page={}&psize={}&col=sgrq&order=desc&_var=v_xgql'
    QQ_XINGU_DEFAULT_PAGE_SIZE = 100

    def __init__(self,**kwargs):
        self.page = 1
        self.total_pages = -1
        super(NewStockList, self).__init__(**kwargs)

    def _parse(self, data):
        lines = data.split('=')[1]
        js = json.loads(lines)
        df = pd.DataFrame(js['data']['data'])
        self.df = self.df.append(df)
        if self.total_pages == -1:
            self.total_pages = js['data']['totalPages']
        self.page = self.page + 1

        if self.page <= self.total_pages:
            return self.cls.QQ_XINGU_URL.format(self.page,self.cls.QQ_XINGU_DEFAULT_PAGE_SIZE)

        return None

    def _get_start_url(self):
        return self.cls.QQ_XINGU_URL.format(self.page,self.cls.QQ_XINGU_DEFAULT_PAGE_SIZE)

    @run_once
    def load_data(self):
        logger.debug(self.df)
        return self.df

    def get_unlisted_stock(self):
        '''
        未上市新股
        :return: 
        '''
        pass

    def get_listed_stock(self):
        '''
        已上市新股
        :return: 
        '''
        pass

    def get_unbroken_stock_list(self):
        '''
        已上市未破板新股
        :return: 
        '''
        pass

    def get_broken_stock_list(self):
        '''
        已上市已破板新股
        :return: 
        '''
        pass


# class NewStockData(object):
#     QQ_XINGU_URL = 'http://web.ifzq.gtimg.cn/stock/xingu/xgrl/xgql?' \
#                    'type=all&page={}&psize={}&col=sgrq&order=desc&_var=v_xgql'
#     QQ_XINGU_DEFAULT_PAGE_SIZE = 100
#
#     NEW_STOCK_HEADERS = ["fxj","fxsyl","fxzs","mzyqy","sclx","sgdm","sgrq","sgsx","ssrq","wsfx","zqdm","zqjc","zql"]
#     NEW_STOCK_HEADERS_TRANS = [u"发行价", u"发行市盈率", u"发行总数", u"每中一签约", u"发行地", u"申购代码", u"申购日期",
#                                u"申购上限", u"上市日期", u"网上发行", u"中签代码",u"股票简称", u"中签率"]
#
#     NEW_STOCK_OUTPUT_HEADERS = [u"申购日期",u"上市日期",u"股票简称",u"中签代码",u"发行价",u"发行市盈率",u"网上发行",u"发行总数"]
#
#     NEW_STOCK_OUTPUT_FORMATER = [datetime,datetime,str,str,float,float,float,float]
#
#     def __init__(self):
#         pass
#
#     @classmethod
#     def _get_new_stock_url(cls,_page = 1,_page_size = QQ_XINGU_DEFAULT_PAGE_SIZE):
#         return cls.QQ_XINGU_URL.format(_page,_page_size)
#
#     @classmethod
#     def _normalize_output_data(cls,df):
#         df.columns = cls.NEW_STOCK_HEADERS_TRANS
#         df = df[cls.NEW_STOCK_OUTPUT_HEADERS]
#         return df
#
#
#     @classmethod
#     def _get_new_stock_list(cls,_page = 1):
#         url = cls._get_new_stock_url(_page)
#         lines = HttpCache().Request(url)
#         if len(lines) < 100:  # no data
#             return None
#         lines = lines.split('=')[1]
#         js = json.loads(lines)
#         #logging.debug(js)
#         data = pd.DataFrame(js['data']['data'])
#         totalPages = js['data']['totalPages']
#         return {'totalPages':totalPages,'data':data}
#
#     @classmethod
#     def _get_new_stock_data(cls):
#         pageIndex = 1
#         totalPages = 0
#         ret = cls._get_new_stock_list(pageIndex)
#         totalPages = ret['totalPages']
#         df = ret['data']
#         logging.debug(totalPages)
#
#         while pageIndex < totalPages:
#             pageIndex = pageIndex + 1
#             ret = cls._get_new_stock_list(pageIndex)
#             df = df.append(ret['data'])
#             time.sleep(cf.REQUEST_DELAY)
#
#         df = cls._normalize_output_data(df)
#         df = utils._normalise_colomn_format(df,cls.NEW_STOCK_OUTPUT_HEADERS,cls.NEW_STOCK_OUTPUT_FORMATER)
#         logging.debug(df)
#         return df
#
#     @classmethod
#     def get_new_stock_data(cls):
#         return cls._get_new_stock_data()
#
#

