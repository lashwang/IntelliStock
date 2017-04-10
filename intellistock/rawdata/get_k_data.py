#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from intellistock.http_cache import HttpCache
from lxml import etree
import StringIO
import pandas as pd

logger = logging.getLogger(__name__)


class GetKData(object):

    FHPG_URL = 'http://quotes.money.163.com/f10/fhpg_{}.html#01d05'

    def __init__(self):
        pass

    @classmethod
    def text(cls,elt):
        return elt

    @classmethod
    def get_FHPG_info(cls,code=None):
        '''
        获得分红配股信息
        '''
        if code is None:
            logger.error('the stock code is empty')
            return None

        url = cls.FHPG_URL.format(code)
        html_raw = HttpCache().Request(url)
        parser = etree.HTMLParser()
        html = etree.parse(StringIO.StringIO(html_raw),parser=parser)
        table = html.xpath("/html/body[@class='test']/div[@class='area']/div[@class='inner_box'][1]/table[@class='table_bg001 border_box limit_sale']")
        logger.debug(len(table))
        table = table[0]
        logger.debug(table)
        logger.debug(type(table))
        logger.debug(table.xpath("//thead"))





