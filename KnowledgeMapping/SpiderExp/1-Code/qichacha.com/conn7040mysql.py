import pymysql


# 连接MySQL
print("Connect to mysql...")
mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='qichacha', charset='utf8')
mysql_cursor = mysql_conn.cursor()


mysql_cursor.close()
mysql_conn.close()
print("Close MySQL Connection...")
print("end")