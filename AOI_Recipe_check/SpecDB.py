import pandas as pd
from Configs import Configs

class SpecDB(object):
    def __init__(self):
        self.root = Configs().get_path('specdb')
        self.db = pd.read_excel(self.root)
        self.db.set_index('그룹', inplace)

