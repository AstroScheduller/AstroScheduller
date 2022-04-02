import os
import time
from .utilities import utilities

class config():
    def __init__(self):
        self.u = utilities()
        self.platform = self.u.get_platform()
        self.libPath = self.u.get_dir(__file__) + "/ashlib"
        self.tempPath = self.u.get_dir(__file__) + "/ashlib/temp"
        self.corePath = self.libPath + "/_scheduller.so"
        self.coreConfigPath = self.libPath + "/_scheduller.config"

        self.check_dir(self.libPath)
        self.check_dir(self.tempPath)

    def check_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

        return True
    
    def auto_clean(self):
        for file in os.listdir(self.tempPath):
            if os.path.isfile(os.path.join(self.tempPath, file)):
                if os.stat(os.path.join(self.tempPath, file)).st_mtime < (time.time() - (30 * 24 * 60 * 60)):
                    os.remove(os.path.join(self.tempPath, file))
        return True