from py2neo import Graph
import pandas as pd
from pyspark import SparkContext
from pyspark.sql import SQLContext
from graphframes import GraphFrame


def write2spark(nodes_df, links_df):
    """

    :param nodes_df:
        +---+-------+---+
        | id|   name|age|
        +---+-------+---+
        |  a|  Alice| 34|
    :param links_df:
        +---+---+------------+
        |src|dst|relationship|
        +---+---+------------+
        |  a|  b|      friend|
    :return:
    """
    # spark
    sc = SparkContext("local", appName="mysqltest")
    sc.setCheckpointDir("ccpoint")
    sqlContext = SQLContext(sc)
    nodes_df = sqlContext.createDataFrame(nodes_df)
    links_df = sqlContext.createDataFrame(links_df)

    nodes_df.show()
    links_df.show()

    # ("a", "Alice", 34)
    vertices = nodes_df
    # ("a", "b", "friend")
    edges = links_df
    g = GraphFrame(vertices, edges)
    print(g)
    result = g.connectedComponents()
    result.select("id", "component").orderBy("component").show()


def read4neo4j():
    # neo4j
    graph = Graph("http://192.168.70.40:7474/", username="neo4j", password="123")
    nodes_data = graph.run("MATCH (n) RETURN n.name as id, id(n) as origin_id, labels(n) as labels LIMIT 1000").data()
    links_data = graph.run("MATCH (a)-[r]->(b) RETURN id(a) as src,"
                           " r.funded_amount as funded_amount, r.funded_rate as funded_rate,"
                           " type(r) as relationship, id(b) as dst LIMIT 1000").data()

    nodes_df = pd.DataFrame(nodes_data)
    links_df = pd.DataFrame(links_data)

    print(nodes_df.shape)
    print(links_df.shape)

    return nodes_df, links_df


if __name__ == '__main__':
    nodes_df, links_df = read4neo4j()
    write2spark(nodes_df, links_df)



