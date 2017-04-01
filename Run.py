#!/usr/bin/python
# -*- coding: utf-8 -*-


import fire
from intellistock.stock_report import StockReport
import logging
import sys
from intellistock.data_wrapper import DataWrapper as dw


def logging_config():
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

def main():
    logging_config()
    fire.Fire(dw)


if __name__ == "__main__":
    main()