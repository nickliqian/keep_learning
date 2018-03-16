import socket
import time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 9999))
print("recive:{}".format(s.recv(1024).decode("utf-8")))

while True:
    string = input("Send:")
    s.send(string.encode("utf-8"))
    str_recv = s.recv(1024).decode("utf-8")
    print("recive:{}".format(str_recv))
    if string == "exit" and str_recv == "exit":
        s.send(b"exit")
        s.close()
