#!/usr/bin/python
# -*- coding: utf-8 -*-

import Configuration as cf
import dataset
import FileUtils
import datetime


class Database:
    FileUtils.mkdir(cf.STOCK_DB_FOLDER)
    db = dataset.connect('sqlite:///{}'.format(cf.STOCK_DB_PATH))

    @classmethod
    def get_db_connection(cls):
        return Database.db






