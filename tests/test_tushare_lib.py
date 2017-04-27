import unittest
import tushare as ts
import logging
import test_case

logger = logging.getLogger(__name__)

class MyTestCase(unittest.TestCase):
    stock_list = test_case.stock_list


    def test_something(self):
        self.assertEqual(True, True)

    def test_k_data(self):
        code = self.__class__.stock_list[0]
        df = ts.get_h_data(code)

        '''
        凤凰网后复权数据(最近三年)
        http://api.finance.ifeng.com/akdaily/?code=sz000002&type=last
        http://api.finance.ifeng.com/akweekly/?code=sz000002&type=last
        http://api.finance.ifeng.com/akmonthly/?code=sz000002&type=last
        '''
        df = ts.get_hist_data(code)


        df = ts.get_k_data(code)


        self.assertEqual(True, True)




if __name__ == '__main__':
    unittest.main()
