#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from datetime import date,datetime

def now_date():
    today = date.today()
    return today.strftime("%m-%d")


def now_datetime():
    today = datetime.now()
    return today.strftime("%m-%d %H:%M:%S")