import unittest2
import dpkt
import arrow
from tests import *
import pandas as pd

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
            eth = dpkt.ethernet.Ethernet(pkt)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                continue


            ip = eth.data
            if not isinstance(ip.data, dpkt.tcp.TCP):
                continue

            # Set the TCP data
            tcp = ip.data

            # Now see if we can parse the contents as a HTTP request
            try:
                _request = dpkt.http.Request(tcp.data)
            except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
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
