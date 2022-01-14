'''
// 211207
 - 210(AOI-backup)서버 AutoExport 레시피 xml파일로부터 Data 얻도록 개발

// 211208
 - UI에서 AOI-Layer (PST-AOI or FINAL) flag 받으면 알맞는 Layer Recipe 선택해서 cluster / frontside recipe 보여주도록 수정

// 211211
 - UI에서 inspection_passes setting 값 요청시 Model의 inspection_passes의 객체값을 꺼내 반환해주는 api 개발
   1. model 객체의 inspection_pass의 갯수를 획득, 구별
   2. recipe.xml 파일에서 해당하는 inspection_pass의 값을 model 객체의 inspection_pass에 할당
   3. model 객체의 할당된 값을 반환
'''

from Model import Model
from XmlParser import XmlParser
from ParamLoader import ParamLoader

class RecipeLoader():
    def __init__(self,device,layer = 'final'):
        self.xml_root = None

        self.xml_parser = XmlParser(device,layer)
        self.model = Model(noip = self.xml_parser.get_noip())

        self.set_cluster()
        self.set_frontside()
        self.product_name, self.layer_name ,self.recipe= self.model.frontside_recipe.split('\\')
        self.set_inspection_passes()
        try:
            self.param_loader = ParamLoader(self.product_name, self.layer_name)
        except:
            pass
        try:
            self.set_idt()
        except:
            pass
        try:
            self.set_idt_sub()
        except:
            pass
        try:
            self.set_pad()
        except:
            pass
        try:
            self.set_pin_mark()
        except:
            pass

    def run(self):
        self.set_cluster()
        self.set_frontside()

    def set_cluster(self):
        self.model.set_cluster_recipe(self.xml_parser.get_cluster_recipe())
            
    def set_frontside(self):
        self.model.set_frontside_recipe(self.xml_parser.get_frontside_recipe())

    def set_inspection_passes(self):
        for idx in range(self.model.noip):
            self.model.set_magnification(idx = idx, value = self.xml_parser.get_magnification(idx))
            self.model.set_illumination(idx = idx, value = self.xml_parser.get_illumination(idx))
            #self.model.inspection_passes[idx].inspection_options = self.xml_parser.get_inspection_options(idx)

    def set_idt(self):
        self.model.set_idt(self.param_loader.get_idt())

    def set_idt_sub(self):
        self.model.set_idt_sub(self.param_loader.get_idt_sub())

    def set_pad(self):
        self.model.set_pad(self.param_loader.get_pad())

    def set_pin_mark(self):
        self.model.set_pin_mark(self.param_loader.get_pin_mark())

    def get_noip(self):
        return self.model.get_noip()
    
    def get_cluster(self):
        if self.model.cluster_recipe:
            return self.model.get_cluster_recipe()
        else:
            return None

    def get_frontside(self):
        if self.model.frontside_recipe:
            return self.model.get_frontside_recipe()
        else:
            return None

    def get_magnification(self, idx = 0):
        return self.model.get_magnification(idx)

    def get_illumination(self, idx = 0):
        return self.model.get_illumination(idx)

    #def get_inspection_options(self,idx = 0):
    #   return self.model.inspection_passes[idx].inspection_options

    def get_idt(self):
        return self.model.get_idt()

    def get_idt_sub(self):
        return self.model.get_idt_sub()

    def get_pad(self):
        return self.model.get_pad()

    def get_pin_mark(self):
        return self.model.get_pin_mark()

   