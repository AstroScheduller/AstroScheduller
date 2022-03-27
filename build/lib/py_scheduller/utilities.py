import os
import hashlib

class utilities():
    def get_dir(self, filename):
        return os.path.dirname(os.path.realpath(filename))
    
    def md5(self, content):
        return hashlib.md5(content).hexdigest()
    
    def str_format(self, content):
        return content.replace("\n", "").replace("\r", "").replace("\t", "").strip()