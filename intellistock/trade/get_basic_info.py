#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from intellistock.http_cache import HttpCache
import pandas as pd
from bs4 import BeautifulSoup
import urlparse
from datetime import datetime
import numpy as np
import utils
from intellistock.trade import *
import StringIO
import html5lib
import arrow

logger = logging.getLogger(__name__)



class GetBasicInfo(object):
    def __init__(self):
        pass

    @classmethod
    def get_FHPG_info(cls,code):
        return GetFHPGInfo.get_FHPG_info(code)


    @classmethod
    def get_GBJG_info(cls,code):
        return GetGBJGInfo.get_GBJG_info(code)


class StockDivInfo(SpiderBase):
    name = "StockDiv"
    URL_FORMAT = 'http://quotes.money.163.com/f10/fhpg_{}.html#01d05'
    HEADS = [u'公告日期',u'分红年度',u'送股',u'转增',u'派息',u'股权登记日',u'除权除息日',u'红股上市日',u'dummy']

    def _check_df_valid(self,df):
        time_str = utils.to_str(df.loc[0][0])
        if utils.is_ascii(time_str):
            try:
                arrow.get(time_str,'YYYY-MM-DD')
            except Exception:
                return False

            return True
        else:
            return False



    def __init__(self, code, **kwargs):
        self.code = code
        self.df = pd.DataFrame()
        super(StockDivInfo, self).__init__(**kwargs)

    def _get_start_url(self):
        return StockDivInfo.URL_FORMAT.format(self.code)

    def _on_response(self, data):
        dfs = pd.read_html(data, attrs={"class": "table_bg001 border_box limit_sale"})
        df = dfs[0]
        if self._check_df_valid(df):
            df.columns = StockDivInfo.HEADS
            logger.debug(df)
        return

    @run_once
    def get_stock_div_info(self):

        return self.df



class GetFHPGInfo(object):


    URL_FORMAT = 'http://quotes.money.163.com/f10/fhpg_{}.html#01d05'
    OUTPUT_HEADERS = [u"分红年度",u"除权除息日",u"送股",u"转增",u"派息"]
    OUTPUT_FORMAT = [datetime,datetime,float,float,float]

    def __init__(self):
        pass


    @classmethod
    def _is_head(cls,row):
        _parent = row.parent
        if _parent.name == "thead":
            return True
        return False

    @classmethod
    def _get_head(cls,row):
        heads = []
        all_th = row.find_all("th")
        for th in all_th:
            if th.get('colspan') is not None:
                continue
            heads.append(th.text)

        return heads


    @classmethod
    def _parse_FHPG_cols(cls,cols):
        data = []


        if len(cols) != 8:
            return data


        for val in cols:
            data.append(val.text)

        return data

    @classmethod
    def _normalise_heads(cls,heads):
        _line_1 = heads[0]
        _line_2 = reversed(heads[1])
        for _val in _line_2:
            _line_1.insert(2,_val)


        return _line_1

    @classmethod
    def _to_pandas_format(cls,heads,rows):
        if len(rows) == 0:
            return pd.DataFrame()
        return pd.DataFrame(rows, columns=heads)

    @classmethod
    def get_FHPG_info(cls,code):
        '''
        获得分红配股信息
        '''
        if code is None:
            logger.error('the stock code is empty')
            return None

        url = cls.URL_FORMAT.format(code)
        html = HttpCache().Request(url)

        soup = BeautifulSoup(html,"lxml")
        table = soup.find("table", attrs={"class": "table_bg001 border_box limit_sale"})

        rows = table.find_all("tr")

        heads = []
        all_rows = []

        for row in rows:
            if not cls._is_head(row):
                cols = row.find_all("td")
                one_row = cls._parse_FHPG_cols(cols)
                if len(one_row) > 0:
                    all_rows.append(one_row)
            else:
                #logger.debug(row)
                heads.append(cls._get_head(row))

        heads = cls._normalise_heads(heads)
        #logger.debug(heads)
        #logger.debug(all_rows)

        df = cls._to_pandas_format(heads,all_rows)
        if len(df) != 0:
            df = df[list(cls.OUTPUT_HEADERS)]
            df = utils._normalise_colomn_format(df, cls.OUTPUT_HEADERS, cls.OUTPUT_FORMAT)


        logger.debug(df)
        return df


class GetGBJGInfo(object):
    '''
    获得股本结构变化信息
    原始url: http://stock.finance.qq.com/corp1/stk_struct.php?zqdm=000001
    '''

    URL_FORMAT = "http://stock.finance.qq.com/corp1/stk_struct.php?zqdm={}"

    OUTPUT_HEADS = [u"变动日期", u"总股本", u"流通股份"]
    OUTPUT_FORMAT = [datetime,int,int]

    def __init__(self):
        pass



    @classmethod
    def _parse_total_page(cls,soup):
        tables = soup.find_all("table")
        head = tables[1]
        rows = head.find_all("td")
        last_row = rows[-1].find('a')
        if last_row is not None:
            url = last_row.get('href')
            logger.debug("url is {}".format(url))
            parsed = urlparse.urlparse(url)
            page = urlparse.parse_qs(parsed.query)['type'][0]
            logger.debug("total page is {}, origin URL is {}".format(page,url))
        else:
            logger.debug("total page is zero")
            page = 0

        return int(page)

    @classmethod
    def _get_table_heads(cls,table):
        data = []
        rows = table.find_all("tr")
        for row in rows:
            heads = row.find_all("th")
            for head in heads:
                data.append(head.text)

        logger.debug(data)

        return data

    @classmethod
    def _normalize_str(cls,_str):
        uniString = utils.to_unicode(_str)
        uniString = uniString.replace(u"\u00A0", "")
        return uniString



    @classmethod
    def _parse_GBJG_table(cls,soup):
        df_dict = {}
        tables = soup.find_all("table")
        table = tables[-1]
        table_heads = cls._get_table_heads(table)
        rows = table.find_all("tr")
        for _idx_row,row in enumerate(rows):
            cols = row.find_all("td")
            _line = []
            for col in (cols):
                _line.append(cls._normalize_str(col.text))

            df_dict[table_heads[_idx_row]] = _line



        df = pd.DataFrame(df_dict)

        df = df[cls.OUTPUT_HEADS]

        return df


    @classmethod
    def _load_page(cls,code,page = 0):
        if page == 0:
            url = cls.URL_FORMAT.format(code)
        else:
            url = cls.URL_FORMAT.format(code) + "&type={}".format(page)

        logger.debug("url is {}".format(url))
        html = HttpCache().Request(url)
        soup = BeautifulSoup(html, "lxml")

        return soup


    @classmethod
    def _remove_empty_lines(cls,df):
        date = cls.OUTPUT_HEADS[0]
        df = df.loc[df[date] != ""]
        return df


    @classmethod
    def get_GBJG_info(cls,code):
        _page_index = 0
        if code is None:
            logger.error('the stock code is empty')
            return None
        soup = cls._load_page(code)
        _total_page = cls._parse_total_page(soup)
        df = cls._parse_GBJG_table(soup)

        while _page_index < _total_page:
            _page_index = _page_index + 1
            soup = cls._load_page(code,_page_index)
            _sub_df = cls._parse_GBJG_table(soup)
            df = df.append(_sub_df,ignore_index=True)

        df = cls._remove_empty_lines(df)
        df = utils._normalise_colomn_format(df,cls.OUTPUT_HEADS,cls.OUTPUT_FORMAT)
        logger.debug(df)
        return df












