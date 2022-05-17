import os
import time
from .utilities import utilities

class config():
    def __init__(self):
        ''' 
        Initialize the config object.
        '''

        self.u = utilities()
        self.platform = self.u.get_platform()
        self.libPath = self.u.get_dir(__file__) + "/ashlib"
        self.tempPath = self.u.get_dir(__file__) + "/ashlib/temp"
        self.corePath = self.libPath + "/_scheduller.so"
        self.coreConfigPath = self.libPath + "/_scheduller.config"
        self.userPath = self.u.get_dir(__file__) + "/user"
        self.userDefinedIOFormatsPath = self.userPath + "/io_formats"

        self.check_dir(self.libPath)
        self.check_dir(self.tempPath)
        self.check_dir(self.userPath)
        self.check_dir(self.userDefinedIOFormatsPath)

    def check_dir(self, path):
        '''
        Check if a directory exists.
        path: The path to the directory.

        return: True if the directory exists, False if not.
        '''

        if not os.path.exists(path):
            os.makedirs(path)

        return True
    
    def auto_clean(self):
        '''
        Clean the temp directory.

        return: True if the directory was cleaned, False if not.
        '''

        for file in os.listdir(self.tempPath):
            if os.path.isfile(os.path.join(self.tempPath, file)):
                if os.stat(os.path.join(self.tempPath, file)).st_mtime < (time.time() - (30 * 24 * 60 * 60)):
                    os.remove(os.path.join(self.tempPath, file))
        return True