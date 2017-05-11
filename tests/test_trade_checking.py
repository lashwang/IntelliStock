import unittest2
from intellistock.trade.trade_checking import StockCalDay
import arrow



def is_week_end(a):
    return (a.weekday() == 5 or a.weekday() == 6)

class MyTestCase(unittest2.TestCase):
    def test_cal_day(self):
        stock_cal_day = StockCalDay()
        stock_cal_day.load_data()

        cal_list = stock_cal_day.get_cal_list()
        self.assertTrue(len(cal_list) >= 13)

        a = arrow.get('2017-01-01', 'YYYY-MM-DD')
        while True:
            if_trade_day = stock_cal_day.check_trading_day(a.format('YYYY-MM-DD'))
            last_trade_day = stock_cal_day.get_last_trading_day(a.format('YYYY-MM-DD'))
            if is_week_end(a):
                self.assertEqual(True,not if_trade_day,str(a))

            self.assertEqual(is_week_end(last_trade_day),False,last_trade_day)
            a = a.replace(days=+1)
            if a.year > 2017:
                break


    def test_arrow(self):
        try:
            a = arrow.get('2017-0101', 'YYYY-MM-DD')
        except Exception,error:
            print error

if __name__ == '__main__':
    unittest2.main()
