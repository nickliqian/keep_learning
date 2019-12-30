import socket
import struct


host = "127.0.0.1"
port = 9001

# 创建一个客户端的socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务端
client.connect((host, port))

sendmsg = "hello"
info_length = len(sendmsg)
total_length = 4 + info_length + 2
length_buff = struct.pack("!I", total_length)
buff = length_buff + "{}\r\n".format(sendmsg).encode("utf-8")


client.send(buff)
msg = client.recv(1024)
print(msg.decode("utf-8"))
client.close()
