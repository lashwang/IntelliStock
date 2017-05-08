import unittest
from intellistock.http_cache import HttpCache
from tests import UnitTestBase


class HttpCacheTestCase(UnitTestBase):


    def __init__(self, methodName='runTest'):
        super(HttpCacheTestCase, self).__init__(methodName)

    def test_http_cache(self):
        http_cache = HttpCache()
        data = http_cache.Request('http://stock.qq.com/stock/xingu/')

        print data




if __name__ == '__main__':
    unittest.main()
