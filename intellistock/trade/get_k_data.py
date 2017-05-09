#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

import pandas as pd
from enum import Enum

from utils import *
from intellistock.trade import *

logger = logging.getLogger(__name__)


'''
1. 从凤凰网获得股票数据
2. 修正数据
3. 从腾讯网获取数据
4. 比较
'''


class KDayType(Enum):
    DAY = 0
    WEEK = 1
    MONTH = 2

class FQType(Enum):
    '''
    QFQ - 前复权
    HFQ - 后复权
    NFQ - 不复权
    '''
    QFQ = 0
    HFQ = 1
    NFQ = 2

@six.add_metaclass(abc.ABCMeta)
class KDataByDayBase(SpiderBase,TimeSequenceData):


    def __init__(self,code = '',
                 day_type = KDayType.DAY,
                 fq_type = FQType.QFQ,
                 date_from = None,
                 date_to = None,
                 **kwargs):
        '''
        
        :param code:  字符类型,
        :param day_type: KDayType
        :param fq_type: FQType
        :param date_from: 'YYYY-MM-DD'
        :param date_to: 'YYYY-MM-DD'
        :param kwargs: 
        '''
        name = self.__class__.__name__
        super(KDataByDayBase, self).__init__(name, **kwargs)
        self.code = code
        self.day_type = day_type
        self.fq_type = fq_type
        self.date_from = date_from
        self.date_to = date_to
        self.code_format = code_format(code)


    def _get_start_url(self):
        return self._get_url()

    def _parse(self, data):
        return self._on_parse(data)


    @abc.abstractmethod
    def _on_parse(self, data):
        pass

    @abc.abstractmethod
    def _get_url(self):
        pass

    @run_once
    def load_k_data(self):
        return self.df
    def get_time_from(self):
        super(KDataByDayBase, self).get_time_from()

    def get_time_to(self):
        super(KDataByDayBase, self).get_time_to()

    def _on_parse_finished(self):
        pass


class KDataFromIFeng(KDataByDayBase):
    '''
    http://api.finance.ifeng.com/akdaily/?code=sz000002&type=last
    http://api.finance.ifeng.com/akweekly/?code=sz000002&type=last
    http://api.finance.ifeng.com/akmonthly/?code=sz000002&type=last
    '''
    URL = 'http://api.finance.ifeng.com/{}/?code={}&type=last'
    DAY_TYPE = ['akdaily','akweekly','akmonthly']
    DAY_PRICE_COLUMNS = ['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change',
                         'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20']

    def __init__(self, code='', day_type=KDayType.DAY, fq_type=FQType.QFQ, date_from='', date_to='', **kwargs):
        if fq_type != FQType.QFQ:
            raise ValueError('The ifeng only support QFQ mode!!!')
        super(KDataFromIFeng, self).__init__(code, day_type, fq_type, date_from, date_to, **kwargs)

    def _get_url(self):
        cls = self.cls
        return cls.URL.format(cls.DAY_TYPE[self.day_type.value], self.code_format)

    def _on_parse(self, data):
        js = json.loads(data)
        js = js['record']
        df = pd.DataFrame(js,columns=self.cls.DAY_PRICE_COLUMNS)
        self.df = self.df.append(df)

class KDataFromQQ(KDataByDayBase):
    URL_FORMAT = "http://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get?p=1&param={code},{k_type},{start_day},{end_day},{number},{fq}"

    DAY_TYPE = ['day', 'week', 'month']

    FQ_TYPE = ['qfq','hfq', '']

    def __init__(self, code='', day_type=KDayType.DAY, fq_type=FQType.QFQ, date_from='', date_to='', **kwargs):
        super(KDataFromQQ, self).__init__(code, day_type, fq_type, date_from, date_to, **kwargs)
        self.day_str = self.cls.DAY_TYPE[self.day_type.value]
        self.fq_str = self.cls.FQ_TYPE[self.fq_type.value]

    def _get_url(self):
        cls = self.cls
        return cls.URL_FORMAT.format(code=self.code_format,
                                            k_type=cls.DAY_TYPE[self.day_type.value],
                                            start_day=self.date_from,
                                            end_day=self.date_to,
                                            number=600,
                                            fq=cls.FQ_TYPE[self.fq_type.value])

    def _on_parse(self, data):
        js = json.loads(data)
        '''
        <type 'list'>: [u'version', u'prec', u'qt', u'qfqday', u'mx_price']
        '''
        js = js['data'][self.code_format]

        keys = js.keys()

        key = [x for x in keys if self.day_str in x]

        if len(key) != 1:
            raise ValueError("unknow response")


        js = js[key[0]]

        df = pd.DataFrame(js)

        self.df = self.df.append(df)

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






