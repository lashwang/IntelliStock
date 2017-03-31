#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import logging
logger = logging.getLogger(__name__)


def mkdir(dir_):
    if dir_ and not os.path.exists(dir_):
        try:
            os.makedirs(dir_)
        except Exception, error:
            logger.error(str(error))

