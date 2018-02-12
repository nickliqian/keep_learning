import pymysql
import redis

# 连接MySQL
CONN_MYSQL = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db='hlj', charset='utf8')
CURSOR_MYSQL = CONN_MYSQL.cursor()
# 连接Redis
POOL = redis.ConnectionPool(host='127.0.0.1', port=6379)
CONN_REDIS = redis.Redis(connection_pool=POOL)

RedisSetName = "hlj:name"

try:
    while True:
        name = CONN_REDIS.spop(RedisSetName)
        if name:
            name = name.decode("utf-8")
            print("-> ", name)
            sql = "INSERT INTO name (name) VALUES ('%s')" % name
            CURSOR_MYSQL.execute(sql)
            CONN_MYSQL.commit()
        else:
            print("No data -> stop!")
            break
except Exception as e:
    raise e
finally:
    CURSOR_MYSQL.close()
    CONN_MYSQL.close()
    print("数据库连接已经关闭")
