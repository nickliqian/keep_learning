import pymysql
import redis

print("Connect to mysql...")
mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='phone_number_info', charset='utf8')
mysql_cursor = mysql_conn.cursor()

# 连接redis
r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r_conn = redis.Redis(connection_pool=r_pool)


try:

    result = r_conn.smembers("telephone_task")

    while True:

        try:
            num = result.pop()

            i = num.decode("utf-8")

            sql = "select prefix from number_prefix WHERE id={}".format(i)
            mysql_cursor.execute(sql)
            r = mysql_cursor.fetchall()

            if r:
                pre = r[0][0]

                sql = "insert into number_test(prefix, flag) VALUE ('{}','{}')".format(pre, 0)
                mysql_cursor.execute(sql)
                mysql_conn.commit()
                print("insert {} {}".format(pre, 0))

            else:
                print("no result")

        except KeyError:
            print("Set is empty")
            break

finally:
    mysql_cursor.close()
    mysql_conn.close()
    print("Close MySQL Connection...")
    print("end")