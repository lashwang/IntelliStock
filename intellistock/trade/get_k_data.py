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

class KDataReq(object):


    @property
    def code(self):
        return self.code

    @code.setter
    def code(self,code):
        self.code = code

    @property
    def day_type(self):
        return self.day_type

    @day_type.setter
    def day_type(self,day_type):
        self.day_type = day_type

    @property
    def fq_type(self):
        return self.fq_type

    @fq_type.setter
    def fq_type(self,fq_type):
        self.fq_type = fq_type


    @property
    def date_from(self):
        return self.date_from

    @date_from.setter
    def date_from(self,date_from = None):
        if date_from is None:
            date_from = '2014-01-01'

        self.date_from = date_from

        if is_date_format_invalid(date_from):
            raise ValueError(date_from)

    @property
    def date_to(self):
        return self.date_to

    @date_to.setter
    def date_to(self,date_to=None):
        if date_to is None:
            now = arrow.now()
            if now.hour >= 16:
                data_to = now.format('YYYY-MM-DD')
            else:
                data_to = now.replace(days=-1).format('YYYY-MM-DD')

        self.date_to = data_to

        if is_date_format_invalid(data_to):
            raise ValueError(data_to)





class KData(object):
    def __init__(self,k_date_req):
        self.k_date_req = k_date_req








@six.add_metaclass(abc.ABCMeta)
class KDataByDayBase(SpiderBase):


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

    @abc.abstractmethod
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

    def _on_parse_finished(self):
        df = self.df



        self.df = df



    def __str__(self):
        str_format = "ifeng-{code}-{day_type}-{fq_type}"
        return str_format.format(code=self.code,
                                 day_type=self.cls.DAY_TYPE[self.day_type.value],
                                 fq_type=self.day_type.value)


class KDataFromQQ(KDataByDayBase):
    URL_FORMAT = "http://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get?p=1&" \
                 "param={code},{k_type},{start_day},{end_day},800,{fq}"
    DAY_TYPE = ['day', 'week', 'month']
    FQ_TYPE = ['qfq','hfq', '']
    HEADER = ['date','open','close','high','low','volume','remarks','turnover']


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
                                            fq=cls.FQ_TYPE[self.fq_type.value])

    def _format(self,df):
        df.columns = self.cls.HEADER
        df.drop('remarks',axis=1, inplace=True)
        df['code'] = self.code
        df = df.set_index(['date','code'])
        df = df.apply(pd.to_numeric)
        df['change'] = df['close'].diff(1)
        return df

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
        df = self._format(df)
        self.df = self.df.append(df)


    def _on_parse_finished(self):
        pass


    def __str__(self):
        str_format = "qq-{code}-{day_type}-{fq_type}"
        return str_format.format(code=self.code,
                                 day_type=self.cls.DAY_TYPE[self.day_type.value],
                                 fq_type=self.cls.FQ_TYPE[self.day_type.value])








