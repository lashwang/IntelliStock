import unittest
import tushare as ts
import logging


logger = logging.getLogger(__name__)

class MyTestCase(unittest.TestCase):
    stock_list = ['000002', '300619', '300414', '600519', '002839', '603039']


    def test_something(self):
        self.assertEqual(True, True)

    def test_k_data(self):
        code = self.__class__.stock_list[0]
        df = ts.get_h_data(code)
        logging.debug(df)

        df = ts.get_hist_data(code)
        logging.debug(df)

        self.assertEqual(True, True)




if __name__ == '__main__':
    unittest.main()
