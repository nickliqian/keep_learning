import re
import redis


r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r_conn = redis.Redis(connection_pool=r_pool)

with open("./log.txt", "r") as f:
    content = f.readlines()

for c in content:
    # print(c.strip())

    r = re.findall(r"(\{.*?\})", c)
    if r:
        print(r[0])
        r_conn.sadd("tencentHouse:task", r[0])
