from wsgiref.simple_server import make_server


def application(environ, start_response):
    """
    符合WSGI标准的一个HTTP处理函数，web程序入口
    :param environ: 请求的信息
    :param start_response: 返回响应的回调函数
    :return:
    """
    # 响应信息
    start_response("200 OK", [("Content-Type", "text/html")])

    text = "<h1>hello world</h1>"
    for i in environ.items():
        print(i)
        text += "<div>{}</div>".format(i)

    # 响应的内容和数据
    return [text.encode("utf-8")]


httpd = make_server("", 8000, application)
print("Serving HTTP on port 8000 ...")
httpd.serve_forever()

