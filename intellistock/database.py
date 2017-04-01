#!/usr/bin/python
# -*- coding: utf-8 -*-

import dataset

import config as cf
import file_utils
import logging
logger = logging.getLogger(__name__)



class DataBase(object):
    file_utils.mkdir(cf.STOCK_DB_FOLDER)
    db = dataset.connect('sqlite:///{}'.format(cf.STOCK_DB_PATH))

    @classmethod
    def get_db_connection(cls):
        return DataBase.db






