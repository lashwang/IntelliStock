#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import dpkt
import socket

logger = logging.getLogger(__name__)



class Http(object):
    def __init__(self,request,request_ts,response,response_ts):
        self.request = request
        self.request_ts = request_ts
        self.response = response
        self.response_ts = response_ts



class TcpConnTrack(object):
    def __init__(self):
        self.conn = dict()

        pass

    def is_fin_flag(self,tcp):
        fin_flag = (tcp.flags & dpkt.tcp.TH_FIN) != 0
        return fin_flag

    def is_syn_flag(self,tcp):
        syn_flag = (tcp.flags & dpkt.tcp.TH_SYN) != 0
        return syn_flag

    def is_rst_flag(self,tcp):
        rst_flag = (tcp.flags & dpkt.tcp.TH_RST) != 0
        return rst_flag

    def is_ack_flag(self,tcp):
        ack_flag = (tcp.flags & dpkt.tcp.TH_ACK) != 0
        return ack_flag


    def parse_http_from_file(self,filename):
        for ts, pkt in dpkt.pcap.Reader(open(filename, 'rb')):
            eth = dpkt.ethernet.Ethernet(pkt)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                continue
            ip = eth.data
            if not isinstance(ip.data, dpkt.tcp.TCP):
                continue

            tcp = ip.data
            saddr = socket.inet_ntoa(ip.src)
            sport = tcp.sport
            daddr = socket.inet_ntoa(ip.dst)
            dport = tcp.dport
            from_app_tag = (saddr, sport, daddr, dport)
            from_server_tag = (daddr, dport,saddr, sport)
            conn_key = None
            is_from_app = False
            is_from_server = False



            if from_app_tag in self.conn:
                is_from_app = True
                conn_key = from_app_tag
            elif from_server_tag in self.conn:
                is_from_server = True
                conn_key = from_server_tag

            if self.is_syn_flag(tcp) and not is_from_server:
                # create new connection
                self.conn[from_app_tag] = Connection()
                continue

            if self.is_fin_flag(tcp):
                if is_from_app:
                    self.conn[from_app_tag].app_fin = True
                elif is_from_server:
                    self.conn[from_server_tag].server_fin = True
                continue

            if self.is_rst_flag(tcp):
                if is_from_app:
                    self.conn[from_app_tag].rst = True
                elif is_from_server:
                    self.conn[from_app_tag].rst = True
                continue

            if tcp.flags == dpkt.tcp.TH_ACK:
                continue


            if conn_key is None:
                continue

            if is_from_server:
                self.conn[conn_key].tcp_server_data += tcp.data

            try:
                stream = self.conn[conn_key].tcp_server_data
                if stream[:4] == 'HTTP':
                    http_response = dpkt.http.Response(stream)
                    curr_http_req = self.conn[conn_key].curr_http_req
                    if curr_http_req is None:
                        raise ValueError

                    if curr_http_req not in self.conn[conn_key].http_data:
                        self.conn[conn_key].http_data[curr_http_req] = [http_response]
                    else:
                        self.conn[conn_key].http_data[curr_http_req].append(http_response)
                else:
                    http_request = dpkt.http.Request(tcp.data)
                    self.conn[conn_key].curr_http_req = http_request
            except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                continue




        pass


class Connection(object):
    def __init__(self):
        self.app_fin = False
        self.server_fin = False
        self.rst = False
        self.tcp_server_data = ''
        self.http_data = dict()
        self.curr_http_req = None

