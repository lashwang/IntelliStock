#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from intellistock.trade.get_k_data import *
import itertools
import os
from intellistock import file_utils
from intellistock.data_base import DBBase
import sys
import unittest


logger = logging.getLogger(__name__)


date_list = ["2015-06-10","2016-06-10","2017-06-10"]
stock_list = ['000002','300619','300414', '600519', '002839', '603039']
fq_type_list = list(FQType)
day_type_list = list(KDayType)


DBBase.DB_IN_TEST = True

def merge_test_case():
    return list(itertools.product(stock_list,day_type_list,fq_type_list))


def get_output_folder():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ROOT_DIR,'output')

file_utils.mkdir(get_output_folder())


def save_to_excel(df,file,label):
    handler =  pd.ExcelWriter(os.path.join(get_output_folder(),file), engine='xlsxwriter')
    df.to_excel(handler, sheet_name=label)
    handler.save()


class UnitTestBase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(UnitTestBase, self).__init__(methodName)
        os.environ["UNITTEST"] = str(True)