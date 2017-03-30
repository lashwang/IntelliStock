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
    def http_cache_index_insert(cls,table_='http_cache',url_ = None):
        table = Database.db[table_]
        table.insert(dict(url=url_,time=datetime.datetime.now()))

        print Database.db[table_].all()




