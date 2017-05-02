import unittest
from intellistock.trade.get_new_stock_list import *


class MyTestCase(unittest.TestCase):
    def test_new_stock_data(self):
        new_stock_list = NewStockList()
        new_stock_list.load_data()
        print new_stock_list.df


if __name__ == '__main__':
    unittest.main()
