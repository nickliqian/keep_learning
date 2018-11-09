import xlrd
import os
import pymysql


def check_file_format():
    file_list = os.listdir(base_path)
    file_list.sort()
    exp_header_1 = ['企业名称', '省份', '城市', '统一社会信用代码', '法定代表人', '企业类型', '成立日期', '注册资本', '地址', '邮箱', '经营范围', '网址', '电话号码', '电话号码（更多号码）']
    exp_header_2 = ['企业名称', '法人', '成立日期', '注册资本', '地址', '邮箱', '经营范围', '网址']
    exp_header_3 = ['企业名称', '法定代表人', '成立日期', '注册资本', '地址', '邮箱', '经营范围', '网址']
    exp_header_4 = ['企业名称', '法定代表人', '成立日期', '注册资本', '地址', '邮箱', '电话号码', '经营范围', '网址']
    exp_header_5 = ['企业名称', '统一社会信用代码', '法定代表人', '成立日期', '注册资本', '地址', '邮箱', '电话号码', '经营范围', '网址']
    exp_header_6 = ['企业名称', '统一社会信用代码', '法定代表人', '成立日期', '注册资本', '地址', '邮箱', '电话号码', '经营范围', '网址', '电话号码（含更多号码）']
    exp_header_7 = ['企业名称', '省份', '城市', '统一社会信用代码', '法定代表人', '企业类型', '成立日期', '注册资本', '地址', '邮箱', '经营范围', '网址', '电话号码（含更多号码）']

    for i, file_name in enumerate(file_list):
        file_path = os.path.join(base_path, file_name)
        data = xlrd.open_workbook(file_path)  # 打开xls文件
        table = data.sheets()[0]  # 打开第一张表
        # nrows = table.nrows  # 获取表的行数
        header = table.row_values(0)  # 第一行
        if header not in (exp_header_1, exp_header_2, exp_header_3, exp_header_4, exp_header_5, exp_header_6, exp_header_7):
            print("[{}] {}: fail".format(i, file_name))
            print("{} {}".format(len(header), header))
            print("字段与预设的不一致")
            break
        else:
            print("[{}] {}: pass".format(i, file_name))


        # for i in range(nrows):  # 循环逐行打印
        #     if i == 0:  # 跳过第一行
        #         continue
        #     print(table.row_values(i)[:13])  # 取前十三列

    print("file count: {}".format(len(file_list)))


