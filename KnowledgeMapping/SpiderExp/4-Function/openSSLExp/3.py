import requests
import ssl
from requests.adapters import HTTPAdapter, PoolManager


class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize):
        super(MyAdapter, self).__init__()
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, ssl_version=ssl.PROTOCOL_SSLv3)


s = requests.Session()
s.mount('https://', MyAdapter())  # 所有的https连接都用ssl.PROTOCOL_SSLV3去连接
s.get('https://xxx.com')
