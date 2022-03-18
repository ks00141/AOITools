import numpy as np
import os
import re
import time
from PIL import Image


p = re.compile('[C|F][_]')
root_path = r'C:\Users\wisol\Desktop\python_dev\AOITools\opencv\03161'

file_list = os.listdir(root_path)

file_list = [file for file in file_list if not p.match(file)]

file_list = [file for file in file_list if os.path.isfile(os.path.join(root_path, file))]

start = time.time()
for file in file_list:
    print(file)
    img = Image.open(os.path.join(root_path, file))
    np_img = np.array(img)
    np_img_1d = np_img.mean(axis=2)
    threshold_np = np.where(np_img_1d < 170, 0, np_img_1d)
    threshold_img = Image.fromarray(threshold_np)
    threshold_img = threshold_img.convert('RGB')
    threshold_img.save(os.path.join(root_path, 'C_'+file), format='JPEG')
    os.rename(os.path.join(root_path, file), os.path.join(root_path, 'F_'+file))
end = time.time() - start
print(f"time : {end:.2f}")
