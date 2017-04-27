#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from intellistock.trade.get_k_data import *
from tests import *
import pandas as pd


test_case_list = merge_test_case()

class TestKDataFromIFeng(unittest.TestCase):
    

    for test_case in test_case_list:
        try:
            kdata_ifeng = KDataFromIFeng(code=test_case[0],day_type=test_case[1],fq_type=test_case[2])
            kdata_ifeng.load_k_data()
        except ValueError,error:
            pass


class TestKDataFromQQ(unittest.TestCase):
    for test_case in test_case_list:
        try:
            kdata_qq = KDataFromQQ(code=test_case[0],day_type=test_case[1],fq_type=test_case[2])
            kdata_qq.load_k_data()
        except pd.PandasError,error:
            pass




if __name__ == '__main__':
    unittest.main()
