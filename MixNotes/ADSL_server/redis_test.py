import redis
import os
import time


redis_host = os.getenv("redis_host")
redis_password = os.getenv("redis_password")

# 连接redis
redis_pool = redis.ConnectionPool(host=redis_host, port=6379, password=redis_password, decode_responses=True)
redis_client = redis.Redis(connection_pool=redis_pool)
print("连接redis")
print("start")
r = redis_client.set("adsl_ip", "{}:{}".format("123", "1234"))
print(r)

time.sleep(10)
print("start")
r = redis_client.set("adsl_ip", "{}:{}".format("123", "1234"))
print(r)
