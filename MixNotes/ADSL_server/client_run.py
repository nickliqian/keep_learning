import re
import subprocess
import redis
import requests
import os
import time


# 初始化参数
net_name = "ppp0"
port = 9580
redis_host = os.getenv("redis_host")
redis_password = os.getenv("redis_password")

print("net_name: {}".format(net_name))
print("port: {}".format(port))
print("redis_host: {}".format(redis_host))
print("redis_password: {}".format(redis_password))

# 连接redis
redis_pool = redis.ConnectionPool(host=redis_host, port=6379, password=redis_password, decode_responses=True)
redis_client = redis.Redis(connection_pool=redis_pool)
print("连接redis")

while True:
    # 重启宽带
    print("start restart pppoe")
    subprocess.getstatusoutput("pppoe-stop")
    time.sleep(0.5)
    (status, output) = subprocess.getstatusoutput("pppoe-start")
    print("pppoe-stop;pppoe-start - status: {}, output: {}".format(status, output))
    if status == 0:
        print('ADSL restart Successfully')

        (status, output) = subprocess.getstatusoutput('ifconfig')
        pattern = re.compile(net_name + '.*?inet.*?(\d+\.\d+\.\d+\.\d+).*?netmask', re.S)
        result = re.search(pattern, output)

        if result:
            ip = result.group(1)
            print("匹配的ip地址为： {}".format(ip))
            print("开始连接测试")
            test_url = "https://www.baidu.com"
            response = requests.get(url=test_url,
                                    proxies={"http": "{}:{}".format(ip, port), "https": "{}:{}".format(ip, port)},
                                    timeout=5)
            if response.status_code == 200:
                print("连接测试成功")
                # redis_client.delete("adsl_ip")
                r = redis_client.set("adsl_ip", "{}:{}".format(ip, port))
                print("redis set result: {}".format(r))

                print("insert success")

                print("等待30s重拨")
                for i in range(1, 31):
                    time.sleep(1)
                    print("time: {}s".format(i), end='\r')
                print()
            else:
                print("连接测试失败")
                time.sleep(3)
        else:
            print("无法匹配出ip地址")
            time.sleep(10)

    else:
        print('ADSL restart failed')
        time.sleep(10)
