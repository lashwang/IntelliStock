import unittest
from intellistock.http_cache import HttpCache



class HttpCacheTestCase(unittest.TestCase):

    def test_http_cache(self):
        http_cache = HttpCache()
        data = http_cache.Request('http://stock.qq.com/stock/xingu/')

        print data




if __name__ == '__main__':
    unittest.main()
