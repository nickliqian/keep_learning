import pymysql
import redis
from constant import city2code_dict


if __name__ == '__main__':

    # 连接redis
    print("Connect to redis...")
    r_pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    # 连接MySQL
    print("Connect to mysql...")
    mysql_db = "fangjiawang"
    m_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
    m_cursor = m_conn.cursor()

    try:
        for num_id in range(1, 106501):
        # for num_id in range(1, 10):
            item = {}

            sql = "select * from house_name where id={}".format(num_id)
            m_cursor.execute(sql)
            query_results = m_cursor.fetchall()
            if not query_results:
                print("MySQL查询结果为空 id=<{}>".format(num_id))
            else:
                query_houses = query_results[0][2]
                query_city = query_results[0][1]
                query_url_code = city2code_dict[query_city]

                item["city"] = query_city
                item["house"] = query_houses
                item["code"] = query_url_code

                print(item)

                r_conn.sadd("fangjiawang_task", item)

    finally:
        m_cursor.close()
        m_conn.close()
        print("MySQL connection close...")