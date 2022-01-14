'''
 // Recipe xml을 읽어서 필요한 항목만 반환
 // 211209
  - Recipe Loader 분리 (Recipe Loader , Model, Xml Parser)
  - xml info
   * Cluster Reicpe = PPID
   * Frontside Recipe = FrontsideRecipe -> RecipeName
   * Number of Inspection pass = number of (FrontsideRecipe -> InspectionPasses ->Item)
   * 1Pass or 2Pass dicision  = The most ROI count in Inspection pass
   * ROI count in Inspection pass = FrontsideRecipe -> InspectionPasses -> Item -> NumberOfROIs
   * Magnification = FrontsideRecipe -> InspectionPasses -> Item -> Magnification
   * Inllumination = FrontsideRecipe -> InspectionPasses -> Item -> IlluminationConfig -> BFIlluminationDesiredGSV
   * InspectionOptions = FrontsideRecipe -> InspectionPasses -> Item -> InspectionOptions

  - Recipe Number Of Inspection Passes view 구현 (not enable pass exception)
'''

import xml.etree.ElementTree as etree
import os
from Configs import Configs

class XmlParser():
    def __init__(self,device,layer = 'final'):

        self.recipe_root_path = Configs().get_path('xmlparser')

        self.device = device
        self.xml_root = None
        self.layer = None
        self.inspection_passes = []

        if layer.lower() == 'pst':
            self.layer = 'PST'
        elif layer.lower() == 'final':
            self.layer = 'FINAL'

        self.set_xml_root()
        self.set_inspection_passes()

    def set_xml_root(self):
        self.xml_root = etree.parse(os.path.join(self.recipe_root_path,self.layer,f'{self.device}.xml'.upper()))

    def set_inspection_passes(self):
        for inspection_passes in self.xml_root.iter('InspectionPasses'):
            self.inspection_passes = [item for item in inspection_passes.findall('Item') if item.find('InspectionPassName').text.find('Not Enabled') < 0]

        self.inspection_passes = sorted(inspection_passes, key = lambda item : int(item.find('NumberOfROIs').text), reverse = True)

    def get_magnification(self,idx):
        return self.inspection_passes[idx].find('Magnification').text

    def get_illumination(self,idx):
        return self.inspection_passes[idx].find('IlluminationConfig').find('BFIlluminationDesiredGSV').text

    def get_inspection_options(self,idx):
        return [inspection_option for inspection_option in self.inspection_passes[idx].find('InspectionOptions').text.split(' ')]

    def get_filelist(self):
        return os.listdir(self.recipe_root_path)


    def get_cluster_recipe(self):
        return self.xml_root.find('PPID').text

    def get_frontside_recipe(self):
        return self.xml_root.find('FrontsideRecipe').find('RecipeName').text

    def get_noip(self):
        return len(self.inspection_passes)

    