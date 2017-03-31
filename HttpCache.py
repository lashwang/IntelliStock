#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import datetime
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
import base64
import Configuration as cf
import FileUtils
from DataBase import Database



class HttpCache:

    HTTP_CACHE_INDEX_TABLE = 'cache_index'

    def __init__(self):
        FileUtils.mkdir(cf.CACHE_FOLDER)

    def Request(self,url_,from_cache_ = True):
        print 'HttpCache, url is ' + url_
        if from_cache_:
            data = self._load_from_cache(url_)
        else:
            data = None

        if data is not None:
            print 'load from cache'
            return data

        try:
            request = Request(url_)
            data = urlopen(request, timeout=10).read()
            self._save_to_cache(data,url_)
            self._save_index_file(url_)
        except Exception, error:
            print str(error)
            return None

        return data

    def _save_to_cache(self,data_,url_):
        cache_path = os.path.join(cf.CACHE_FOLDER,self._url_to_filename(url_))
        print cache_path

        with open(cache_path, 'wb') as f:
            f.write(data_)



    def _load_from_cache(self,url_):
        filename = self._url_to_filename(url_)
        data = None
        index = self._load_index_file(url_)
        print index

        if index:
            if self._is_cache_valid(index):
                try:
                    with open(os.path.join(cf.CACHE_FOLDER,filename),'r') as f:
                        data = f.read()
                except Exception,error:
                    print str(error)
                    return data

        return data

    def _is_cache_valid(self,index_):
        time = index_['time'] + datetime.timedelta(minutes=cf.CACHE_TIME_OUT_MIN)
        now = datetime.datetime.now()
        print time,now

        return (now < time)


    def _url_to_filename(self,url_):
        return base64.b32encode(url_)

    def _save_index_file(self,url_):
        self.http_cache_index_upsert(url_)


    def _load_index_file(self,url_):
        if url_ is None:
            raise RuntimeError
        db = Database.get_db_connection()

        index = db[HttpCache.HTTP_CACHE_INDEX_TABLE].find_one(url=url_)

        return index



    def http_cache_index_upsert(self,url_ = None):
        if url_ is None:
            raise RuntimeError
        db = Database.get_db_connection()
        try:
            with db:
                table = db[HttpCache.HTTP_CACHE_INDEX_TABLE]
                table.upsert(dict(url=url_,time=datetime.datetime.now()),['url'])
        except Exception,error:
            print str(error)



