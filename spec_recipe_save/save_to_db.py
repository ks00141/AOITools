# recipe.json 파일을 recipe db에 저장 하는 프로그램
# recipe db schema
# recipe
#  └─ spec table
#       ├─ cluster_recipe, varchar(60)
#       └─ frontside_recipe, varchar(60)

import pymysql
import json
import re

# dbinfo.json 파일로부터 설정값 불러오기
db_info = json.load(fp=open('dbinfo.json', 'r', encoding='utf-8'))

# mysql db connection 생성
conn = pymysql.connect(host=db_info['DBIP'],
                       port=db_info['DBPORT'],
                       user=db_info['USER'],
                       password=db_info['PWD'],
                       db=db_info['DBNAME'])
cur = conn.cursor()

# recipes.json 파일 읽기
with open(file='recipes.json', mode='r', encoding='utf-8') as recipe_data:
    data = json.load(recipe_data)

#

# cluster_recipes, frontside_recipes key list 생성
cluster_recipes = list(data.keys())
frontside_recipes = list(data.values())

# 1. Recipe 개별로 다음과 같은 객체를 생성
#       cluster_recipe(Key) : cluster_reicpe(Value)
#       frontside_recipe(Key) : frontside_recipe(Value)
# 2. 객체가 담긴 리스트 생성
recipes = [{'cluster_recipe': cluster, 'frontside_recipe': frontside} for cluster, frontside in zip(cluster_recipes, frontside_recipes)]

# insert query
sql = 'INSERT INTO `spec` VALUES(%(cluster_recipe)s, %(frontside_recipe)s)'
cur.executemany(query=sql,
                args=recipes)
conn.commit()

