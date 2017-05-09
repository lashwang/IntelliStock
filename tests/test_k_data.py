#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest2
from intellistock.trade.get_k_data import *
from tests import *
import pandas as pd
from intellistock.excel_helper import ExcelHelper

test_case_list = merge_test_case()

excel_helper = None

def setUpModule():
    global excel_helper
    excel_helper = ExcelHelper(get_excel_path('test_stock'))

def tearDownModule():
    global excel_helper
    excel_helper.close()

class TestKDataBase(object):
    def test_data(self,cls):
        for test_case in test_case_list:
            try:
                kdata_object = cls(code=test_case[0],day_type=test_case[1],fq_type=test_case[2])
                df = kdata_object.load_k_data()
                #print test_case,len(df)
                self.assertFalse(len(df) < 1)
                excel_helper.add(df,label=str(kdata_object))
            except Exception,error:
                print error


class TestKDataFromIFeng(UnitTestBase,TestKDataBase):
    def test_data(self):
        super(TestKDataFromIFeng,self).test_data(KDataFromIFeng)


class TestKDataFromQQ(UnitTestBase,TestKDataBase):
    def test_data(self):
        super(TestKDataFromQQ,self).test_data(KDataFromQQ)




if __name__ == '__main__':
    unittest2.main()
