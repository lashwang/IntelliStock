#!/usr/bin/python
# -*- coding: utf-8 -*-

import tushare as ts

from intellistock.trade.get_basic_info import *
from intellistock.trade.get_new_stock_list import *
from intellistock.trade.trade_checking import *

logger = logging.getLogger(__name__)




class DataWrapper:

    def interface_test(self):

        # date_list = ["2015-06-10","2016-06-10","2017-06-10"]
        # for date in date_list:
        #     # isTradingDay = StockCalDay(date).is_trading_day()
        #     # isTradingTime = StockTradeTime().is_trading_time()
        #     # logger.debug("isTradingDay:{},isTradingTime:{}".format(isTradingDay, isTradingTime))

        # stock_list = ['000002','300619','300414', '600519', '002839', '603039']
        # for _code in stock_list:
        #     StockDivInfo(_code).get_df()
        #     StockStructureInfo(_code).get_df()
        #     pass

        #NewStockList().load_data()
        df = ts.get_hist_data('300414')
        logger.debug(df)

        #
        # for _code in stock_list:
        #     start_day = "2016-04-08"
        #     end_day = arrow.now().format("YYYY-MM-DD")
        #     GetKData.get_k_data_by_day(code=_code,k_type=GetKData.KDayType.DAY,
        #                                start_day=start_day, end_day=end_day,fq_type=GetKData.FQType.QFQ)
        #





