#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from intellistock.http_cache import HttpCache

logger = logging.getLogger(__name__)


class GetKData(object):

    FHPG_URL = 'http://quotes.money.163.com/f10/fhpg_{}.html#01d05'

    def __init__(self):
        pass


    @classmethod
    def get_FHPG_info(cls,code=None):
        if code is None:
            logger.error('the stock code is empty')
            return None

        url = cls.FHPG_URL.format(code)

        html = HttpCache().Request(url)

        logger.debug(html)

