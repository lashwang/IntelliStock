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
        self._start(*args, **kwargs)
        return fun(self, *args, **kwargs)

    return wrapper


def run_once(fun):
    def wrapper(self, *args, **kwargs):
        if not self.started:
            self._start(*args, **kwargs)
        return fun(self, *args, **kwargs)

    return wrapper


@six.add_metaclass(abc.ABCMeta)
class SpiderBase(object):
    name = None


    def __init__(self, name = None,**kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            error = "{} must have a name".format(type(self).__name__)
            raise ValueError(error)

        self.__dict__.update(kwargs)

        self.started = False
        self.cache = True
        self.cache_timeout = None


    @abc.abstractmethod
    def _get_start_url(self):
        return

    @abc.abstractmethod
    def _on_response(self,data):
        return

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self,value):
        self._cache = value

    @property
    def cache_timeout(self):
        return self._cache_timeout


    @cache_timeout.setter
    def cache_timeout(self,value):
        self._cache_timeout = value

    def _start(self):
        logger.debug("_start,cache={},cache_timeout={}".format(self._cache,self._cache_timeout))
        url = self._get_start_url()
        data = HttpCache().Request(url,self._cache,self._cache_timeout)
        self._on_response(data)
        self.started = True
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

