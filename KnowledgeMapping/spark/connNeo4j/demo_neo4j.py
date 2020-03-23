from py2neo import Graph
import time

graph = Graph(
    "http://localhost:7474",
    username="admin",
    password="123"
)


def add_names(items, tx):
    for data in items:
        tx.append(statement, data)
    tx.process()


def main():
    with open("./raw.csv", "r") as f:
        content = f.readlines()

    items = []
    for index, c in enumerate(content):
        print(">>> {}".format(index))
        c = c.strip()

        person_name, person_id, company_name, company_id, company_type, query_time = c.split(",")

        data = {
            "person_name": person_name,
            "person_id": person_id,
            "company_name": company_name,
            "company_id": company_id,
            "company_type": company_type,
            "query_time": query_time,
        }
        items.append(data)

        if index % 1000 == 0:
            tx = graph.begin()
            add_names(items, tx)
            items = []
            tx.commit()


if __name__ == '__main__':
    # ./bin/neo4j stop;rm -rf data/databases/graph.db;./bin/neo4j start
    s = time.time()
    statement = """MERGE (node1:Person {person_name:{person_name}, person_id:{person_id}})
                     MERGE (node2:Company {company_name:{company_name}, company_id:{company_id}, company_type:{company_type}})
                     MERGE (node1)<-[:Query {query_time: {query_time}}]-(node2)
    """
    main()
    e = time.time()
    print("耗时：{}s".format(e-s))