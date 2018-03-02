import requests
import time


def get_ip(choose_url_num):
    """
    get a proxy ip for crawl, ip value is different each time.
    int:param choose_url_num:api num(1 -> 15999543812@163.com, 2 -> 86395@qq.com)
    str:return:proxy ip value
    """

    if choose_url_num == 1:
        url = "http://api.ip.data5u.com/dynamic/get.html?order=752f110af5d4475a4576f097a9f2e569&ttl=1&sep=3"  ## 15999543812@163.com
    else:
        url = "http://api.ip.data5u.com/dynamic/get.html?order=abf29865eba904481712d47f9c078847&ttl=1&sep=3"  ## 86395@qq.com

    while True:
        session = requests.Session()
        session.trust_env = False
        try:
            r = session.get(url, timeout=10)
            print("origin -> {}".format(r.text))
            ip, ttl = r.text.split(",")
            if int(ttl) > 10000:
                print("ok -> {}".format(ip))
                return ip
        except Exception as e:
            print(e)
            print("即将重试")
        time.sleep(1)


if __name__ == "__main__":
    get_ip(1)
