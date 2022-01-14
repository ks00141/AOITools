import configparser

class Configs():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        
        
    def get_path(self, class_name):
        return self.config[class_name.lower()]['path']