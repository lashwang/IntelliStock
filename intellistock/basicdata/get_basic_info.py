#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from intellistock.http_cache import HttpCache
import pandas as pd
from bs4 import BeautifulSoup
import urlparse

logger = logging.getLogger(__name__)


def _to_unicode(_str):
    if isinstance(_str, unicode):
        return _str

    return _str.decode('utf-8')


def _string_to_hex(_string):
    if isinstance(_string,unicode):
        _string = _string.encode("utf8")

    return ':'.join(x.encode('hex') for x in _string)





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

    FHPG_SELECT_HEADS = [u"分红年度",u"除权除息日",u"送股",u"转增",u"派息"]


    def __init__(self):
        pass


    @classmethod
    def _is_head(cls,row):
        attrs = row.get("class")
        if attrs is None:
            return False

        if "dbrow" in attrs:
            return True

        return False

    @classmethod
    def _get_head(cls,row):
        heads = []
        all_th = row.find_all("th")
        for th in all_th:
            heads.append(th.text)

        return heads


    @classmethod
    def _parse_FHPG_cols(cls,cols):
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

        heads = []

        for row in rows:
            if not cls._is_head(row):
                cols = row.find_all("td")
                df = df.append(pd.DataFrame(cls._parse_FHPG_cols(cols)),ignore_index=True)
            else:
                logger.debug(row)
                heads.append(cls._get_head(row))

        logger.debug(heads)
        logger.debug(df)

        return df


class GetGBJGInfo(object):
    '''
    获得股本结构变化信息
    原始url: http://stock.finance.qq.com/corp1/stk_struct.php?zqdm=000001
    '''

    GBJG_URL = "http://stock.finance.qq.com/corp1/stk_struct.php?zqdm={}"

    GBJG_HEADS = [u"变动日期",u"总股本",u"流通股份",u"限售流通股",u"未流通股份"]


    def __init__(self):
        pass

    @classmethod
    def _find_index(cls,head,sub_head):
        index = []

        for _sub_head in sub_head:
            index.append(head.index(_to_unicode(_sub_head)))

        logger.debug(index)

        return index

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
        uniString = _to_unicode(_str)
        uniString = uniString.replace(u"\u00A0", "")
        return uniString



    @classmethod
    def _parse_GBJG_table(cls,soup):
        df_dict = {}
        tables = soup.find_all("table")
        table = tables[-1]
        table_heads = cls._get_table_heads(table)
        select_heads = cls._find_index(table_heads,GetGBJGInfo.GBJG_HEADS)
        rows = table.find_all("tr")
        for _idx_row,row in enumerate(rows):
            if _idx_row not in select_heads:
                continue
            _head_index = select_heads.index(_idx_row)
            cols = row.find_all("td")

            _line = []
            for _idx_col, col in enumerate(cols):
                _line.append(cls._normalize_str(col.text))

            df_dict[cls.GBJG_HEADS[_head_index]] = _line



        return pd.DataFrame(df_dict)


    @classmethod
    def _load_page(cls,code,page = 0):
        if page == 0:
            url = cls.GBJG_URL.format(code)
        else:
            url = cls.GBJG_URL.format(code) + "&type={}".format(page)

        logger.debug("url is {}".format(url))
        html = HttpCache().Request(url)
        soup = BeautifulSoup(html, "lxml")

        return soup


    @classmethod
    def _remove_empty_lines(cls,df):
        date = cls.GBJG_HEADS[0]
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
        logger.debug(df)
        return df












