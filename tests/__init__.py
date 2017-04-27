#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from intellistock.trade.get_k_data import *
import itertools

logger = logging.getLogger(__name__)


date_list = ["2015-06-10","2016-06-10","2017-06-10"]
stock_list = ['000002','300619','300414', '600519', '002839', '603039']
fq_type_list = list(FQType)
day_type_list = list(KDayType)


def merge_test_case():
    return list(itertools.product(stock_list,day_type_list,fq_type_list))