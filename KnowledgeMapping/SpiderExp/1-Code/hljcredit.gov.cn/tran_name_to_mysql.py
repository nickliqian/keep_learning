import pymysql
import redis

if __name__ == '__main__':
    # 连接MySQL
    print("Connect to mysql...")
    mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='name', charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    # 连接redis
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    redis_conn = redis.Redis(connection_pool=redis_pool)

    try:
        while True:
            # 从redis取出数据
            name_byte = redis_conn.spop("hlj_name_word")
            if name_byte:
                name = name_byte.decode("utf-8")

                try:
                    sql = "insert into hlj_name_0428(name) VALUE ('{}')".format(name)
                    mysql_cursor.execute(sql)
                    mysql_conn.commit()
                except Exception as e:
                    redis_conn.sadd("hlj_name_word", name)
                    print("Error {} {}".format(name, e))
                    raise e
                else:
                    print("Insert {}".format(name))

            else:
                print("Redis no data...")
                break
    except Exception as e:
        print("MySQL Opration Error...")
        raise e
    finally:
        # 关闭mysql连接
        mysql_cursor.close()
        mysql_conn.close()
        print("Close MySQL Connection...")
        print("end")
