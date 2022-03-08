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

# insert query
sql = f'INSERT INTO `spec` VALUES(%(cluster_recipe)s, %(frontside_recipe)s, %(inspection_dies)s, %(inspection_columns)s, %(inspection_rows)s) '    # excutemany 할때 dict key값이 들어감
cur.executemany(query=sql,
                args=list(data.values()))

# commit and resource return
conn.commit()
cur.close()
conn.close()

