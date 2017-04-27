#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from intellistock.trade.get_k_data import *
import test_case


class TestKData(unittest.TestCase):
    kdata_ifeng = KDataFromIFeng(test_case.stock_list[0])
    kdata_ifeng.load_k_data()

    kdata_qq = KDataFromQQ(test_case.stock_list[0])
    kdata_qq.load_k_data()


    pass



if __name__ == '__main__':
    unittest.main()
