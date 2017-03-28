#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import datetime
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
import base64
import json
import configuration as cf



class HttpCache:



    def __init__(self):
        try:
            os.mkdir(cf.CACHE_FOLDER)
        except Exception, error:
            print str(error)

        self.index = self._load_index_file()

    def Request(self,url_,from_cache_ = True):
        print 'HttpCache, url is ' + url_
        data = self._load_from_cache(url_)

        if data is not None:
            print 'load from cache'
            return data

        try:
            request = Request(url_)
            data = urlopen(request, timeout=10).read()
            self._save_to_cache(data,url_)
            self.index[self._url_to_filename(url_)] = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            self._save_index_file()
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

        if self.index.has_key(filename):
            try:
                with open(os.path.join(cf.CACHE_FOLDER,filename),'r') as f:
                    data = f.read()
            except Exception,error:
                print str(error)

        return data


    def _url_to_filename(self,url_):
        return base64.b32encode(url_)


    def _load_index_file(self):
        try:
            with open(cf.CACHE_INDEX_FILE,'r') as data_file:
                index = json.load(data_file)
        except Exception,error:
            index = dict()
            print str(error)

        return index

    def _save_index_file(self):
        try:
            with open(cf.CACHE_INDEX_FILE,'w') as data_file:
                json.dump(self.index,data_file,indent=4, sort_keys=True)

        except Exception, error:
            print str(error)

