import unittest2
from intellistock.trade.get_ipo_data import *
import requests
from tests import *


excel_helper = None

def setUpModule():
    global excel_helper
    excel_helper = ExcelHelper(get_excel_path('test_ipo'))

def tearDownModule():
    global excel_helper
    excel_helper.close()


class MyTestCase(UnitTestBase):


    @unittest2.skip("test_html_extract skipping")
    def test_html_extract(self):
        url = 'http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/12/order/desc/ajax/1/'
        r = requests.get(url)
        with open(os.path.join(get_output_folder(),'test.html'), 'wb') as f:
            f.write(r.content)
        html = IPOData.parse_html(r.content)
        df = IPODataTHS2('002752')._read_html(html)
        print df


    def test_new_stock_data(self):
        ipo_data = IPOData(start_time='2017-01-01')
        ipo_data.load_data()
        excel_helper.add(ipo_data.df_raw,label='ipo_raw')
        excel_helper.add(ipo_data.df_broken,label='ipo_broken')
        excel_helper.add(ipo_data.df_unbroken, label='ipo_unbroken')


if __name__ == '__main__':
    unittest2.main()