def main():
    exp_header_1 = ['企业名称', '省份', '城市', '统一社会信用代码', '法定代表人', '企业类型', '成立日期', '注册资本', '地址', '邮箱', '经营范围', '网址', '电话号码', '电话号码（更多号码）']
    exp_header_2 = ['企业名称', '法人', '成立日期', '注册资本', '地址', '邮箱', '经营范围', '网址']
    exp_header_3 = ['企业名称', '法定代表人', '成立日期', '注册资本', '地址', '邮箱', '经营范围', '网址']
    exp_header_4 = ['企业名称', '法定代表人', '成立日期', '注册资本', '地址', '邮箱', '电话号码', '经营范围', '网址']
    exp_header_5 = ['企业名称', '统一社会信用代码', '法定代表人', '成立日期', '注册资本', '地址', '邮箱', '电话号码', '经营范围', '网址']

    exp_header_6 = ['企业名称', '统一社会信用代码', '法定代表人', '成立日期', '注册资本', '地址', '邮箱', '电话号码', '经营范围', '网址', '电话号码（含更多号码）']
    exp_header_7 = ['企业名称', '省份', '城市', '统一社会信用代码', '法定代表人', '企业类型', '成立日期', '注册资本', '地址', '邮箱', '经营范围', '网址', '电话号码（含更多号码）']

    print("Connect to mysql...")

    m_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
    m_cursor = m_conn.cursor()
    try:
        file_list = os.listdir(base_path)
        file_list.sort()

        for i, file_name in enumerate(file_list):
            file_path = os.path.join(base_path, file_name)
            data = xlrd.open_workbook(file_path)  # 打开xls文件
            table = data.sheets()[0]  # 打开第一张表
            nrows = table.nrows  # 获取表的行数
            header = table.row_values(0)  # 第一行

            if header == exp_header_1:
                print("{} {} {} {}".format(i, file_name, nrows, "exp_header_1"))
                for j in range(nrows):  # 循环逐行打印
                    if j == 0:  # 跳过第一行
                        continue
                    data_list = table.row_values(j)
                    sql = "insert into qcc_info_1(company_name, province, city, credit_code, legal_person, company_type, establishment_date, registered_capital, address, email, business_scope, site, telephone, more_telephone) VALUE ({})".format(("%s,"*len(exp_header_1))[:-1])
                    m_cursor.execute(sql, data_list)
                m_conn.commit()

            elif header == exp_header_2:
                print("{} {} {} {}".format(i, file_name, nrows, "exp_header_2"))
                for j in range(nrows):  # 循环逐行打印
                    if j == 0:  # 跳过第一行
                        continue
                    data_list = table.row_values(j)
                    sql = "insert into qcc_info_2(company_name, legal_person, establishment_date, registered_capital, address, email, business_scope, site) VALUE ({})".format(("%s,"*len(exp_header_2))[:-1])
                    m_cursor.execute(sql, data_list)
                m_conn.commit()

            elif header == exp_header_3:
                print("{} {} {} {}".format(i, file_name, nrows, "exp_header_3"))
                for j in range(nrows):  # 循环逐行打印
                    if j == 0:  # 跳过第一行
                        continue
                    data_list = table.row_values(j)
                    sql = "insert into qcc_info_3(company_name, legal_person, establishment_date, registered_capital, address, email, business_scope, site) VALUE ({})".format(("%s,"*len(exp_header_3))[:-1])
                    m_cursor.execute(sql, data_list)
                m_conn.commit()

            elif header == exp_header_4:
                print("{} {} {} {}".format(i, file_name, nrows, "exp_header_4"))
                for j in range(nrows):  # 循环逐行打印
                    if j == 0:  # 跳过第一行
                        continue
                    data_list = table.row_values(j)
                    sql = "insert into qcc_info_4(company_name, legal_person, establishment_date, registered_capital, address, email, telephone, business_scope, site) VALUE ({})".format(("%s,"*len(exp_header_4))[:-1])
                    m_cursor.execute(sql, data_list)
                m_conn.commit()

            elif header == exp_header_5:
                print("{} {} {} {}".format(i, file_name, nrows, "exp_header_5"))
                for j in range(nrows):  # 循环逐行打印
                    if j == 0:  # 跳过第一行
                        continue
                    data_list = table.row_values(j)
                    sql = "insert into qcc_info_5(company_name, credit_code, legal_person, establishment_date, registered_capital, address, email, telephone, business_scope, site) VALUE ({})".format(("%s,"*len(exp_header_5))[:-1])
                    m_cursor.execute(sql, data_list)
                m_conn.commit()

            elif header == exp_header_6:
                print("{} {} {} {}".format(i, file_name, nrows, "exp_header_6"))
                for j in range(nrows):  # 循环逐行打印
                    if j == 0:  # 跳过第一行
                        continue
                    data_list = table.row_values(j)
                    sql = "insert into qcc_info_6(company_name, credit_code, legal_person, establishment_date, registered_capital, address, email, telephone, business_scope, site, more_telephone) VALUE ({})".format(("%s,"*len(exp_header_6))[:-1])
                    m_cursor.execute(sql, data_list)
                m_conn.commit()

            elif header == exp_header_7:
                print("{} {} {} {}".format(i, file_name, nrows, "exp_header_7"))
                for j in range(nrows):  # 循环逐行打印
                    if j == 0:  # 跳过第一行
                        continue
                    data_list = table.row_values(j)
                    sql = "insert into qcc_info_7(company_name, province, city, credit_code, legal_person, company_type, establishment_date, registered_capital, address, email, business_scope, site, more_telephone) VALUE ({})".format(("%s,"*len(exp_header_7))[:-1])
                    m_cursor.execute(sql, data_list)
                m_conn.commit()

            else:
                print("{} {} {} {}".format(i, file_name, nrows, "异常状况"))
                raise TypeError("异常状况")

    finally:
        m_cursor.close()
        m_conn.close()
        print("MySQL connection close...")


if __name__ == '__main__':
    mysql_db = "qcc_tyc_index"
    base_path = "/home/nick/Desktop/数据备份/qcc_tyc_download_data/down_file/"
    main()
