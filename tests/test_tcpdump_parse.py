import unittest2
import dpkt
import arrow
from tests import *
import pandas as pd
import socket
import time
from intellistock.pcap_parser import TcpConnTrack


def setUpModule():
    global excel_helper
    excel_helper = ExcelHelper(get_excel_path('test_tcpdump'))

def tearDownModule():
    global excel_helper
    excel_helper.close()


filename='./test_data/tcpdump.pcap'

class Connection(object):
    def __init__(self, data):
        self.start = time.time()
        self.data = data

    def append(self, data):
        self.data += data

    def __len__(self):
        return len(self.data)

    def chronometer(self):
        return (time.time() - self.start) * 1000


class HttpConnection(object):
    def __init__(self,request,request_ts,response,response_ts):
        self.request = request
        self.request_ts = request_ts
        self.response = response
        self.response_ts = response_ts


    def dump(self):
        pass



class MyTestCase(UnitTestBase):

    def test_pcap_parser(self):
        TcpConnTrack().parse_http_from_file(filename)


    @unittest2.skip('skip')
    def test_something(self):
        df = pd.DataFrame()
        conn = dict()  # Connections with current buffer
        rere = dict()
        http_conn = dict()
        for ts, pkt in dpkt.pcap.Reader(open(filename, 'rb')):
            eth = dpkt.ethernet.Ethernet(pkt)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                continue


            ip = eth.data
            if not isinstance(ip.data, dpkt.tcp.TCP):
                continue



            # Set the TCP data
            tcp = ip.data
            saddr = socket.inet_ntoa(ip.src)
            sport = tcp.sport
            daddr = socket.inet_ntoa(ip.dst)
            dport = tcp.dport
            tupl = (saddr, sport, daddr, dport)
            k = (daddr, dport,saddr, sport)
            if tupl in conn:
                conn[tupl].append(tcp.data)
            else:
                conn[tupl] = Connection(tcp.data)

            # Now see if we can parse the contents as a HTTP request
            try:
                stream = conn[tupl].data
                if stream[:4] == 'HTTP':
                    http_response = dpkt.http.Response(stream)
                    if k in rere:
                        http_conn[k] = HttpConnection(rere[k][0],rere[k][1],http_response,ts)
                        del rere[k]
                else:
                    http_request = dpkt.http.Request(tcp.data)
                    rere[tupl] = (http_request,ts)
            except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                continue
        # end for

        # # Print out the info
        # time = arrow.get(ts).to('local').format('YYYY-MM-DD HH:mm:ss.SS')
        # host = http_request.headers['host']
        # url = http_request.uri
        # #print 'ts:{}'.format(time)
        # #print 'host:{}'.format(host)
        # #print 'url:{}'.format(url)
        # df0 = pd.DataFrame({'ts':[time],'host':[host],'url':[url]})
        # df = df.append(df0)
        # df = df.set_index('ts')
        # excel_helper.add(df,'tcpdump')

        print http_conn



        self.assertEqual(True, True)


if __name__ == '__main__':
    logging_config()
    unittest2.main()
