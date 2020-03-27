from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase

# server端地址和端口
transport = TSocket.TSocket('192.168.19.31', 9090)
# 可以设置超时
transport.setTimeout(5000)
# 设置传输方式（TFramedTransport或TBufferedTransport）
trans = TTransport.TBufferedTransport(transport)
# 设置传输协议
protocol = TBinaryProtocol.TBinaryProtocol(trans)
# 确定客户端
client = Hbase.Client(protocol)
# 打开连接
transport.open()

print(client.getTableNames())