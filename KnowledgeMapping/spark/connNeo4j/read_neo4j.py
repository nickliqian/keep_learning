# -*- coding: utf-8 -*-

from py2neo import Graph
import json
import re

graph = Graph("http://192.168.10.74:7474/", username="neo4j", password="123456")

nodes_data = graph.run("MATCH (n) RETURN n").data()
links_data = graph.run("MATCH ()-[r]->() RETURN r").data()


for node in nodes_data:
    labels = list(node["n"].__dict__["_labels"])
    kv = dict(node["n"])
    if "Industry" not in labels:
        continue

    print(labels, kv)





class Neo4jToJson(object):
    """知识图谱数据接口"""

    def __init__(self):
        """初始化数据"""
        # 与neo4j服务器建立连接
        self.graph = Graph("http://IP//:7474", username="neo4j", password="xxxxx")
        self.links = []
        self.nodes = []

    def post(self):
        """与前端交互"""
        # 前端传过来的数据
        select_name = '南京审计大学'
        # 取出所有节点数据
        nodes_data_all = self.graph.run("MATCH (n) RETURN n").data()
        # node名存储
        nodes_list = []
        for node in nodes_data_all:
            nodes_list.append(node['n']['name'])
        # 根据前端的数据，判断搜索的关键字是否在nodes_list中存在，如果存在返回相应数据，否则返回全部数据
        if select_name in nodes_list:
            # 获取知识图谱中相关节点数据
            nodes_data = self.graph.run("MATCH (n)--(b) where n.name='" + select_name + "' return n,b").data()
            links_data = self.graph.run("MATCH (n)-[r]-(b) where n.name='" + select_name + "' return r").data()
            self.get_select_nodes(nodes_data)
        else:
            # 获取知识图谱中所有节点数据
            links_data = self.graph.run("MATCH ()-[r]->() RETURN r").data()
            nodes_data = self.graph.run("MATCH (n) RETURN n").data()
            self.get_all_nodes(nodes_data)

        self.get_links(links_data)

        # 数据格式转换
        neo4j_data = {'links': self.links, 'nodes': self.nodes}
        neo4j_data_json = json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u'')
        return neo4j_data_json

    def get_links(self, links_data):
        """知识图谱关系数据获取"""
        links_data_str = str(links_data)
        links = []
        i = 1
        dict = {}
        # 正则匹配
        links_str = re.sub("[\!\%\[\]\,\。\{\}\-\:\'\(\)\>]", " ", links_data_str).split(' ')
        for link in links_str:
            if len(link) > 1:
                if i == 1:
                    dict['source'] = link
                elif i == 2:
                    dict['name'] = link
                elif i == 3:
                    dict['target'] = link
                    self.links.append(dict)
                    dict = {}
                    i = 0
                i += 1
        return self.links

    def get_select_nodes(self, nodes_data):
        """获取知识图谱中所选择的节点数据"""
        dict_node = {}
        for node in nodes_data:
            name = node['n']['name']
            tag = node['n']['tag']
            dict_node['name'] = name
            dict_node['tag'] = tag
            self.nodes.append(dict_node)
            dict_node = {}
            break
        for node in nodes_data:
            name = node['b']['name']
            tag = node['b']['tag']
            dict_node['name'] = name
            dict_node['tag'] = tag
            self.nodes.append(dict_node)
            dict_node = {}

    def get_all_nodes(self, nodes_data):
        """获取知识图谱中所有节点数据"""
        dict_node = {}
        for node in nodes_data:
            name = node['n']['name']
            tag = node['n']['tag']
            dict_node['name'] = name
            dict_node['tag'] = tag
            self.nodes.append(dict_node)
            dict_node = {}
        return self.nodes

