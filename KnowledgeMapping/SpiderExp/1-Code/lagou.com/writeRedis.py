import redis
import json


redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)
conn_redis = redis.Redis(connection_pool=redis_pool)
source_path = "D://A//C//lagouData.csv"

with open(source_path, "r") as f:

    while True:
        data = f.readline().strip()
        if not data:
            print("exit")
            break
        conn_redis.rpush("lagou:spider", data)
        print(data)