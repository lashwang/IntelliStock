import unittest
import tushare as ts
import logging
from tests import *
excel_helper = None

def setUpModule():
    global excel_helper
    excel_helper = ExcelHelper(get_excel_path('test_tushare_lib'))

def tearDownModule():
    global excel_helper
    excel_helper.close()



logger = logging.getLogger(__name__)

class MyTestCase(unittest.TestCase):
    @unittest.skip('skip')
    def test_k_data(self):
        code = stock_list[0]
        #df = ts.get_h_data(code)
        #df = ts.get_hist_data(code)
        #df = ts.get_k_data(code)
        df = ts.get_today_all()
        excel_helper.add(df,label='get_today_all')
        df = ts.get_tick_data('002868', date='2017-05-17')
        excel_helper.add(df, label='get_tick_data')
        print df


    def test_basic_info(self):
        df = ts.get_stock_basics()
        excel_helper.add(df, label='get_stock_basics')

if __name__ == '__main__':
    unittest.main()
