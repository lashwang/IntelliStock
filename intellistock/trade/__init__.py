#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc
import six
import logging
from intellistock.http_cache import HttpCache
from bs4 import BeautifulSoup
import inspect


logger = logging.getLogger(__name__)


def run(fun):
    def wrapper(self, *args, **kwargs):
        logger.debug("run:{}".format(fun))
        self._start(*args, **kwargs)
        return fun(self, *args, **kwargs)

    return wrapper


def run_once(fun):
    def wrapper(self, *args, **kwargs):
        logger.debug("run_once:{}".format(fun))
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
        self._cache = True
        self._cache_timeout = None
        self.cls = object.__name__

    @abc.abstractmethod
    def _get_start_url(self):
        pass

    @abc.abstractmethod
    def _parse(self, data):
        '''
        Paser http response data(str or unicode)
        :param data: 
        :return:If need to parse next page, then return next page url, else return None  
        '''
        pass

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
        for url in self._request(url):
            logger.debug(url)

        self.started = True
        return

    def _request(self,url):
        logger.debug("Call request, url:{}".format(url))
        while True:
            data = HttpCache().Request(url, self._cache, self._cache_timeout)
            url = self._parse(data)
            if url is not None:
                logger.debug("looping to the next url:{}".format(url))
                yield url
            else:
                logger.debug("no further page need to parse!!")
                return



