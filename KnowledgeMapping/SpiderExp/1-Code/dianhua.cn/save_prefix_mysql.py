"""
所有号码段存入192.168.70.40的mysql
"""
import os
import pymysql


# 获取指定文件夹文件列表
def get_files_name(dir):
    all_filename = os.listdir(dir)
    return all_filename


# 从文件中提取出号码前缀
def split_number(filename, parents_dir):
    print("File name is <{}>".format(filename))
    # 读取文件
    with open(os.path.join(parents_dir, filename), "r") as f:
        results = f.readlines()

    # 逐行读取文件
    for result in results:
            data = result.strip().split(",")
            if len(data) == 5:
                print(data)
                sql = "insert into number_prefix(prefix,company,province,city,sub_company) value ('{}','{}','{}','{}','{}')".format(*data)
                mysql_cursor.execute(sql)
            else:
                print("{} {}".format(data, filename))
    mysql_conn.commit()


if __name__ == '__main__':
    # 连接MySQL
    print("Connect to mysql...")
    mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='phone_number_info', charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    main_dir = "/home/nick/Desktop/H3-移动号码归属/"
    # main_dir = "/home/watson/dc45/telephone_number/bd_dhb/H3-移动号码归属"
    # 获取所有文件名称 list
    files = get_files_name(main_dir)
    print("文件夹<{}>下共<{}>个文件".format(main_dir, len(files)))
    # 把每一个文件传入函数提取出电话号码前缀，第一行不要
    for file in files:
        split_number(file, main_dir)

    # 关闭mysql连接
    mysql_cursor.close()
    mysql_conn.close()
    print("Close MySQL Connection...")
    print("end")
