#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import os

class ExcelHelper(object):
    def __init__(self,excel_path=None):
        filename, file_extension = os.path.splitext(excel_path)
        if file_extension is not "xlsx":
            excel_path = excel_path + ".xlsx"
        self.handler = pd.ExcelWriter(excel_path, engine='openpyxl')

    def add(self,df,label):
        df.to_excel(self.handler, sheet_name=label)


    def close(self):
        self.handler.save()