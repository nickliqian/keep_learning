import pymysql

print("Connect to mysql...")
mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='phone_number_info', charset='utf8')
mysql_cursor = mysql_conn.cursor()


try:

    for i in range(1, 291009):
        sql = "SELECT prefix FROM number_prefix WHERE id='{}'".format(i)
        mysql_cursor.execute(sql)
        results = mysql_cursor.fetchall()
        if results:
            prefix = results[0][0]

            # number_prefix_index.id 实际上就是 prefix_id
            sql = "select id from number_prefix_index where prefix='{}'".format(prefix)
            mysql_cursor.execute(sql)
            results = mysql_cursor.fetchall()
            prefix_id = results[0][0]

            sql = "update number_prefix set prefix_id='{}' WHERE id={}".format(prefix_id, i)
            mysql_cursor.execute(sql)
            mysql_conn.commit()

            print("insert -> id<{}> {} {}".format(i, prefix_id, prefix))
        else:
            print("empty -> id<{}>".format(i))

finally:
    mysql_cursor.close()
    mysql_conn.close()
    print("Close MySQL Connection...")
    print("end")