#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

def mkdir(dir_):
    try:
        os.mkdir(dir_)
    except Exception, error:
        print str(error)

