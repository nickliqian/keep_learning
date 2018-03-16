import socket
import time


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("127.0.0.1", 9999))
print("Receive:{}".format(sock.recv(1024).decode("utf-8")))

while True:
    string = input("Send:")
    sock.send(string.encode("utf-8"))
    str_recv = sock.recv(1024).decode("utf-8")
    print("Receive:{}".format(str_recv))
    if string == "exit" and str_recv == "exit":
        sock.send(b"exit")
        sock.close()
        print("Connection closed")
        break
