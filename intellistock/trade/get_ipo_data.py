#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import pandas as pd
from bs4 import BeautifulSoup


from intellistock.trade import *
from intellistock.trade.utils import *
import traceback

logger = logging.getLogger(__name__)



class IPOData(object):

    KEY_SSRQ = u'上市日期'
    KEY_GPDM = u'股票代码'
    KEY_FXZS = u'发行总数（万股）'
    KEY_WSFX = u'网上发行（万股）'
    KEY_FXJG = u'发行价格'
    KEY_FXSYL = u'发行市盈率'

    def __init__(self,start_time = "2015-01-01"):
        self.start_time = start_time
        self.df = pd.DataFrame()

    def get_df(self):
        ths1 = IPODataTHS1(self.start_time)
        ths1.load_data()
        code = ths1.get_last_code()
        ths2 = IPODataTHS2(code)
        ths2.load_data()
        df1 = ths1.get_df()
        df2 = ths2.get_df()
        df_final = reduce(lambda left, right: pd.merge(left, right, on=IPOData.KEY_GPDM), [df1,df2])
        df_final = df_final.set_index(IPOData.KEY_SSRQ)
        float_headers = list(df_final.columns)[2:6]
        df_final[float_headers] = df_final[float_headers].astype(float)

        '''
        Format digital data
        '''
        # op = float_headers[0]
        # df_final[op] = df_final[op]/10000
        # op = float_headers[1]
        # df_final[op] = df_final[op]/10000
        op = float_headers[2]
        df_final[op] = df_final[op].map(FORMAT)
        op = float_headers[3]
        df_final[op] = df_final[op].map(FORMAT)
        df_final[float_headers] = df_final[float_headers].astype(float)

        '''
        add stock type
        '''
        name = u'股票类型'
        df_final[name] = df_final[IPOData.KEY_GPDM].map(lambda x:get_stock_type(x))

        return df_final

    @staticmethod
    def parse_html(raw_html):
        return BeautifulSoup(markup=raw_html, features='lxml',from_encoding='GBK')

    @staticmethod
    def format_stock_code(df):
        df.loc[:, IPOData.KEY_GPDM] = df.loc[:, IPOData.KEY_GPDM].map(FORMAT_STOCK_CODE)
        return df


class IPODataTHS1(SpiderBase):
    name = __name__
    START_URL = 'http://data.10jqka.com.cn/ipo/xgsr/'
    NEXT_URL = 'http://data.10jqka.com.cn/ipo/xgsr/field/SSRQ/order/desc/page/{page}/ajax/1/'


    def __init__(self,start_time, **kwargs):
        super(IPODataTHS1, self).__init__(**kwargs)
        self.page = 1
        self.total_pages = -1
        self.start_time = start_time

    def _get_total_pages(self,html):
        tag = html.find_all(class_='page_info')
        tag = tag[0].text
        return int(tag.split('/')[1])


    def _parse(self, data):
        self.page = self.page +1
        if self.current_url == self.cls.START_URL:
            html = IPOData.parse_html(data)
            self.total_pages = self._get_total_pages(html)

        df = pd.read_html(data,flavor='bs4',encoding='GBK')[0]
        self.df = self.df.append(df)
        dates = df[IPOData.KEY_SSRQ]
        if dates.min() < self.start_time:
            return
        if self.page <= self.total_pages:
            return self.cls.NEXT_URL.format(page=self.page)

    def _get_start_url(self):
        return self.cls.START_URL


    def get_last_code(self):
        return self.df.iloc[-1][IPOData.KEY_GPDM]

    def _on_parse_finished(self):
        KEY_GPDM = IPOData.KEY_GPDM
        KEY_SSRQ = IPOData.KEY_SSRQ
        headers = [KEY_GPDM,KEY_SSRQ]
        df = self.df
        df = df[df[KEY_SSRQ] >= self.start_time]
        if df[KEY_SSRQ].min() < self.start_time:
            raise ValueError
        df = df[headers]
        df= IPOData.format_stock_code(df)
        self.df = df

class IPODataTHS2(SpiderBase):
    name = __name__
    START_URL = 'http://data.10jqka.com.cn/ipo/xgsgyzq/'
    NEXT_URL = 'http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/{page}/order/desc/ajax/1/'



    def __init__(self,code,**kwargs):
        super(IPODataTHS2, self).__init__(**kwargs)
        self.page = 1
        self.total_pages = -1
        self.code = str(code)


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
        html = IPOData.parse_html(data)
        self.page = self.page + 1
        if self.current_url == self.start_url:
            tag = html.find_all(class_="page_info")
            if len(tag) < 1:
                raise ValueError("can't parse url :" + self.start_url)
            page_info = tag[0].text
            self.total_pages = int(page_info.split('/')[1])
        df = self._read_html(html)
        self.df = self.df.append(df)
        if self.code in list(df[IPOData.KEY_GPDM]):
            return None

        if self.page <= self.total_pages:
            return self.cls.NEXT_URL.format(page=self.page)
        else:
            return None


    def _get_start_url(self):
        return self.cls.START_URL

    def _on_parse_finished(self):
        KEY_GPDM = IPOData.KEY_GPDM
        headers = list(self.df.columns)
        '''
        0 = {unicode} u'股票代码'
        1 = {unicode} u'股票简称'
        2 = {unicode} u'发行总数（万股）'
        3 = {unicode} u'网上发行（万股）'
        4 = {unicode} u'发行价格'
        5 = {unicode} u'发行市盈率'
        6 = {unicode} u'行业市盈率'
        7 = {unicode} u'涨停数量'
        '''
        headers = [u'股票代码',u'股票简称',u'发行总数（万股）',u'网上发行（万股）',u'发行价格',u'发行市盈率']

        df = self.df
        df = df[headers]
        df = IPOData.format_stock_code(df)
        self.df = df



# class IPODataQQ(SpiderBase):
#     name = "NewStockQQ"
#     QQ_XINGU_URL = 'http://web.ifzq.gtimg.cn/stock/xingu/xgrl/xgql?' \
#                    'type=all&page={}&psize={}&col=sgrq&order=desc&_var=v_xgql'
#     QQ_XINGU_DEFAULT_PAGE_SIZE = 100
#
#     def __init__(self,**kwargs):
#         self.page = 1
#         self.total_pages = -1
#         super(IPODataQQ, self).__init__(**kwargs)
#
#     def _parse(self, data):
#         lines = data.split('=')[1]
#         js = json.loads(lines)
#         df = pd.DataFrame(js['data']['data'])
#         self.df = self.df.append(df)
#         if self.total_pages == -1:
#             self.total_pages = js['data']['totalPages']
#         self.page = self.page + 1
#
#         if self.page <= self.total_pages:
#             return self.cls.QQ_XINGU_URL.format(self.page,self.cls.QQ_XINGU_DEFAULT_PAGE_SIZE)
#
#         return None
#
#     def _get_start_url(self):
#         return self.cls.QQ_XINGU_URL.format(self.page,self.cls.QQ_XINGU_DEFAULT_PAGE_SIZE)
#
#     @run_once
#     def load_data(self):
#         logger.debug(self.df)
#         return self.df
#
#     def get_unlisted_stock(self):
#         '''
#         未上市新股
#         :return:
#         '''
#         pass
#
#     def get_listed_stock(self):
#         '''
#         已上市新股
#         :return:
#         '''
#         pass
#
#     def get_unbroken_stock_list(self):
#         '''
#         已上市未破板新股
#         :return:
#         '''
#         pass
#
#     def get_broken_stock_list(self):
#         '''
#         已上市已破板新股
#         :return:
#         '''
#         pass


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

