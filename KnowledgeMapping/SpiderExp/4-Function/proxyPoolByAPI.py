import requests
import redis
import time
from multiprocessing import Pool
import os


def get_wuyou_ip(set_name, api_num):
    """
    request api and get usage ip value
    str:param set_name:redis set name/process name
    int:param api_num:choose api url
    str:return:ip from api
    """
    while True:
        if api_num == 1:
            # 15999543812@163.com
            url = "http://api.ip.data5u.com/dynamic/get.html?order=752f110af5d4475a4576f097a9f2e569&ttl=1&sep=3"
        else:
            # 86395@qq.com
            url = "http://api.ip.data5u.com/dynamic/get.html?order=abf29865eba904481712d47f9c078847&ttl=1&sep=3"
        session = requests.Session()
        session.trust_env = False
        try:
            r = session.get(url, timeout=10)
            print("Process-{} -> {}".format(set_name, r.text))
            ip, ttl = r.text.split(",")
            if int(ttl) > 15000:
                return ip, ttl
        except Exception as e:
            print("Process-{} -> {}".format(set_name, e))
            print("Process-{} -> 即将重试".format(set_name))
        time.sleep(1)


def keep_pool(set_name, api_num):
    """
    update redis set value to be ip by loop
    str:param set_name:redis set name/process name
    int:param api_num:choose api url
    None:return:
    """
    # 连接Redis
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    conn_redis = redis.Redis(connection_pool=redis_pool)

    while True:
        try:
            # 获得IP和剩余存活时间
            ip, ttl = get_wuyou_ip(set_name, api_num)
            # 写ip
            conn_redis.set(set_name, ip)
            # 计算休眠时间
            # ttl = int(ttl)/1000-10
            # 休眠，时间到后获取新的IP并覆盖旧的IP
            time.sleep(10)
        except Exception as e:
            print("Process-{} -> {}".format(set_name, e))
            time.sleep(1)


if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    # 设置redis代理池组名称和数量
    groupA_name = ["myip11", "myip22", "myip33"]
    groupB_name = ["myip55", "myip66", "myip77"]
    process_num = len(groupA_name) + len(groupB_name)

    # 初始化进程池
    p = Pool(process_num)
    # 向进程池添加任务
    for name in groupA_name:
        p.apply_async(keep_pool, args=(name, 1))

    for name in groupB_name:
        p.apply_async(keep_pool, args=(name, 2))

    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
