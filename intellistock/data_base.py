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
from intellistock import *

logger = logging.getLogger(__name__)

@six.add_metaclass(abc.ABCMeta)
class DBBase(object):
    DB_FOLDER = os.path.join(cf.EXPORT_PATH_DIR, 'db')
    DB_FILE_NAME = 'stock_data.db'



    def __init__(self,table_name):
        self.cls = self.__class__
        file_utils.mkdir(self._get_db_folder())
        db_file_name = self.cls.DB_FILE_NAME if not check_unit_test() else 'stock_data_test.db'
        _db_path = os.path.join(self._get_db_folder(), db_file_name)
        self.db_conn = dataset.connect('sqlite:///{}'.format(_db_path))
        self.table_name = table_name

    def _get_db_folder(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(root_dir)
        return os.path.join(root_dir,DBBase.DB_FOLDER)

    def get_db_connection(self):
        return self.db_conn

    def get_db_table(self):
        return self.db_conn[self.table_name]


    def upset(self,row, keys):
        try:
            with self.db_conn:
                table = self.db_conn[self.table_name]
                table.upsert(row,keys)
        except Exception,error:
            logger.error(str(error))






