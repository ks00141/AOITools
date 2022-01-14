'''
// 211207
 - 10.21.11.210 AOI-Backup 서버에 AOI 작업시마다 Recipe.xml file 변환(recipe name) 및 저장
 - 1시간 마다 변환되게 스케줄러 등록 완료

// 211208
 - FINAL-AOI / PST-AOI split 기능 구현 (root / FINAL or PST)
 - PPID 가운데 layer를 보고 판단함
 - 조건에 안맞는 Reciep는 root 폴더에 그대로 저장
'''
import os
import xml.etree.ElementTree as elemTree
import shutil
import logging
import configparser

# XML File Path Read from filepath_config

config = configparser.ConfigParser()
config.read('convert_config.ini')

root_path = config['path']['root']
pst_dir = config['layer']['pst']
final_dir = config['layer']['final']

#with open('./filepath_config.txt') as file:
#    root_path = file.readline().rstrip()
#    pst_dir = file.readline().rstrip()
#    final_dir = file.readline().rstrip()

# File name len >= 20 --> before convert file
# File name len < 20 --> after convert file

xml_files = [file_name for file_name in os.listdir(root_path) if len(file_name) > 20]
file_info = {}


for xml in xml_files:
    xml_tree = elemTree.parse(os.path.join(root_path,xml))
    cluster_recipe = xml_tree.find("PPID").text
    frontside_recipe = xml_tree.find("FrontsideRecipe").find("RecipeName").text
    device, layer = cluster_recipe.split('\\')[0], cluster_recipe.split('\\')[1]
    file_info[xml] = {'device' : cluster_recipe.split('\\')[0],
                          'cluster_recipe' : cluster_recipe,
                          'frontside_recipe' : frontside_recipe}
    print('{} -> {} convert start in {}'.format(xml,cluster_recipe.split('\\')[0]+'.xml',layer))
    if layer.lower() == 'pst_aoi':
        shutil.move(os.path.join(root_path,xml),os.path.join(root_path,pst_dir,cluster_recipe.split('\\')[0])+'.xml')
    elif layer.lower() == 'final' or layer.lower() == 'final_merge':
        shutil.move(os.path.join(root_path,xml),os.path.join(root_path,final_dir,cluster_recipe.split('\\')[0])+'.xml')
    else:
        shutil.move(os.path.join(root_path,xml),os.path.join(root_path,cluster_recipe.split('\\')[0])+'.xml')