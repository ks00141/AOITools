'''
 // 211221
  - XML에서 Frontside 레시피에 대한 정보를 가져온 다음 Recipe DB에서 뽑아온 Receie All.xlsx file을 padnas로 열어서
    DB처럼 쓴다
  - 읽어온 데이터는 DataFrame이고, index를 Layer name, Product Name으로 이중 인덱스 구성
  - RecipeLoader로 부터 Frontside Reicpe 에서 Product Name, Leyer Name을 받아와서 DataFrame 조회
  - Defect Bin Name 기준으로 가장 최근일자에 Modify된 row만 남기고 제거
  - SPEC, TOOL Value 비교는 Defect Bin Name : Defect Criteria로 하면 될 듯 하다
  - GUI에는 Defect Criteria 숫자만 보여줘야 할 듯
'''

import pandas as pd
import os
import re
from Configs import Configs

class ParamLoader():
    def __init__(self, product_name, layer_name):
        self.root = Configs().get_path('paramloader')
        self.recipe_db = pd.read_excel(self.root)
        self.recipe_db.set_index(['Product Name','Layer Name'], inplace = True)
        self.recipe_db = self.recipe_db.loc[product_name,layer_name][['Defect Bin Name','Defect Criteria']].drop_duplicates(['Defect Bin Name'], keep = 'last')
        self.recipe_db.set_index('Defect Bin Name', inplace = True)
        


    def get_idt(self):
        value =  self.recipe_db.loc['IDT Defect'].item()
        return re.findall(r'\d+', value)[0]

    def get_idt_sub(self):
        value = self.recipe_db.loc['IDT Defect_sub'].item()
        return re.findall(r'\d+', value)[0]

    def get_pad(self):
        value = self.recipe_db.loc['PAD Defect'].item()
        return re.findall(r'\d+', value)[0]

    def get_pin_mark(self):
        value = self.recipe_db.loc['Probe Mark Area'].item()
        return re.findall(r'\d+', value)[0]