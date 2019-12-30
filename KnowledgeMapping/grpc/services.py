import struct
from io import BytesIO
import socket
import threading


class InvalidOperation(Exception):
    def __init__(self, message=None):
        self.message = message or 'invalid operation'


class MethodProtocol(object):

    def __init__(self, connection):
        self.conn = connection

    def _read_all(self, size):
        """
        读取指定大小的二进制数据
        :param size:
        :return:
        """
        if isinstance(self.conn, BytesIO):
            buff = self.conn.read(size)
            return buff
        else:
            # socket
            have = 0
            buff = b''
            while have < size:
                chunk = self.conn.recv(size - have)
                buff += chunk
                chunk_len = len(chunk)
                have += chunk_len

                if chunk_len == 0:
                    # 表示客户端socket关闭了
                    raise EOFError()
        return buff

    def get_method_name(self):
        """
        提供方法名
        :return:
        """
        buff = self._read_all(4)
        length = struct.unpack('!I', buff)[0]

        buff = self._read_all(length)
        name = buff.decode()
        return name


class DivideProtocol(object):

    def __init__(self):
        self.conn = None

    def args_encode(self, num1, num2=1):
        """
        把方法名和参数都编码为二进制
        :param num1:
        :param num2:
        :return:
        """
        name = "divide"

        # 方法名
        buff = struct.pack("!I", 6)
        buff += name.encode()

        # 参数1
        buff2 = struct.pack("!B", 1)
        buff2 += struct.pack("!I", num1)

        # 参数2
        if num2 != 1:
            buff2 = struct.pack("!B", 2)
            buff2 += struct.pack("!I", num2)

        # 处理消息长度，边界设定
        length = len(buff2)
        buff += struct.pack("!I", length)

        # 合并方法名和参数
        buff += buff2

        return buff

    def _read_all(self, size):
        """
        读取指定大小的二进制数据
        :param size:
        :return:
        """
        if isinstance(self.conn, BytesIO):
            buff = self.conn.read(size)
            return buff
        else:
            # socket
            have = 0
            buff = b''
            while have < size:
                chunk = self.conn.recv(size - have)
                buff += chunk
                chunk_len = len(chunk)
                have += chunk_len

                if chunk_len == 0:
                    # 表示客户端socket关闭了
                    raise EOFError()
        return buff

    def args_decode(self, connection):
        """
        参数解码
        :param connection:
        :return:
        """
        params_detail = [
            {
                "len": 4,
                "fmt": "!i",
                "name": "num1"
            },
            {
                "len": 4,
                "fmt": "!i",
                "name": "num1"
            }
        ]

        args = dict()

        self.conn = connection

        # 处理方法名

        # 处理消息边界(得到参数数据的总长度，一次性读出来)
        buff = self._read_all(4)
        length = struct.unpack('!I', buff)[0]

        # 已经读取处理的字节数
        hava = 0

        # 处理第一个参数
        buff = self._read_all(1)
        hava += 1
        param_seq = struct.unpack('!B', buff)[0]

        buff = self._read_all(params_detail[param_seq]["len"])
        hava += params_detail[param_seq]["len"]
        param = struct.unpack(params_detail[param_seq]["fmt"], buff)[0]

        args[params_detail[param_seq]["name"]] = param

        if hava >= length:
            return args

        # 处理第二个参数值
        buff = self._read_all(1)
        hava += 1
        param_seq = struct.unpack('!B', buff)[0]

        buff = self._read_all(params_detail[param_seq]["len"])
        hava += params_detail[param_seq]["len"]
        param = struct.unpack(params_detail[param_seq]["fmt"], buff)[0]

        args[params_detail[param_seq]["name"]] = param

        return args

    def result_encode(self, result):
        """
        返回值编码
        :param result:
        :return:
        """
        # 正常返回浮点型
        if isinstance(result, float):
            buff = struct.pack('!B', 1)
            buff += struct.pack('!f', result)
            return buff
        # 异常
        else:
            buff = struct.pack('!B', 2)
            length = len(result.message)
            buff += struct.pack('!I', length)
            buff += result.message.encode()
            return buff

    def result_decode(self, connnection):
        """
        传递过来的二进制形式的返回值解码
        :param connnection:
        :return:
        """
        self.conn = connnection

        # 获取类型（浮点结果还是异常）
        buff = self._read_all(1)
        result_type = struct.unpack('!B', buff)[0]

        # 浮点结果
        if result_type == 1:
            buff = self._read_all(4)
            val = struct.unpack('!f', buff)[0]
            return val
        else:
            buff = self._read_all(4)
            length = struct.unpack('!I', buff)[0]

            buff = self._read_all(length)
            message = buff.decode()

            return InvalidOperation(message)


class Channel(object):
    """
    客户端建立网络连接
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_connection(self):
        """
        获取连接对象
        :return:
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock


class Server(object):
    """
    RPC服务器
    """
    def __init__(self, host, port, handlers):
        # 创建socket的工具对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置socket重用地址
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 绑定地址
        sock.bind((host, port))
        self.host = host
        self.port = port
        self.sock = sock
        self.handlers = handlers

    def server(self):
        """
        开启服务器运行，提供RPC服务
        :return:
        """
        self.sock.listen(128)
        print("服务器开始监听")

        while True:
            # 接收客户端请求
            client_sock, client_addr = self.sock.accept()

            # 交给ServerStub，完成客户端的具体的RPC调用请求
            pass


class ClientStub(object):
    """
    用来帮助客户端完成远程过程调用 RPC调用

    stub = ClientStub()
    stub.divide(100, 100)
    stub.add(100, 100)
    """

    def __init__(self, channel):
        self.channel = channel
        self.conn = self.channel.get_connection()

    def divide(self, num1, num2=1):
        # 将调用的参数打包成消息协议的数据
        proto = DivideProtocol()
        args = proto.args_encode(num1, num2)

        # 将消息数据通过网络发送给服务器
        self.conn.senall(args)

        # 接收服务器返回的返回值消息数据，并进行解析
        result = proto.result_decode(self.conn)

        # 将结果值
        if isinstance(result, float):
            return result
        else:
            raise result


class ServerStub(object):
    """
    帮助服务器完成远端过程调用
    """
    def __init__(self, connection, handlers):
        """

        :param connection:
        :param handlers:
        """
        self.conn = connection
        self.method_proto = MethodProtocol(self.conn)
        self.process_map = {
            "divide": self._process_divide,
        }
        self.handlers = handlers

    def process(self):
        """
        当服务端接受了一个客户端的连接，建立好连接后，完成远端调用处理
        :return:
        """
        # 接受消息数据，解析方法的名字
        name = self.method_proto.get_method_name()
        # 根据解析获得的方法名，调用响应的过程协议，接受并解析消息数据
        _process = self.process_map[name]
        _process()

    def _process_divide(self):
        """
        处理除法的过程调用
        :return:
        """
        # 创建用于除法过程调用参数协议数据解析的工具
        proto = DivideProtocol()
        # 解析调用参数消息数据
        args = proto.args_decode(self.conn)

        try:
            val = self.handlers.divide(**args)
        except InvalidOperation as e:
            ret_message = proto.result_encode(e)
        else:
            ret_message = proto.result_encode(val)

        self.conn.senall(ret_message)


if __name__ == '__main__':
    proto = DivideProtocol()

    message = proto.args_encode(200)
    conn = BytesIO()
    conn.write(message)
    conn.seek(0)

    method_proto = MethodProtocol(conn)
    name = method_proto.get_method_name()
    print(name)

    args = proto.args_decode(conn)
    print(args)


