#!/usr/bin/python
# -*- coding: utf-8 -*-

import dataset

import Configuration as cf
import FileUtils
import logging
logger = logging.getLogger(__name__)



class DataBase(object):
    FileUtils.mkdir(cf.STOCK_DB_FOLDER)
    db = dataset.connect('sqlite:///{}'.format(cf.STOCK_DB_PATH))

    @classmethod
    def get_db_connection(cls):
        return DataBase.db






