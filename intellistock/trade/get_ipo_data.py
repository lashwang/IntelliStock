#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import pandas as pd
from bs4 import BeautifulSoup
from intellistock.trade import *
from intellistock.trade.utils import *
import traceback
from intellistock.trade.get_k_data import *


logger = logging.getLogger(__name__)



class IPOData(object):

    KEY_SSRQ = 'list_date'
    KEY_GPDM = 'code'
    KEY_FXZS = 'issue_number_total'
    KEY_WSFX = 'issue_number_online'
    KEY_FXJG = 'issue_price'


    def __init__(self,start_time = "2015-01-01"):
        self.start_time = start_time
        self.df_raw = pd.DataFrame()
        self.df_broken = pd.DataFrame()
        self.df_unbroken = pd.DataFrame()

    def _get_df_raw(self):
        ths1 = IPODataTHS1(self.start_time)
        ths1.load_data()
        last_stock_code = ths1.get_last_stock_code()
        ths2 = IPODataTHS2(last_stock_code)
        ths2.load_data()
        df1 = ths1.get_df()
        df2 = ths2.get_df()
        df_final = reduce(lambda left, right:
                          pd.merge(left, right, on=None,left_index=True,right_index=True), [df1,df2])
        float_headers = ['issue_number_total','issue_number_online','issue_price']
        df_final[float_headers] = df_final[float_headers].astype(float)
        name = 'stock_type'
        df_final[name] = df_final.index.map(lambda x:get_stock_type(x))
        df_final.sort_values('list_date',axis=0,ascending=False,inplace=True)
        self.df_raw = df_final

    def _get_calculated_ipo_data(self):
        df_ipo = self.df_raw
        df_final = pd.DataFrame()

        for index, row in df_ipo.iterrows():
            param = KDataParam(index)
            kdata = KData(param)
            param.date_from = row.list_date
            param.fq_type = FQType.NFQ
            df_kdata = kdata.get_k_data()
            row_calced = self.calculate_ipo_data(row,df_kdata)
            df_final = df_final.append(row_calced)


        self.df_broken = df_final[df_final.broken == True]
        self.df_unbroken = df_final[df_final.broken == False]

        self.df_broken = self.df_broken.drop('broken',axis=1)
        self.df_unbroken = self.df_unbroken.drop('broken', axis=1)

    def calculate_ipo_data(self,ipo_row,k_data):
        daily_limit_number = 0
        high_price = 0
        income = 0
        is_broken = False
        for index,k_row in k_data.iterrows():
            high_price = k_row['high']
            if index == 0:
                k_row['change'] = k_row['close'] - ipo_row.issue_price
                k_row['change_rate'] = k_row['change']/ipo_row.issue_price
                k_row['change_rate'] = round(k_row['change_rate']*100,2)
                # 上市第一天
                if round(k_row['change_rate'],0) >= 44:
                    daily_limit_number = daily_limit_number + 1
                    continue

            high_price = k_row['high']
            # 计算涨停数
            if (k_row['open'] == k_row['close'] == k_row['high'] == k_row['low']) \
                    and (round(k_row['change_rate'],0) >= 10):
                    daily_limit_number = daily_limit_number+1
            else:
                ipo_row[u'broken_date'] = k_row['date']
                is_broken = True
                break
        # end for


        ipo_row[u'broken'] = is_broken
        ipo_row[u'涨停数'] = daily_limit_number

        if is_broken:
            ipo_row[u'破板日换手率'] = k_row['turnover']
            ipo_row[u'破板后最高价'] = k_data['high'].max()
            ipo_row[u'破板后最低价'] = k_data[k_data['date'] >= k_row['date']].low.min()
            ipo_row[u'破板价'] = high_price
            ipo_row[u'破板时流通市值'] = round(ipo_row.issue_number_total * high_price/10000,2)



        if code_format(k_row['code']).startswith('sh'):
            income = (high_price - ipo_row.issue_price)*1000
        else:
            income = (high_price - ipo_row.issue_price)*500
        ipo_row[u'中签收益(万)'] = income/10000
        return ipo_row


    def load_data(self):
        self._get_df_raw()
        self._get_calculated_ipo_data()


    @staticmethod
    def parse_html(raw_html):
        return BeautifulSoup(markup=raw_html, features='lxml',from_encoding='GBK')

    @staticmethod
    def format_stock_code(df):
        df['code'] = df['code'].map(FORMAT_STOCK_CODE)
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
        headers = [u'股票代码',u'上市日期']
        headers_trans = ['code','list_date']
        df = df[headers]
        df.rename(columns=lambda x:headers_trans[headers.index(x)], inplace=True)
        self.df = self.df.append(df)
        dates = df.list_date
        if dates.min() < self.start_time:
            return
        if self.page <= self.total_pages:
            return self.cls.NEXT_URL.format(page=self.page)

    def _get_start_url(self):
        return self.cls.START_URL


    def get_last_stock_code(self):
        return self.df.index[-1]

    def _on_parse_finished(self):
        df = self.df
        df = df[df.list_date >= self.start_time]
        latest_date = get_last_valid_date()
        df = df[df.list_date < latest_date]

        if df.list_date.min() < self.start_time:
            raise ValueError
        df= IPOData.format_stock_code(df)
        df.set_index('code',inplace=True)
        self.df = df

class IPODataTHS2(SpiderBase):
    name = __name__
    START_URL = 'http://data.10jqka.com.cn/ipo/xgsgyzq/'
    NEXT_URL = 'http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/{page}/order/desc/ajax/1/'



    def __init__(self,contains_stock_code,**kwargs):
        super(IPODataTHS2, self).__init__(**kwargs)
        self.page = 1
        self.total_pages = -1
        self.contains_stock_code = contains_stock_code


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
        all_list_code = list(df[u'股票代码'])
        if self.contains_stock_code in all_list_code:
            return None

        if self.page <= self.total_pages:
            return self.cls.NEXT_URL.format(page=self.page)
        else:
            return None


    def _get_start_url(self):
        return self.cls.START_URL

    def _on_parse_finished(self):
        '''
        0 = {unicode} u'股票代码'
        1 = {unicode} u'股票简称'
        2 = {unicode} u'发行总数（万股）'
        3 = {unicode} u'网上发行（万股）'
        4 = {unicode} u'发行价格'
        '''
        headers = [u'股票代码',u'股票简称',u'发行总数（万股）',u'网上发行（万股）',u'发行价格']
        headers_trans = ['code','name','issue_number_total','issue_number_online','issue_price']

        df = self.df
        df = df[headers]
        df.rename(columns=lambda x: headers_trans[headers.index(x)], inplace=True)
        df = IPOData.format_stock_code(df)
        df.set_index('code',inplace=True)
        self.df = df



