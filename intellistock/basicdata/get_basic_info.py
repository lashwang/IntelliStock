#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from intellistock.http_cache import HttpCache
import pandas as pd
from bs4 import BeautifulSoup
import urlparse
from datetime import datetime
from collections import OrderedDict

logger = logging.getLogger(__name__)


def _to_unicode(_str):
    if isinstance(_str, unicode):
        return _str

    return _str.decode('utf-8')


def _string_to_hex(_string):
    if isinstance(_string,unicode):
        _string = _string.encode("utf8")

    return ':'.join(x.encode('hex') for x in _string)

def _type_compare(type1,type2):
    return type1.__name__ == type2.__name__


def _normalise_colomn_format(_df,_header,_formator):
    for _idx,_format in enumerate(_formator):
        _key = _header[_idx]
        if _type_compare(_format,datetime):
            _df[_key] = pd.to_datetime(_df[_key])
            pass
        elif _type_compare(_format,float):
            _df[_key].replace(u'--',0,inplace=True)
            _df[_key] = pd.to_numeric(_df[_key])
            pass


    return _df


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
            df = _normalise_colomn_format(df, cls.OUTPUT_HEADERS, cls.OUTPUT_FORMAT)


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
        rows = table.find_all("tr")
        for _idx_row,row in enumerate(rows):
            cols = row.find_all("td")
            _line = []
            for col in (cols):
                _line.append(cls._normalize_str(col.text))

            df_dict[table_heads[_idx_row]] = _line



        df = pd.DataFrame(df_dict)

        df = df[cls.GBJG_HEADS]

        return df


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












