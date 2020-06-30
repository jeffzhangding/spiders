# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json

from .database import PostgresqlConnection

pool = PostgresqlConnection(minconn=1, maxconn=10,
                            database='spider', username='postgres',
                            password='redstar123', host='10.2.136.11', port='5432')


class MsjItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 名称
    crafts = scrapy.Field()  # 工艺
    difficult = scrapy.Field()  # 难度
    number_of_people = scrapy.Field()  # 人数
    taste = scrapy.Field()  # 口味
    preparation_time = scrapy.Field()  # 准备时间
    cook_time = scrapy.Field()  # 烹饪时间
    descrip = scrapy.Field()  # 描述
    first_ingredients = scrapy.Field()  # 主料
    second_ingredients = scrapy.Field()  # 辅料
    practice = scrapy.Field()  # 做法
    url = scrapy.Field()  # 对应页面
    category = scrapy.Field()  # 分类

    def save(self):
        """"""
        with pool.cursor() as cr:
            self['first_ingredients'] = json.dumps(self['first_ingredients'])
            self['second_ingredients'] = json.dumps(self['second_ingredients'])
            self['practice'] = self['practice'].replace("'", '"')
            sql = """INSERT INTO  recipe_msj(name, crafts, difficult, number_of_people, taste, 
            preparation_time, cook_time, descrip, first_ingredients, second_ingredients, practice, url, category) 
                    VALUES ('%(name)s', 
                    '%(crafts)s', '%(difficult)s', '%(number_of_people)s', '%(taste)s', '%(preparation_time)s', 
                    '%(cook_time)s', '%(descrip)s', '%(first_ingredients)s', '%(second_ingredients)s', 
                    '%(practice)s', '%(url)s', '%(category)s') """ % dict(self)
            cr.execute(sql)
            # cr.commit()



