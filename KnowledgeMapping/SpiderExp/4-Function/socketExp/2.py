import socket
import ssl

s = socket.socket()
sock = ssl.wrap_socket(s)
sock.connect(('passport.baidu.com', 443))
data = '''\ 
POST /?login HTTP/1.1 
...
'''

sock.sendall(data)

recv_data = sock.recv(8192)

sock.close()

