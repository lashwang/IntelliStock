import unittest
from intellistock.trade.get_ipo_data import *


class MyTestCase(unittest.TestCase):
    def test_new_stock_data(self):
        ipo_data = IPOData()
        ipo_data.load_data()

        print ipo_data.get_df()


if __name__ == '__main__':
    unittest.main()
