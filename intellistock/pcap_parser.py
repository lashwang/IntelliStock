#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import dpkt


logger = logging.getLogger(__name__)



class Http(object):
    def __init__(self,request,request_ts,response,response_ts):
        self.request = request
        self.request_ts = request_ts
        self.response = response
        self.response_ts = response_ts






class Connection(object):
    def __init__(self):
        self.is_syn = 1
        self.reqest_fin = False
        self.response_fin = False
        self.conn_addr = None

    @staticmethod
    def parse_http_connection(filename):
        for ts, pkt in dpkt.pcap.Reader(open(filename, 'rb')):
            eth = dpkt.ethernet.Ethernet(pkt)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                continue
            ip = eth.data
            if not isinstance(ip.data, dpkt.tcp.TCP):
                continue

class HttpConnection(Connection):
    def __init__(self):
        super(Connection,self).__init__()
        self.http = list()