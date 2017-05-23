import unittest2
import dpkt
import arrow
from tests import *
import pandas as pd
import socket


def setUpModule():
    global excel_helper
    excel_helper = ExcelHelper(get_excel_path('test_tcpdump'))

def tearDownModule():
    global excel_helper
    excel_helper.close()


filename='./test_data/tcpdump.pcap'

class MyTestCase(unittest2.TestCase):
    def test_something(self):
        df = pd.DataFrame()
        conn = dict()  # Connections with current buffer
        for ts, pkt in dpkt.pcap.Reader(open(filename, 'rb')):
            is_request = False
            is_response = False
            eth = dpkt.ethernet.Ethernet(pkt)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                continue


            ip = eth.data
            if not isinstance(ip.data, dpkt.tcp.TCP):
                continue

            # Set the TCP data
            tcp = ip.data
            f = {'src': socket.inet_ntoa(ip.src), 'sport': tcp.sport,
                 'dst': socket.inet_ntoa(ip.dst), 'dport': tcp.dport}


            # Now see if we can parse the contents as a HTTP request
            try:
                _request = dpkt.http.Request(tcp.data)
                is_request = True
            except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                pass

            try:
                if not is_request:
                    _response = dpkt.http.Response(tcp.data)
                    is_response = True
            except Exception:
                continue
            # Print out the info
            time = arrow.get(ts).to('local').format('YYYY-MM-DD HH:mm:ss.SS')
            host = _request.headers['host']
            url = _request.uri
            #print 'ts:{}'.format(time)
            #print 'host:{}'.format(host)
            #print 'url:{}'.format(url)
            df0 = pd.DataFrame({'ts':[time],'host':[host],'url':[url]})
            df = df.append(df0)
        # end for

        df = df.set_index('ts')

        excel_helper.add(df,'tcpdump')

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest2.main()
