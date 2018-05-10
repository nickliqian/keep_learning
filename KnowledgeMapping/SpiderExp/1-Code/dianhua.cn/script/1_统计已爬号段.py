import pymysql
import redis

print("Connect to mysql...")
mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='phone_number_info', charset='utf8')
mysql_cursor = mysql_conn.cursor()

# 连接redis
r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r_conn = redis.Redis(connection_pool=r_pool)


try:

    for i in range(1, 455699):

        sql = "select number from number_tag WHERE id={}".format(i)
        mysql_cursor.execute(sql)
        r = mysql_cursor.fetchall()

        if r:
            pre = r[0][0][:7]
            print(pre)
            r_conn.sadd("baidu_phone_already_crawl", pre)
        else:
            print("no result")


finally:
    mysql_cursor.close()
    mysql_conn.close()
    print("Close MySQL Connection...")
    print("end")