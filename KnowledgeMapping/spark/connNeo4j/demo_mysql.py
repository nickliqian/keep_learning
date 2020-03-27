import pymysql


print("Connect to mysql...")
mysql_db = "report_system"
m_conn = pymysql.connect(host='192.168.20.20', port=3306, user='admin', passwd='1qaz@WSX', db=mysql_db, charset='utf8')
m_cursor = m_conn.cursor()

# sql = "select row_key,account_id,cell_no,is_id_match,product_id,response_ref_id,query_time from tb_report_info_test where id >= (select id from {} order by id limit {},1) order by id limit 0, {};".format(name_key_field, mysql_table, mysql_table, i * step, step)
# sql = "select row_key,account_id,cell_no,is_id_match,product_id,response_ref_id,query_time from tb_report_info_test limit {},{}".format(num_id * step, step)

num_id = 0
step = 10000
try:
    while True:
        sql = "select row_key,account_id,cell_no,is_id_match,product_id,response_ref_id,query_time " \
              "from tb_report_info_test limit {},{}".format(num_id*step, step)
        # print("===> {}".format(sql))
        m_cursor.execute(sql)
        query_results = m_cursor.fetchall()
        if not query_results:
            print("MySQL查询结果为空 id=<{}>".format(num_id))
            break
        else:
            for index, result in enumerate(query_results):
                row_key, account_id, cell_no, is_id_match, product_id, response_ref_id, query_time = result
                print(num_id, index, row_key, account_id, cell_no, is_id_match, product_id, response_ref_id, query_time)
        num_id += 1

finally:
    m_cursor.close()
    m_conn.close()
    print("MySQL connection close...")