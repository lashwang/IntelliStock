import unittest
from intellistock.trade.get_ipo_data import *
import requests

class MyTestCase(unittest.TestCase):

    def test_html_extract(self):
        url = 'http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/12/order/desc/ajax/1/'
        r = requests.get(url)
        html = BeautifulSoup(r.content, 'lxml')
        IPODataTHS2('002752')._read_html(html)


    def test_new_stock_data(self):
        ipo_data = IPOData()
        df = ipo_data.get_df()
        print df



if __name__ == '__main__':
    unittest.main()
