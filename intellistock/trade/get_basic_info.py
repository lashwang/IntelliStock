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
        super(StockDivInfo, self).__init__(**kwargs)

    def _get_start_url(self):
        return self.cls.URL_FORMAT.format(self.code)

    def _parse(self, data):
        dfs = pd.read_html(data, attrs={"class": "table_bg001 border_box limit_sale"})
        df = dfs[0]
        if self._check_df_valid(df):
            df.columns = self.cls.HEADS
            logger.debug(df)
        return

    @run_once
    def get_df(self):
        return self.df


class StockStructureInfo(SpiderBase):

    name = "StockStructure"
    URL_FORMAT = "http://stock.finance.qq.com/corp1/stk_struct.php?zqdm={}"

    def __init__(self, code, **kwargs):
        self.code = code
        self.page = 0
        self.total_page = -1
        super(StockStructureInfo, self).__init__(self,**kwargs)


    def _parse_total_page(self,soup):
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

    def _parse(self, data):
        logger.debug("_parse")
        dfs = pd.read_html(data)
        df = dfs[-1]
        df = df.T
        self.df = self.df.append(df)


        if self.total_page == -1:
            self.total_page = self._parse_total_page(BeautifulSoup(data, "lxml"))
        self.page = self.page + 1
        logger.debug("page is:{}".format(self.page))

        if self.page <= self.total_page:
            url = self.cls.URL_FORMAT.format(self.code) + "&type={}".format(self.page)
            return url
        else:
            return None


    def _get_start_url(self):
        return self.cls.URL_FORMAT.format(self.code)


    @run_once
    def get_df(self):
        logger.debug(self.df)
        return self.df














