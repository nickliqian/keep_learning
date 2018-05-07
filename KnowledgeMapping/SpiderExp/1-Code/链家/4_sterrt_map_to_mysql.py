import pymysql
import json

mysql_db = "lianjia"
mysql_table = "lianjia_area"
m_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
m_cursor = m_conn.cursor()

try:
    with open("./dc45/street_map.json", "r") as f:
        data = json.load(f)

    for d in data:
        print(d)
        sql = "INSERT INTO {}(city,city_code,area,street,street_url) VALUE ('{}','{}','{}','{}','{}')"\
            .format(mysql_table, d["city_name"], d["city_code"], d["area_name"], d["street"], d["href"])
        m_cursor.execute(sql)
        m_conn.commit()
finally:
    m_cursor.close()
    m_conn.close()
    print("close mysql connection")