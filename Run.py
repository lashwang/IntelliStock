#!/usr/bin/python
# -*- coding: utf-8 -*-


import fire

from intellistock.StockReport import StockReport


def main():
    fire.Fire(StockReport)


if __name__ == "__main__":
    main()