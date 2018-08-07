# -*- coding: utf-8 -*-
# @Topic : 
# @Title : 
# @Content : 
# @Author : LiQian
# @Create Time : 2018/08/07 14:32
# @Update Time : 2018/08/07 14:32
import requests

# 1. 连接超时：服务器在指定时间内没有应答，抛出 requests.exceptions.ConnectTimeout
# requests.get('http://github.com', timeout=0.001)

# 2. 连接、读取超时：分别指定连接和读取的超时时间，服务器在指定时间没有应答，抛出 requests.exceptions.ReadTimeout
# timeout=([连接超时时间], [读取超时时间])
# 连接：客户端连接服务器并并发送http请求服务器
# 读取：客户端等待服务器发送第一个字节之前的时间
# requests.get('http://github.com', timeout=(6.05, 0.01))


# 3. 未知的服务器：抛出 requests.exceptions.ConnectionError
# requests.get('http://github.comasf', timeout=(6.05, 27.05))

# 4. 代理连接不上：代理服务器拒绝建立连接，端口拒绝连接或未开放，抛出 requests.exceptions.ProxyError
# requests.get('http://github.com', timeout=(6.05, 27.05), proxies={"http": "192.168.10.1:800"})


# 5. 连接代理超时：与代理服务器建立连接超时，抛出 requests.exceptions.ConnectTimeout
# requests.get('http://github.com', timeout=(30.05, 30.05), proxies={"http": "10.200.123.123:800"})


# 6. 网络环境异常：抛出 requests.exceptions.ConnectionError
# requests.get('http://github.com', timeout=(6.05, 27.05))


# 7. 即使代理访问很快，如果代理服务器访问目标站点超时，这个锅还是代理服务器背
# 假定代理可用，timeout就是向代理服务器的连接和读取过程的超时时间，不用关心代理服务器是否连接和读取成功
# requests.get('http://github.com', timeout=(0.0001, 0.5), proxies={"http": "192.168.10.1:800"})

