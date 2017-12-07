from wsgiref.simple_server import make_server


# environ: 一个包含所有HTTP请求信息的dict对象
# 一个发送HTTP响应的函数。
def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    body = '<meta charset="UTF-8"><h1>你好, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]


if __name__ == "__main__":
    httpd = make_server('127.0.0.1', 9000, application)
    print("Serving HTTP on port 9000... click: http://127.0.0.1:9000")
    httpd.serve_forever()