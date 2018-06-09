import redis

# 连接redis
print("Connect to redis...")
r_pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
r_conn = redis.Redis(connection_pool=r_pool)


for i in range(8339):
    print(i)
    r_conn.sadd("mingluji_task", str(i))