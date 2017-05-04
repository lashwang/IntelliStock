import unittest
from intellistock.trade.get_ipo_data import *
import requests
from tests import *


class MyTestCase(unittest.TestCase):

    def test_html_extract(self):
        url = 'http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/12/order/desc/ajax/1/'
        r = requests.get(url)
        with open(os.path.join(get_output_folder(),'test.html'), 'wb') as f:
            f.write(r.content)
        html = BeautifulSoup(markup=r.content, features='lxml',from_encoding='GBK')
        df = IPODataTHS2('002752')._read_html(html)
        print df


    def test_new_stock_data(self):
        ipo_data = IPOData(start_time='2017-01-01')
        df = ipo_data.get_df()
        print df



if __name__ == '__main__':
    unittest.main()
