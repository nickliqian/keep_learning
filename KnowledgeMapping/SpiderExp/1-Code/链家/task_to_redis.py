import redis
import json
r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r_conn = redis.Redis(connection_pool=r_pool)
with open("./dc45/street_map.json", "r") as f:
    data = json.load(f)

for d in data:
    r_conn.sadd("lianjia_list_task", d)
