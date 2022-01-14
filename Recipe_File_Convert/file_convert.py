import os
import xml.etree.ElementTree as elemTree
import shutil
import logging
import configparser

# XML File Path Read from filepath_config

c = configparser.ConfigParser()
c.read('./config.ini')

root_path = c['PATH']['ROOT']
dst_path = c['PATH']['DST']
pst_dir = c['DIRS']['PST']
final_dir = c['DIRS']['FINAL']
temp_dir = c['DIRS']['TEMP']
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
    print('{} -> {} convert start in {}'.format(xml,
                                                cluster_recipe.split('\\')[0]+'.xml',
                                                layer))
    if layer.lower() == 'pst_aoi':
        shutil.move(src=os.path.join(root_path, xml),
                    dst=os.path.join(dst_path, pst_dir, cluster_recipe.split('\\')[0])+'.xml',)
    elif layer.lower() == 'final' or layer.lower() == 'final_merge':
        shutil.move(src=os.path.join(root_path, xml),
                    dst=os.path.join(dst_path, final_dir, cluster_recipe.split('\\')[0])+'.xml',)
    else:
        shutil.move(src=os.path.join(root_path, xml),
                    dst=os.path.join(dst_path, temp_dir, cluster_recipe.split('\\')[0])+'.xml',)
