#!/usr/bin/python
# -*- coding: utf-8 -*-

import dataset

import Configuration as cf
import FileUtils


class DataBase:
    FileUtils.mkdir(cf.STOCK_DB_FOLDER)
    db = dataset.connect('sqlite:///{}'.format(cf.STOCK_DB_PATH))

    @classmethod
    def get_db_connection(cls):
        return DataBase.db






