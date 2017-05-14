#!/usr/bin/python
# -*- coding: utf-8 -*-


import fire
from intellistock.stock_report import StockReport
import logging
import sys
from intellistock.data_wrapper import DataWrapper as dw
from intellistock.trade import *


def main():
    logging_config()
    fire.Fire(dw)


if __name__ == "__main__":
    main()