#!/usr/bin/python
# -*- coding: utf-8 -*-


import logging
from datetime import datetime

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)



def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def to_unicode(_str):
    if isinstance(_str, unicode):
        return _str



    try:
        _unicode = _str.decode('utf-8')
        return _unicode
    except Exception,error:
        logger.error(error)

    try:
        _unicode = _str.decode('gbk')
        return _unicode
    except Exception, error:
        logger.error(error)


def to_str(_str):
    if isinstance(_str,str):
        return _str

    return _str.encode('utf-8')


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
            _df[_key] = pd.to_datetime(_df[_key], errors='coerce')
            pass
        elif _type_compare(_format,float) or _type_compare(_format,int):
            _df[_key].replace(u'--',0,inplace=True)
            _df[_key] = _df[_key].astype(np.str).str.replace(',','')
            _df[_key] = pd.to_numeric(_df[_key])
            _df[_key].fillna(0.0, inplace=True)

            pass



    return _df

FORMAT_STOCK_CODE = lambda x:str(x).zfill(6)
FORMAT = lambda x: '%.2f' % x
FORMAT4 = lambda x: '%.4f' % x

SZ_START_CODE = ["000", "002", "300"]
SH_START_CODE = ["60"]


def code_format(code):
    code = to_str(code)
    if code[0:3] in SZ_START_CODE:
        return "sz" + code

    if code[0:2] in SH_START_CODE:
        return "sh" + code

    raise SyntaxError(code)


def get_stock_type(code):
    code = to_str(code)
    if code[0:3] in SZ_START_CODE:
        index = SZ_START_CODE.index(code[0:3])
        if index == 0:
            return u'深圳主板'
        elif index == 1:
            return u'深圳中小板'
        else:
            return u'深圳创业板'

    if code[0:2] in SH_START_CODE:
        return u"上海"

    raise SyntaxError(code)
