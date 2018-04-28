import pymysql
import requests
from lxml import etree


url = "https://www.baidu.com/s?wd=15315720191"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

response = requests.get(url=url, headers=headers)
html = etree.HTML(response.text)
results = html.xpath(
    "//div[@class='c-border op_fraudphone_container']/div//div[@class='op_fraudphone_word']/strong/text()")

print(15315720191, results[0].replace('"', ''))



# 连接MySQL
print("Connect to mysql...")
mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='phone_number_info', charset='utf8')
mysql_cursor = mysql_conn.cursor()

# sql = "SELECT prefix FROM number_prefix WHERE id={}".format(347047)
# mysql_cursor.execute(sql)
# result = mysql_cursor.fetchone()
# print(result[0])

sql = "INSERT INTO number_tag(number,tag,prefix_id) VALUE ('{}','{}','{}')".format(1598454, results[0].replace('"', ''), 67856)

mysql_cursor.execute(sql)
mysql_conn.commit()

mysql_cursor.close()
mysql_conn.close()
print("Close MySQL Connection...")
print("end")