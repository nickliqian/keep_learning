import pymysql


print("Connect to mysql...")
mysql_db = "mydata"
m_conn = pymysql.connect(host='192.168.10.87', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
m_cursor = m_conn.cursor()

num_id = 1
try:
    sql = "select * from house_name where id={}".format(num_id)
    m_cursor.execute(sql)
    query_results = m_cursor.fetchall()
    print(query_results)
    if not query_results:
        print("MySQL查询结果为空 id=<{}>".format(num_id))
    else:
        query_houses = query_results[0][2]

finally:
    m_cursor.close()
    m_conn.close()
    print("MySQL connection close...")