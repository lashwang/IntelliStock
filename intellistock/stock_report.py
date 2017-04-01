#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import time

import pandas as pd

import config as cf, mail
import logging
import file_utils
from data_analyser import DataAnylyser as da
from data_wrapper import DataWrapper as dw


logger = logging.getLogger(__name__)

class StockReport(object):

    def __init__(self):
        file_utils.mkdir(cf.EXPORT_PATH_DIR)
        self.writer = pd.ExcelWriter(cf.EXPORT_XLS_FILE_PATH, engine='xlsxwriter')

    def send_mail(self,files=None):
        mail_ = mail.Mail()
        mail_.send_email(files)




    def generate_xingu_report(self):
        data = da()._analyse_xingu_report()

        data.to_excel(self.writer, sheet_name=u'次新股')
        self.writer.save()
        return os.path.abspath(cf.EXPORT_XLS_FILE_PATH)


    def check_is_trading(self):
        dw().check_is_trading()

    def run(self):
        export_xls_path = self.generate_xingu_report()
        f = [export_xls_path]
        self.send_mail(f)