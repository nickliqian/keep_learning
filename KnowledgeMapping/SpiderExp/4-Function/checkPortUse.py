import os
import socket
def IsOpen(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        #利用shutdown()函数使socket双向数据传输变为单向数据传输。shutdown()需要一个单独的参数，
        #该参数表示了如何关闭socket。具体为：0表示禁止将来读；1表示禁止将来写；2表示禁止将来读和写。
        print('%d is open' % port)
        return True
    except:
        print('%d is down' % port)
        return False
if __name__ == '__main__':
    IsOpen('127.0.0.1', 7777)