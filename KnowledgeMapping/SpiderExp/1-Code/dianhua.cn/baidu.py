import requests
from lxml import etree
import time
import random
import redis


url = "https://www.baidu.com/s"
params = {
    "wd": "1388888888",
}
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}
# 连接redis
redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
redis_conn = redis.Redis(connection_pool=redis_pool)


def get_now_time():
    time_obj = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return str(time_obj)


def get_proxy():
    """
    获得代理IP
    :return: string
    """
    while True:
        try:
            num_list = [i for i in range(1, 21)]
            ip_choice = random.choice(num_list)
            ip_str = "myip" + str(ip_choice)
            ip_num = redis_conn.mget(ip_str)[0]
            if not ip_num:
                return None
            ip_num = ip_num.decode('utf-8')
            print("本次的代理为: %s" % ip_num)
            return ip_num
        except Exception as e:
            print(e)
            time.sleep(1)


def req_number(number):
    params["wd"] = number

    f = 0
    while f < 3:
        try:
            response = requests.get(url=url, headers=headers, params=params, proxies={"http": get_proxy()})
            if response.status_code == 200:
                html = etree.HTML(response.text)
                results = html.xpath("//div[@class='c-border op_fraudphone_container']/div//div[@class='op_fraudphone_word']/strong/text()")
                print(results)
                if results != []:
                    print(results[0])
                    return results[0]
                else:
                    print("此号码未被标记")
                break
            else:
                print("状态码异常：{},{},{}\n".format(get_now_time(),number, response.status_code))
                with open("./statusCode_error.log", "a+") as f:
                    f.write("{},{},{}\n".format(get_now_time(),number, response.status_code))
        except Exception as e:
            print("请求异常：{},{},{}\n".format(get_now_time(), number, e))
            with open("./exception_error.log", "a+") as f:
                f.write("{},{},{}\n".format(get_now_time(), number, e))
            f += 1


def generate_number(number_prefix):
    if type(number_prefix) == int:
        number_prefix = str(number_prefix)
    for i in range(10000):
        number_suffix = (4-len(str(i)))*'0'+str(i)
        complete_number = number_prefix + number_suffix
        print(complete_number)
        tag = req_number(complete_number)
        with open("./{}.csv".format(number_prefix), "a+") as f:
            f.write("{},{}\n".format(complete_number, tag))
        time.sleep(0.5)


if __name__ == '__main__':
    # 连接redis
    r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    while True:
        num_b = r_conn.spop("telephone_task")
        if num_b:
            num = num_b.decode("utf-8")
            generate_number(num)