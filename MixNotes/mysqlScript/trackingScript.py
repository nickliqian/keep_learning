import pymysql


mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='bd05', charset='utf8')
mysql_cursor = mysql_conn.cursor()


try:
    sql = "select count(*) from bd05"
    mysql_cursor.execute(sql)
    result = mysql_cursor.fetchall()
    print(result[0][0])

    sql = "insert into dcc.project_tablecount(count, table_id, time_point) VALUE ()"

    mysql_conn.commit()
finally:
    mysql_cursor.close()
    mysql_conn.close()