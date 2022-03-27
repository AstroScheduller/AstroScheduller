import os
from .utilities import utilities

class config():
    def __init__(self):
        self.u = utilities()
        self.tempPath = self.u.get_dir(__file__) + "/temp"
        self.corePath = self.u.get_dir(__file__) + "/lib/_scheduller.so"
        self.coreConfigPath = self.u.get_dir(__file__) + "/lib/_scheduller.config"

        self.check_dir(self.tempPath)
        self.check_dir(self.corePath)
        self.check_dir(self.coreConfigPath)

    def check_dir(self, path):
        thisDir = path
        if(not os.path.isdir(thisDir)):
            thisDir = self.u.get_dir(thisDir)
        if(not os.path.isdir(thisDir)):
            print("mkdir", thisDir)
            return os.mkdir(path)
        return True