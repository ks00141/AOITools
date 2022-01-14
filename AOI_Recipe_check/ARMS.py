import sys
import os
from RecipeLoader import RecipeLoader
import pymysql

layer = 'FINAL'

try:
    device = sys.argv[1]
except:
    print('Need Input Device')

try:
    layer = sys.argv[2]
except:
    pass

try:
    conn = pymysql.connect(host = '10.29.10.54', user = 'root', passwd = 'wisol123', db = 'recipe', port = 3306, charset="utf8")
    cur = conn.cursor()
except:
    pass


os.system('cls')
print('LOAD..')

recipe_loader = RecipeLoader(device = device, layer = layer)
tool_cluster = recipe_loader.get_cluster()
tool_frontside = recipe_loader.get_frontside()
os.system('cls')

try:
    cur.execute('''SELECT CLUSTER_PRODUCT, CLUSTER_LAYER, CLUSTER_NAME, FRONTSIDE_PRODUCT, FRONTSIDE_LAYER, FRONTSIDE_NAME FROM spec WHERE DEVICE = "{}" AND FRONTSIDE_LAYER = "{}";'''.format(device,layer))
    result = cur.fetchone()
    spec_cluster = os.path.join(result[0],result[1],result[2])
    spec_frontside = os.path.join(result[3],result[4],result[5])
except:
    print("Can't Load SPEC")
    spec_cluster = ''
    spec_frontside = ''



print('''
    === ARMS ===


    DEVICE                  :   {}

    AOI LAYER               :   {}

    TOOL RECIPE
        - CLUSTER RECIPE       :   {}
        - FRONTSIDE RECIPE     :   {}

    SPEC RECIPE
        - CLUSTER RECIPE       :   {}
        - FRONTSIDE RECIPE     :   {}

Judgment : {}'''.format(device, layer, tool_cluster, tool_frontside,spec_cluster,spec_frontside,tool_cluster == spec_cluster and tool_frontside == spec_frontside))