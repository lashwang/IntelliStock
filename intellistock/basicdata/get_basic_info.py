#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from intellistock.http_cache import HttpCache
import pandas as pd
from bs4 import BeautifulSoup
import urlparse

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


class GetFHPGInfo(object):


    FHPG_URL = 'http://quotes.money.163.com/f10/fhpg_{}.html#01d05'
    '''
    公告日期	分红年度 送股	转增	派息	股权登记日 除权除息日 红股上市日
    '''
    FHPG_INDEX = ['GGRQ', 'FHND', 'SG', 'ZZ', 'PX', 'GQDJR', 'CQCXR', 'HGSSR']

    def __init__(self):
        pass


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
    def get_FHPG_info(cls,code):
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


class GetGBJGInfo(object):
    '''
    获得股本结构变化信息
    原始url: http://stock.finance.qq.com/corp1/stk_struct.php?zqdm=000001
    '''

    GBJG_URL = "http://stock.finance.qq.com/corp1/stk_struct.php?zqdm={}"

    def __init__(self):
        pass


    @staticmethod
    def parse_total_page(soup):
        tables = soup.find_all("table")
        head = tables[1]
        rows = head.find_all("td")
        last_row = rows[-1].find('a')
        if last_row is not None:
            url = last_row.get('href')
            logger.debug("url is {}".format(url))
            parsed = urlparse.urlparse(url)
            page = urlparse.parse_qs(parsed.query)['type'][0]
            logger.debug("total page is {}, origin URL is {}:".format(page,url))
        else:
            logger.debug("total page is zero")
            page = 0

        return page


    @classmethod
    def get_GBJG_info(cls,code):
        type = 0
        if code is None:
            logger.error('the stock code is empty')
            return None
        df = pd.DataFrame()
        url = cls.GBJG_URL.format(code,type)
        html = HttpCache().Request(url)
        soup = BeautifulSoup(html, "lxml")
        total_page = cls.parse_total_page(soup)













