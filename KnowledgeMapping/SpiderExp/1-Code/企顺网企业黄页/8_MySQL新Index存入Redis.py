import pymysql
import redis


redis_key = "qishun_list"
mysql_db = "qishun"

redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
redis_conn = redis.Redis(connection_pool=redis_pool)

m_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
m_cursor = m_conn.cursor()

try:
    for i in range(1, 130000):
        id_num = i
        sql = "select city,url_title,url from request_index WHERE id={}".format(id_num)
        m_cursor.execute(sql)
        results = m_cursor.fetchall()
        if results:
            result = results[0]
            print(result)
            redis_conn.sadd(redis_key, str(result))

finally:
    m_cursor.close()
    m_conn.close()
    print("数据库连接关闭")
