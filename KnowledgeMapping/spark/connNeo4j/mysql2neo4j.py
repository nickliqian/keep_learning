from py2neo import Graph
from py2neo.database.status import ConstraintError
import time
import pymysql
from conf import mysql_conf, neo4j_conf


def add_data(items, tx):
    for data in items:
        tx.run(statement, data)
    tx.process()


def write2neo4j(num, graph, content):
    start = 0
    end = 0
    items = []
    cycle = 0
    total = 1
    for c in content:
        start = time.time()
        row_key, account_id, cell_no, is_id_match, product_id, response_ref_id, query_time = c

        data = {
            "row_key": row_key,
            "account_id": account_id,
            "cell_no": cell_no,
            "is_id_match": is_id_match,
            "product_id": product_id,
            "response_ref_id": response_ref_id,
            "query_time": query_time
        }
        items.append(data)
        if total % neo4j_conf["step"] == 0:
            tx = graph.begin()
            add_data(items, tx)
            count = len(items)
            items = []
            tx.commit()
            end = time.time()
            print("--- Neo4j Write Time: <index:{}-{}> Commit:{} Time:{}".format(num, cycle, count, end-start))
            cycle += 1
        total += 1

    if items:
        tx = graph.begin()
        add_data(items, tx)
        count = len(items)
        tx.commit()
        print("--- Neo4j Write Time: <index:{}-{}> Commit:{} Time:{}".format(num, cycle, count, end-start))


def main():
    # 连接Neo4j
    print("Connect to Neo4j...")
    graph = Graph(
        neo4j_conf["url"],
        username=neo4j_conf["username"],
        password=neo4j_conf["password"]
    )
    print("Create Neo4j index")

    try:
        graph.schema.create_index("Company", "account_id")
        graph.schema.create_index("Person", "row_key")
    except Exception:
        print("Index already exists")

    # 连接MySQL
    print("Connect to MySQL...")
    m_conn = pymysql.connect(
        host=mysql_conf["host"],
        port=mysql_conf["port"],
        user=mysql_conf["user"],
        passwd=mysql_conf["passwd"],
        db=mysql_conf["db"],
        charset=mysql_conf["charset"]
    )
    m_cursor = m_conn.cursor()
    table_name = mysql_conf["table_name"]

    # 循环读取mysql数据
    num_id = 0
    try:
        while True:
            start = time.time()
            sql = "select row_key,account_id,cell_no,is_id_match,product_id,response_ref_id,query_time " \
                  "from {} " \
                  "where id >= (select id from {} " \
                  "order by id limit {},1) order by id limit 0, {}"\
                  .format(table_name, table_name, num_id * mysql_conf["step"], mysql_conf["step"])
            m_cursor.execute(sql)
            query_results = m_cursor.fetchall()
            end = time.time()
            print("Mysql Query Time: <index:{}> Count:{} Time:{}s".format(num_id, len(query_results), end - start))
            if not query_results:
                print("MySQL查询结果为空 id=<{}>".format(num_id))
                break
            else:
                write2neo4j(num_id, graph, query_results)
            num_id += 1
    finally:
        m_cursor.close()
        m_conn.close()
        print("MySQL connection close...")


if __name__ == '__main__':
    # 重启neo4j：./bin/neo4j stop;rm -rf data/databases/graph.db;./bin/neo4j start
    # 字段：row_key, account_id, cell_no, is_id_match, product_id, response_ref_id, query_time
    # 新建索引：create index on :Company(account_id); create index on :Person(row_key);
    s = time.time()
    statement = """MERGE (node1:Person {row_key:{row_key}})
                   MERGE (node2:Company {account_id:{account_id}})
                   MERGE (node1)<-[:Query {query_time: {query_time}, cell_no: {cell_no}, is_id_match: {is_id_match}, product_id: {product_id}, response_ref_id: {response_ref_id}}]-(node2)"""
    main()
    e = time.time()
    print("总耗时：{}s".format(e-s))
