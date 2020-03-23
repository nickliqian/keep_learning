# 使用Python将MySQL的数据根据指定规则导入Neo4j
## 1. 初始化db，重启Neo4j数据库，注意这一步会清空数据库所有数据
```
./bin/neo4j stop;rm -rf data/databases/graph.db;./bin/neo4j start
```

## 2. 为Neo4j数据库新建索引，需要依据实际属性的数量
```
create index on :Company(account_id);
create index on :Person(row_key);
```

## 3. 为MySQL数据表新增自增id
```
alter table xxx_table_name add `id` int(11) NOT NULL AUTO_INCREMENT primary key
```

## 4. 分块从MySQL读取数据，根据自增id的范围，步长为10000
```
sql = "select row_key,account_id,cell_no,is_id_match,product_id,response_ref_id,query_time " \
      "from {} " \
      "where id >= (select id from {} " \
      "order by id limit {},1) order by id limit 0, {}".format(table_name, table_name, num_id * step, step)
```

## 5. 把MySQL读取的数据传入写Neo4j的函数，以1000条为一批开始批量导入
```
statement = """MERGE (node1:Person {row_key:{row_key}})
               MERGE (node2:Company {account_id:{account_id}})
               MERGE (node1)<-[:Query {query_time: {query_time}, cell_no: {cell_no}, is_id_match: {is_id_match}, product_id: {product_id}, response_ref_id: {response_ref_id}}]-(node2)"""
```

## 6. 过程中记录各项操作消耗的时间