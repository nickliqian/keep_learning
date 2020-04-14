import pymysql
import random


print("Connect to mysql...")
mysql_db = "mytest"
m_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
m_cursor = m_conn.cursor()


try:
    for i in range(10000):
        print(i)
        key1 = str(random.randint(1, 100))
        key2 = 10 * i + i
        key3 = str(random.randint(1, 100))
        key_part1 = str(random.randint(1, 100))
        key_part2 = str(random.randint(1, 100))
        key_part3 = str(random.randint(1, 100))
        common_field = str(random.randint(1, 100))

        sql = "insert into single_table(key1, key2, key3, key_part1, key_part2, key_part3, common_field)" \
              " values(%s,%s,%s,%s,%s,%s,%s)"
        m_cursor.execute(sql, [key1, key2, key3, key_part1, key_part2, key_part3, common_field])
    m_conn.commit()

finally:
    m_cursor.close()
    m_conn.close()
    print("MySQL connection close...")