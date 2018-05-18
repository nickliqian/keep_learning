import redis


redis_key = "qishun_list"
redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
redis_conn = redis.Redis(connection_pool=redis_pool)


a = redis_conn.spop(redis_key)
a = a.decode("utf-8")
print(a)
b = eval(a)
print(b)
print(type(b))
redis_conn.sadd(redis_key, a)