#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from intellistock.http_cache import HttpCache
from lxml import etree
import StringIO
import pandas as pd
from html_parser import HtmlParser as hp;
from bs4 import BeautifulSoup
import numpy as np


logger = logging.getLogger(__name__)


class GetKData(object):

    FHPG_URL = 'http://quotes.money.163.com/f10/fhpg_{}.html#01d05'
    '''
    公告日期	分红年度 送股	转增	派息	股权登记日 除权除息日 红股上市日
    '''
    FHPG_INDEX = ['GGRQ', 'FHND', 'SG', 'ZZ', 'PX', 'GQDJR', 'CQCXR', 'HGSSR']

    def __init__(self):
        pass

    @classmethod
    def text(cls,elt):
        return elt


    @classmethod
    def is_head(cls,row):
        attrs = row.get("class")
        if attrs is None:
            return False

        if "dbrow" in attrs:
            return True

        return False

    @classmethod
    def parse_FHPG_cols(cls,cols):
        data = {}


        if len(cols) != 8:
            return None


        for idx,col in enumerate(cols):
            data[cls.FHPG_INDEX[idx]] = [col.text]

        return data


    @classmethod
    def get_FHPG_info(cls,code=None):
        '''
        获得分红配股信息
        '''
        if code is None:
            logger.error('the stock code is empty')
            return None
        df = pd.DataFrame()

        url = cls.FHPG_URL.format(code)
        html = HttpCache().Request(url)

        soup = BeautifulSoup(html,"lxml")
        table = soup.find("table", attrs={"class": "table_bg001 border_box limit_sale"})

        rows = table.find_all("tr")

        for row in rows:
            if not cls.is_head(row):
                cols = row.find_all("td")
                df = df.append(pd.DataFrame(cls.parse_FHPG_cols(cols)),ignore_index=True)

        logger.debug(df)

        return df










