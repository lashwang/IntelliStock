#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
import base64
import config as cf
import file_utils
from data_base import DataBase
import logging
import requests

logger = logging.getLogger(__name__)



class HttpCache(object):

    HTTP_CACHE_INDEX_TABLE = 'cache_index'


    def __init__(self):
        file_utils.mkdir(self._get_cache_folder())


    def _get_cache_folder(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        ROOT_DIR = os.path.dirname(ROOT_DIR)
        return os.path.join(ROOT_DIR,cf.CACHE_FOLDER)

    def Request(self, url_, from_cache = True, cache_timeout_minute = None):
        logger.debug('HttpCache, url is ' + url_)
        if from_cache:
            data = self._load_from_cache(url_, cache_timeout_minute)
        else:
            data = None

        if data is not None:
            logger.debug('load from cache,cache name is {}'.format(self._url_to_filename(url_)))
            return data

        try:
            # request = Request(url_)
            # data = urlopen(request, timeout=10).read()
            r = requests.get(url_)
            data = r.content
            self._save_to_cache(data,url_)
            self._save_index_file(url_)
        except Exception, error:
            logger.error(str(error))
            return None

        return data

    def _save_to_cache(self,data_,url_):
        cache_path = os.path.join(self._get_cache_folder(),self._url_to_filename(url_))
        logger.debug(cache_path)

        with open(cache_path, 'wb') as f:
            f.write(data_)



    def _load_from_cache(self,url_,cache_timeout_):
        filename = self._url_to_filename(url_)
        data = None
        index = self._load_index_file(url_)
        logger.debug(index)

        if index:
            if self._is_cache_valid(index,cache_timeout_):
                try:
                    with open(os.path.join(self._get_cache_folder(),filename),'r') as f:
                        data = f.read()
                except Exception,error:
                    logger.error(str(error))
                    return data

        return data

    def _is_cache_valid(self,index_,cache_timeout_):
        if cache_timeout_ is None:
            cache_timeout_ = cf.DEFAULT_CACHE_TIME_OUT_MIN

        time = index_['time'] + datetime.timedelta(minutes=cache_timeout_)
        now = datetime.datetime.now()
        valid = (now < time)
        logger.debug("_is_cache_valid:{}".format(valid))
        return valid


    def _url_to_filename(self,url_):
        return base64.b32encode(url_)

    def _save_index_file(self,url_):
        self.http_cache_index_upsert(url_)


    def _load_index_file(self,url_):
        if url_ is None:
            raise ValueError
        db = DataBase.get_db_connection()

        index = db[HttpCache.HTTP_CACHE_INDEX_TABLE].find_one(url=url_)

        return index



    def http_cache_index_upsert(self,url_ = None):
        if url_ is None:
            raise ValueError
        db = DataBase.get_db_connection()
        try:
            with db:
                table = db[HttpCache.HTTP_CACHE_INDEX_TABLE]
                table.upsert(dict(url=url_,time=datetime.datetime.now()),['url'])
        except Exception,error:
            logger.error(str(error))



