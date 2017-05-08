#!/usr/bin/python
# -*- coding: utf-8 -*-
import os


def check_unit_test():
    test = bool(os.environ.get("UNITTEST", str(False)))

    return test