#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc
import six
import logging
from intellistock.http_cache import HttpCache

logger = logging.getLogger(__name__)

@six.add_metaclass(abc.ABCMeta)
class StockSpiderBase(object):
    name = None

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            error = "{} must have a name".format(type(self).__name__)
            raise ValueError(error)
        self.__dict__.update(kwargs)


    @abc.abstractmethod
    def _get_start_url(self):
        return

    @abc.abstractmethod
    def _on_response(self,data):
        return

    def _start(self):
        url = self._get_start_url()
        data = HttpCache().Request(url)
        self._on_response(data)
        return





