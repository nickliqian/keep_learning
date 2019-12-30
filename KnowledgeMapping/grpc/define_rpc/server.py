import socket
import threading
import struct


class Server(object):
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 9001
        self.server_name = (self.host, self.port)
        self.recv_size = 11

    def start_server(self):
        # 创建socket的工具对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置socket 重用地址
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定地址
        sock.bind((self.host, self.port))
        # 监听客户端
        sock.listen(128)
        print("监听中...")

        # 接受客户端的连接请求
        while True:
            client_sock, client_addr = sock.accept()
            print('与客户端%s建立了连接' % str(client_addr))
            # print("client_sock: {}".format(client_sock))

            # 创建子线程处理这个客户端
            t = threading.Thread(target=self._handler, args=(client_sock, client_addr))
            # 开启子线程执行
            t.start()

    def _handler(self, client_sock, client_addr):
        recv_data = b''
        # 循环接收
        while True:
            msg = client_sock.recv(self.recv_size)
            print(len(msg))
            recv_data += msg
            if len(msg) < self.recv_size:
                break
            elif len(msg) == self.recv_size:
                count = recv_data[:4]
                count_value = struct.unpack("!I", count)[0]
                print(count_value)
                end_string = recv_data[-2:].decode("utf-8")
                print(end_string)
                if (len(msg) == count_value) and (end_string == "\r\n"):
                    break
            else:
                pass

        recv_data = recv_data[4:-2]
        # 把接收到的数据进行解码
        strData = recv_data.decode("utf-8")
        print(client_addr)
        print(strData)
        print(self.server_name)
        print(strData)
        client_sock.send(strData.encode("utf-8"))


if __name__ == '__main__':
    server = Server()
    server.start_server()





