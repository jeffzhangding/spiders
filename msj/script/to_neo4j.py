__author__ = 'jeff'

import sys
import os
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))


from msj.database import PostgresqlTool
from msj.items import pool
from math import ceil
from py2neo import Graph, Node, Relationship
# graph = Graph(password="123", user='neo4j')
from tqdm import tqdm

graph = Graph(password="123", user='neo4j')


def to_neo4j():
    """导入到neo4j"""
    with pool.cursor(auto_commit=False) as cr:
        sql = "select count(*) as c from recipe_tuple"
        cr.execute(sql)
        count_dt = PostgresqlTool.get_dict(cr)
        l = ceil(count_dt['c'] / 100.0)
        for i in tqdm(range(l)):
            sql1 = "select * from recipe_tuple order by id limit %s offset %s" % (100, 100*i)
            cr.execute(sql1)
            dt_list = PostgresqlTool.get_dicts(cr)
            # for dt in dt_list:
            #     tuple_to_neo(dt['start_name'], dt['end_name'], dt['relation_name'])

            data_list = []
            for dt in dt_list:
                data_list.append((dt['start_name'].strip(), dt['end_name'].strip(), dt['relation_name'].strip()))
            tuple_to_neos(data_list)


def tuple_to_neo(start_node, end_node, relation_name):
    with graph.begin() as tx:
        n1 = Node('ShopMall', name=start_node)
        n2 = Node('ShopMall', name=end_node)
        p = Relationship(n1, relation_name, n2)
        tx.merge(p, primary_label=relation_name, primary_key='name')


def tuple_to_neos(data_list):
    with graph.begin() as tx:
        for start_node, end_node, relation_name in data_list:
            n1 = Node('ShopMall', name=start_node)
            n2 = Node('ShopMall', name=end_node)
            p = Relationship(n1, relation_name, n2)
            tx.merge(n1, primary_label='ShopMall', primary_key='name')
            tx.merge(n2, primary_label='ShopMall', primary_key='name')
            tx.merge(p, primary_label=relation_name, primary_key='name')


if __name__ == '__main__':
    to_neo4j()

