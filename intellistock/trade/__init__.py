#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc
import six
import logging
from intellistock.http_cache import HttpCache
from bs4 import BeautifulSoup



logger = logging.getLogger(__name__)


def run(fun):
    def wrapper(self, *args, **kwargs):
        self._start()
        return fun(self, *args, **kwargs)

    return wrapper


@six.add_metaclass(abc.ABCMeta)
class SpiderBase(object):
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
        logger.debug("_start")
        url = self._get_start_url()
        data = HttpCache().Request(url)
        self._on_response(data)
        return






@six.add_metaclass(abc.ABCMeta)
class HTMLStockSpider(SpiderBase):
    def __init__(self,**kwargs):
        super(HTMLStockSpider,self).__init__(**kwargs)

    def _on_response(self, html):
        soup = BeautifulSoup(html, "lxml")
        self._on_html_response(soup)

    @abc.abstractmethod
    def _get_start_url(self):
        return

    @abc.abstractmethod
    def _on_html_response(self, soup):
        return

