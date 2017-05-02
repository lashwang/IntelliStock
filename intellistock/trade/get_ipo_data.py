#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import pandas as pd
from bs4 import BeautifulSoup


from intellistock.trade import *
from intellistock.trade.utils import *

logger = logging.getLogger(__name__)


class IPOData(SpiderBase):
    name = "IPO_10jqka"
    START_URL = 'http://data.10jqka.com.cn/ipo/xgsgyzq/'
    NEXT_URL = 'http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/{page}/order/desc/ajax/1/'


    def __init__(self, **kwargs):
        super(IPOData, self).__init__(**kwargs)
        self.page = 1
        self.total_pages = -1


    def _read_html(self,html):
        headers = html.find(class_='m_table').find('thead').find_all('th')
        header_list = [head.text.strip() for head in headers]
        tr_list = html.find(class_='m_tbd').find_all('tr')
        all_data = []
        for tr in tr_list:
            line_data = [td.text.strip() for td in tr.find_all('td')]
            if len(line_data) != len(header_list):
                raise ValueError
            all_data.append(line_data)
        return pd.DataFrame(all_data,columns=header_list)

    def _parse(self, data):
        html = BeautifulSoup(data,'lxml')
        self.page = self.page + 1
        if self.current_url == self.start_url:
            tag = html.find_all(class_="page_info")
            if len(tag) < 1:
                raise ValueError("can't parse url :" + self.start_url)
            page_info = tag[0].text
            self.total_pages = int(page_info.split('/')[1])
            df = self._read_html(html)
            self.df = self.df.append(df)
            return self.cls.NEXT_URL.format(page=self.page)
        else:
            df = self._read_html(html)
            self.df = self.df.append(df)

            if self.page <= self.total_pages:
                return self.cls.NEXT_URL.format(page=self.page)
            else:
                return None


    def _get_start_url(self):
        return self.cls.START_URL




class IPODataQQ(SpiderBase):
    name = "NewStockQQ"
    QQ_XINGU_URL = 'http://web.ifzq.gtimg.cn/stock/xingu/xgrl/xgql?' \
                   'type=all&page={}&psize={}&col=sgrq&order=desc&_var=v_xgql'
    QQ_XINGU_DEFAULT_PAGE_SIZE = 100

    def __init__(self,**kwargs):
        self.page = 1
        self.total_pages = -1
        super(IPODataQQ, self).__init__(**kwargs)

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

