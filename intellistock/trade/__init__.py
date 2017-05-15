#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc
import six
import logging
from intellistock.http_cache import HttpCache
from bs4 import BeautifulSoup
import inspect
import pandas as pd
import sys


logger = logging.getLogger(__name__)


def logging_config():
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)



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
        self.cls = self.__class__
        self.started = False
        self._cache = True
        self._cache_timeout_min = None
        self.df = pd.DataFrame()

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


    @abc.abstractmethod
    def _on_parse_finished(self):
        pass

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self,value):
        self._cache = value

    @property
    def cache_timeout(self):
        return self._cache_timeout_min


    @cache_timeout.setter
    def cache_timeout(self,value):
        self._cache_timeout_min = value

    @run_once
    def load_data(self):
        pass

    def _start(self):
        logger.debug("_start,cache={},cache_timeout={}".format(self._cache, self._cache_timeout_min))
        url = self._get_start_url()
        self.start_url = url
        for url in self._request(url):
            logger.debug(url)

        self.started = True
        return

    def _request(self,url):
        logger.debug("Call request, url:{}".format(url))
        while True:
            self.current_url = url
            data = HttpCache().Request(url, self._cache, self._cache_timeout_min)
            url = self._parse(data)
            if url is not None:
                logger.debug("looping to the next url:{}".format(url))
                yield url
            else:
                logger.debug("no further page need to parse!!")
                self._on_parse_finished()
                return

    def get_df(self):
        return self.df


@six.add_metaclass(abc.ABCMeta)
class TimeSequenceData(object):
    @abc.abstractmethod
    def get_time_from(self):
        pass

    @abc.abstractmethod
    def get_time_to(self):
        pass

    def get_time_interval(self):
        pass
