'''
 // 211209
  - Recipe Object init
  - device : 기종명
  - cluster_recipe : cluster , PPID Recipe
  - frontside_recipe : frontside(inspection) Recipe
  - inspection_passes : inspection pass (1pass / 2pass)

'''

from InspectionPass import InspectionPass

class Model():
    def __init__(self,noip = 2):
        self.device = None
        self.cluster_recipe = None
        self.frontside_recipe = None
        self.noip = noip
        self.inspection_passes = []# = {idx : InspectionPass() for idx in range(number_of_inspection_pass)}
        self.create_inspection_pass()
        self.idt = None
        self.idt_sub = None
        self.pad = None
        self.pin_mark = None
    

    def create_inspection_pass(self):
        for idx in range(self.noip):
            self.inspection_passes.append(InspectionPass())

    def set_cluster_recipe(self,recipe):
        self.cluster_recipe = recipe

    def set_frontside_recipe(self, recipe):
        self.frontside_recipe = recipe

    def set_idt(self,value):
        self.idt = value

    def set_idt_sub(self, value):
        self.idt_sub = value

    def set_pad(self, value):
        self.pad = value

    def set_pin_mark(self,value):
        self.pin_mark = value

    def set_magnification(self, idx, value):
        self.inspection_passes[idx].magnification = value

    def set_illumination(self,idx,value):
        self.inspection_passes[idx].illumination = value

    def get_cluster_recipe(self):
        return self.cluster_recipe

    def get_frontside_recipe(self):
        return self.frontside_recipe

    def get_noip(self):
        return self.noip

    def get_magnification(self,idx):
        return self.inspection_passes[idx].magnification

    def get_illumination(self, idx):
        return self.inspection_passes[idx].illumination

    def get_idt(self):
        return self.idt

    def get_idt_sub(self):
        return self.idt_sub

    def get_pad(self):
        return self.pad

    def get_pin_mark(self):
        return self.pin_mark