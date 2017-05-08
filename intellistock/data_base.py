#!/usr/bin/python
# -*- coding: utf-8 -*-

import dataset
import abc
import six
import config as cf
import file_utils
import logging
import os
import config as cf


logger = logging.getLogger(__name__)

@six.add_metaclass(abc.ABCMeta)
class DBBase(object):
    DB_FOLDER = os.path.join(cf.EXPORT_PATH_DIR, 'db')

    def __new__(cls):
        file_utils.mkdir(cls._get_db_folder())
        return super(DBBase, cls).__new__(cls)

    @classmethod
    def _get_db_folder(cls):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(root_dir)
        return os.path.join(root_dir,DBBase.DB_FOLDER)



    def __init__(self,table_name):
        self.cls = self.__class__
        _db_path = os.path.join(self.cls._get_db_folder(), 'stock_data.db')
        self.db_conn = dataset.connect('sqlite:///{}'.format(_db_path))
        self.table_name = table_name


    def get_db_connection(self):
        return self.db_conn

    def get_db_table(self):
        return self.db_conn[self.table_name]



class DataBase(object):
    file_utils.mkdir(cf.STOCK_DB_FOLDER)
    db = dataset.connect('sqlite:///{}'.format(cf.STOCK_DB_PATH))

    @classmethod
    def get_db_connection(cls):
        return DataBase.db






