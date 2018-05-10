import pymysql

print("Connect to mysql...")
mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='phone_number_info', charset='utf8')
mysql_cursor = mysql_conn.cursor()


try:

    province_list = ['广东', '上海', '北京', '河南', '山东', '江苏', '浙江']

    for province in province_list:
        sql = "SELECT prefix FROM number_prefix WHERE province='{}'".format(province)
        mysql_cursor.execute(sql)
        results = mysql_cursor.fetchall()
        if results:
            for r in results:
                sql = "insert ignore into number_test(prefix, flag) VALUE ('{}','{}')".format(r[0], 1)
                mysql_cursor.execute(sql)
                mysql_conn.commit()
                print("insert -> {} {} {}".format(province, r[0], 1))
        else:
            print(province, "empty")

finally:
    mysql_cursor.close()
    mysql_conn.close()
    print("Close MySQL Connection...")
    print("end")