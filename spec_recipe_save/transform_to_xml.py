# recipe.xml 파일들을 읽어 cluster, frontside recipe의 값만 획득, 하나의 json 파일로 저장하는 프로그램

import os
import re
import json
import xml.etree.ElementTree as et

# 설정파일(JSON) 읽기
with open('config.json') as config:
    conf = json.load(config)
    ROOT_DIR = conf['ROOTDIR']
    RE_PATTERN = conf['REXPATTERN']

# DIR 필터링을 위한 정규식 패턴 준비
p = re.compile(RE_PATTERN)

# XML DIR 설정
DIRS = [os.path.join(ROOT_DIR, dir) for dir in os.listdir(ROOT_DIR) if p.match(dir)]

# XML file 경로 설정
# sum method 사용하여 2차원 -> 1차원 정렬
files = sum([[os.path.join(dir, file) for file in os.listdir(dir)] for dir in DIRS], [])

cluster_recipe= list()
frontside_recipe = list()
recipes = dict()

# XML 파일 읽기
for file in files:
    xml = et.parse(file)
    root = xml.getroot()
    # PPID tag = cluster recipe
    cluster_recipe.append(re.sub('[\\\\]', '/', root.find("PPID").text))            # 백슬래시는 정규식을 이용하여 / 로 치환
    # frontside recipe
    frontside_recipe.append(
        re.sub('[\\\\]', '/',                                                       # 백슬래시는 정규식을 이용하여 / 로 치환
               root.find("FrontsideRecipe")
               .find("RecipeName")
               .text)
    )

# cluster_recipe : frontside_recipe 형태의 dict 생성
recipes = {clu_recipe: fro_recipe for clu_recipe, fro_recipe in zip(cluster_recipe, frontside_recipe)}

# recipes dict -> recipes.json 파일로 저장
with open('./recipes.json', 'w', encoding='utf-8') as save_file:
    json.dump(recipes, save_file, indent='\t')
