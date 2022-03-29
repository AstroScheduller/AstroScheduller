import os
from .utilities import utilities

class config():
    def __init__(self):
        self.u = utilities()
        self.platform = self.u.get_platform()
        self.libPath = self.u.get_dir(__file__) + "/rel_lib"
        self.tempPath = self.u.get_dir(__file__) + "/temp"
        self.corePath = self.libPath + "/_scheduller.so"
        self.coreConfigPath = self.libPath + "/_scheduller.config"

        self.check_dir(self.libPath)
        self.check_dir(self.tempPath)

    def check_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

        return True