#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import utils
import pandas as pd
from enum import Enum
import arrow
from intellistock.http_cache import HttpCache
import json
from intellistock.trade import *


logger = logging.getLogger(__name__)


class FQType(Enum):
    QFQ = 'qfq' #前复权
    HFQ = 'hfq' #后复权
    BFQ = 'nfq'    #不复权

class DataType(Enum):
    pass

class KDataParam(object):
    def __init__(self):
        self.code = None
        self.start = None
        self.end = None
        self.fq = FQType.QFQ




class KDataBase(SpiderBase):
    pass


# class GetKData(object):
#
#     URL_FORMAT = "http://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get?p=1&param={code},{k_type},{start_day},{end_day},{number},{fq}"
#     SZ_START_CODE = ["000","002","300"]
#     SH_START_CODE = ["60"]
#
#     class KDayType(Enum):
#         DAY = 'day'
#         WEEK = 'week'
#         MONTH = 'month'
#
#     class KMinType(Enum):
#         #'5', '15', '30', '60'
#         FIVE = '5'
#         FIFTEEN = '15'
#         THIRTY = '30'
#         SIXTY = '60'
#
#     class FQType(Enum):
#         QFQ = 'qfq' #前复权
#         HFQ = 'hfq' #后复权
#         BFQ = ''    #不复权
#
#
#     KDAY_HEADER = ['date','open','close', 'high','low', 'volume', 'remarks', 'turnoverratio']
#     KDAY_HEADER_OUTPUT = KDAY_HEADER[0:6] + KDAY_HEADER[7:7]
#
#
#
#     def __init__(self):
#         pass
#
#
#     @classmethod
#     def _code_format(cls,code):
#         code = utils._to_str(code)
#         if code[0:3] in cls.SZ_START_CODE:
#             return "sz" + code
#
#         if code[0:2] in cls.SH_START_CODE:
#             return "sh" + code
#
#         raise SyntaxError(code)
#
#
#     @classmethod
#     def _get_url(cls, code, k_type, start_day, end_day, fq_type=FQType.QFQ):
#         url = cls.URL_FORMAT.format(code=cls._code_format(code),
#                                     k_type=k_type,
#                                     start_day=start_day,
#                                     end_day=end_day,
#                                     number=600,
#                                     fq=fq_type)
#
#         return url
#
#     @classmethod
#     def _set_df_type(cls,df):
#         col = df.columns[0]
#         df[col] = pd.to_datetime(df[col])
#         for col in df.columns[1:]:
#             df[col] = df[col].astype(float)
#
#         df = df.round(2)
#         return df
#
#
#     @classmethod
#     def _parse_response(cls,response,code,k_type,fq_type):
#         js = json.loads(response)
#         js = js['data'][cls._code_format(code)]
#         kflag = k_type
#         for key in js.keys():
#             if k_type in key:
#                 kflag = key
#                 break
#
#         df = pd.DataFrame(js[kflag],columns=cls.KDAY_HEADER)
#         df = df[cls.KDAY_HEADER_OUTPUT]
#         df = cls._set_df_type(df)
#         logging.debug(df)
#         return df
#
#     @classmethod
#     def get_k_data_by_day(cls, code, k_type=KDayType.DAY, start_day='', end_day='', fq_type=FQType.QFQ):
#         '''
#         获得K线日线级别数据
#         :param code:  股票代码
#         :param k_type: KDayType
#         :param start_day: 格式"YYYY-MM-DD"
#         :param end_day: 格式"YYYY-MM-DD"
#         :param fq_type: FQType
#         :return: dataframe
#         '''
#         logging.debug("get_k_data_by_day,code={}".format(code))
#         url = cls._get_url(code,k_type.value,start_day,end_day,fq_type.value)
#         response = HttpCache().Request(url)
#         df = cls._parse_response(response,code,k_type.value,fq_type.value)
#         return df
#
#
#
#
#
#     @classmethod
#     def get_k_data_by_min(cls,code):
#         pass
#
#
#
#
#






