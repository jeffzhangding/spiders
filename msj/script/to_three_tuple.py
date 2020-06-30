# coding=gbk
__author__ = 'jeff'

import sys
import os

spider_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

# spider_path = spider_path + os.sep + 'msj'

sys.path.append(spider_path)

from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
import pickle
import json
from tqdm import tqdm
from msj.database import PostgresqlTool
from msj.items import pool

RELATION_NAME = ['烹饪方法', '口味', '分类', '材料']


class MsjDeal(object):

    def to_tuple(self):
        """"""
        recipe_list = self.get_data()
        for i in tqdm(range(len(recipe_list))):
            recipe = recipe_list[i]
        # for recipe in recipe_list:
            start_name = recipe['name'].split('（')[0].split('(')[0]
            if ':' in start_name or '：' in start_name:
                continue
            relation_list = [
                (start_name.strip(), recipe['crafts'].strip(), '烹饪方法'),
                (start_name.strip(), recipe['taste'].strip(), '口味'),
                (start_name.strip(), recipe['category'].strip(), '分类'),
            ]
            first_ingredients = recipe['first_ingredients']
            second_ingredients = recipe['second_ingredients']
            for i in first_ingredients + second_ingredients:
                name = i['name'].split('(')[0].split('（')[0]
                relation_list.append((start_name, name, '材料'))
            # for i in second_ingredients:
            #             #     relation_list.append((start_name, i['name'], '材料'))
            #             # print(relation_list)
            self.batch_insert(relation_list)

    def get_data(self):
        """"""
        with pool.cursor(auto_commit=False) as cr:
            sql = "select * from recipe_msj"
            cr.execute(sql)
            data = PostgresqlTool.get_dicts(cr)
            return data

    def insert_to_db(self, start_name, end_name, relation_name):
        """插入数据库"""
        sql = "INSERT INTO recipe_tuple (start_name, end_name, relation_name) VALUES ('{}', '{}', '{}')".\
            format(start_name, end_name, relation_name)
        with pool.cursor(auto_commit=True) as cr:
            cr.execute(sql)
        return True

    def batch_insert(self, relation_list):
        """批量插入数据库"""
        with pool.cursor(auto_commit=True) as cr:
            for start_name, end_name, relation_name in relation_list:
                sql = "INSERT INTO recipe_tuple (start_name, end_name, relation_name) VALUES ('{}', '{}', '{}')". \
                    format(start_name, end_name, relation_name)
                cr.execute(sql)
        return True


if __name__ == '__main__':
    MsjDeal().to_tuple()





