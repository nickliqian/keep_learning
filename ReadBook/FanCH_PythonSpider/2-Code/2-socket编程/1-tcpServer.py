import socket
import threading
import time


# 处理socket连接函数
def dealClient(sock, addr):
    print("Accept new connection from {}:{}".format(*addr))
    # 接收数据后先回信
    sock.send(b"Connect to server...")
    # 取出数据
    while True:
        data = sock.recv(1024).decode("utf-8")
        print(type(data))
        time.sleep(0.1)
        # 如果收到空数据或者收到指令exit则退出线程和关闭套接字
        if data == 'exit':
            sock.send(b"exit")
            sock.close()
            print("Connection from {}:{} closed".format(*addr))
            break
        # 如果收到的数据正常
        print("Send:{}".format(data))
        sock.send(("Loop_Msg -- {}".format(data)).encode('utf-8'))
    print("Thread exit")

if __name__ == "__main__":
    # 设置监听端口连接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 9999))

    s.listen(5)
    print("Waiting for connection...")

    while True:
        # 循环接收连接，并将连接送入一个线程去处理
        sock, addr = s.accept()

        t = threading.Thread(target=dealClient, args=(sock, addr))
        t.start()
