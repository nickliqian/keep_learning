import xlrd
import os
import pymysql
import zipfile


def check_file_format():
    file_list = os.listdir(base_path)
    file_list.sort()
    exp_header_1 = ['公司名称', '法定代表人', '注册资本', '成立日期', '联系电话', '地址', '企业网址', '邮箱', '经营范围']
    exp_header_2 = ['公司名称', '法定代表人', '注册资本', '成立日期', '所属地区', '统一信用代码', '联系电话', '地址', '企业网址', '邮箱', '经营范围']
    exp_header_3 = ['公司名称', '法定代表人', '注册资本', '成立日期', '所属地区', '统一信用代码', '企业公示的联系电话', '企业公示的地址', '企业公示的网址', '企业公示的邮箱', '经营范围']

    BadZipFile_list = []

    for i, file_name in enumerate(file_list):
        if i < 9508:
            continue
        print("start {}".format(file_name))
        if not file_name.endswith(".xlsx"):
            continue
        # if file_name == "企业数据服务—天眼查(W20080905951533782806447).xlsx":
        # if file_name == "企业数据服务—天眼查(W20070905951531100095212).xlsx":
        file_path = os.path.join(base_path, file_name)
        try:
            data = xlrd.open_workbook(file_path)  # 打开xls文件
        except zipfile.BadZipFile:
            BadZipFile_list.append(file_name)
            continue
        table = data.sheets()[0]  # 打开第一张表
        header = table.row_values(1)

        if header not in (exp_header_1, exp_header_2, exp_header_3):
            print("[{}] {}: fail_1".format(i, file_name))
            print("{} {}".format(len(header), header))
            break
        else:
            print("[{}] {}: pass".format(i, file_name))

        # break

    print("file count: {}".format(len(file_list)))
    print("BadZipFile_list: {}".format(BadZipFile_list))


def main():
    print("Connect to mysql...")
    mysql_db = "company_data"
    m_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
    m_cursor = m_conn.cursor()

    try:
        file_list = os.listdir(base_path)
        file_list.sort()
        exp_header_1 = ['公司名称', '法定代表人', '注册资本', '成立日期', '联系电话', '地址', '企业网址', '邮箱', '经营范围']
        exp_header_2 = ['公司名称', '法定代表人', '注册资本', '成立日期', '所属地区', '统一信用代码', '联系电话', '地址', '企业网址', '邮箱', '经营范围']
        exp_header_3 = ['公司名称', '法定代表人', '注册资本', '成立日期', '所属地区', '统一信用代码', '企业公示的联系电话', '企业公示的地址', '企业公示的网址', '企业公示的邮箱',
                        '经营范围']

        for index, file_name in enumerate(file_list):
            if not file_name.endswith(".xlsx"):
                continue
            if index <= 10355:
                continue
            file_path = os.path.join(base_path, file_name)
            data = xlrd.open_workbook(file_path)  # 打开xls文件
            table = data.sheets()[0]  # 打开第一张表
            nrows = table.nrows  # 获取表的行数
            header = table.row_values(1)
            if header == exp_header_1:
                for i in range(nrows):  # 循环逐行打印
                    if i == 0:  # 跳过第一行
                        continue
                    data_list = table.row_values(i)  # 取前十三列
                    sql = "insert into tyc_info_1(company_name, legal_person, registered_capital, establishment_date, telephone, address, site, email, business_scope)  VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    m_cursor.execute(sql, data_list)
                m_conn.commit()
                print("[{}] {} {} {}".format(index, file_name, 1, nrows))
            elif header == exp_header_2:
                for i in range(nrows):  # 循环逐行打印
                    if i == 0:  # 跳过第一行
                        continue
                    data_list = table.row_values(i)  # 取前十三列
                    sql = "insert into tyc_info_2(company_name, legal_person, registered_capital, establishment_date, area, credit_code, telephone, address, site, email, business_scope)   VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    m_cursor.execute(sql, data_list)
                m_conn.commit()
                print("[{}] {} {} {}".format(index, file_name, 2, nrows))
            elif header == exp_header_3:
                for i in range(nrows):  # 循环逐行打印
                    if i == 0:  # 跳过第一行
                        continue
                    data_list = table.row_values(i)  # 取前十三列
                    sql = "insert into tyc_info_3(company_name, legal_person, registered_capital, establishment_date, area, credit_code, telephone, address, site, email, business_scope)    VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    m_cursor.execute(sql, data_list)
                m_conn.commit()
                print("[{}] {} {} {}".format(index, file_name, 3, nrows))
            else:
                print("{} {} {}".format(index, file_name, nrows))
                break

            with open("./loc", "w") as f:
                f.write(str(index))
    finally:
        m_cursor.close()
        m_conn.close()
        print("MySQL connection close...")


if __name__ == '__main__':
    base_path = "D:\\A\\Desktop\\StudyFlow\\爬虫数据\\天眼查\\1003\\"
    main()
