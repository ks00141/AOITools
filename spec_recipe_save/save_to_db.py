# recipe.json 파일을 recipe db에 저장 하는 프로그램
# recipe db schema
# recipe
#  └─ spec table
#       ├─ cluster_recipe, varchar(60)
#       └─ frontside_recipe, varchar(60)

import pymysql
import json


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

# cluster_recipes, recipes_values list 생성
cluster_recipes = list(data.keys())
recipes_values = list(data.values())
values_key = list(recipes_values[0])
# for i in range(len(cluster_recipes)):
#     recipes.update(
#         {'cluster_recipe': cluster_recipes[0],
#          'frontsdie_recipe': recipes_values[0][values_key[0]],
#          'inspection_dies': recipes_values[0][values_key[1]],
#          'inspection_columns'
# recipes_values[0][values_key[2]]
#     recipes_values[0][values_key[3]]

print(list(data.values())[0])
# 1. Recipe 개별로 다음과 같은 객체를 생성
#       cluster_recipe(Key) : cluster_reicpe(Value)
#       frontside_recipe(Key) : frontside_recipe(Value)
# 2. 객체가 담긴 리스트 생성
# recipes = [{'cluster_recipe': cluster, 'frontside_recipe': frontside} for cluster, frontside in zip(cluster_recipes, frontside_recipes)]



# insert query
sql = f'INSERT INTO `spec` VALUES(%(cluster_recipe)s, %(frontside_recipe)s, %(inspection_dies)s, %(inspection_columns)s, %(inspection_rows)s) '    # excutemany 할때 dict key값이 들어감
cur.executemany(query=sql,
                args=list(data.values()))

# commit and resource return
conn.commit()
cur.close()
conn.close()

