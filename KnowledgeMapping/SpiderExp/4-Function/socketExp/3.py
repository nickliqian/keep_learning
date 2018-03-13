import socket
import ssl


s = socket.socket()
sock = ssl.wrap_socket(s)

url = "sp0.baidu.com"

sock.connect((url, 443))

data = b"""
GET /8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA&pn=10&rn=10&ie=utf-8&oe=utf-8&format=json&t=1520925028538&cb=jQuery110205127129572717999_1520836892261&_=1520836892304 HTTP/1.1
Host: sp0.baidu.com
Connection: close
Pragma: no-cache
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36
Accept: */*
Referer: https://www.baidu.com/s?wd=%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA&rsv_spt=1&rsv_iqid=0x9e071f490004d9bb&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=1&oq=requests&rsv_t=a4cb%2BCdngGc0OR6%2BDn7gHSPq5XNjtXWlfBgXQ%2Fly2nB%2BmM57fk3Xv01kWuzpye0Phn%2FQ&inputT=1208&rsv_sug3=37&rsv_sug1=31&rsv_sug7=100&rsv_pq=dddc338200049975&rsv_sug2=0&rsv_sug4=2274
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7\r\n\r\n
"""

sock.send(data)

recv_data = sock.recv(8192)

sock.close()

print(recv_data)
