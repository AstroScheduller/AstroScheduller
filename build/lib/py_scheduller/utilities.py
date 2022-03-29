import os
import hashlib

class utilities():
    def get_dir(self, filename):
        return os.path.dirname(os.path.realpath(filename))
    
    def md5(self, content):
        return hashlib.md5(content).hexdigest()
    
    def str_format(self, content):
        return content.replace("\n", "").replace("\r", "").replace("\t", "").strip()
    
    def is_mac(self):
        return os.name == "posix" and os.uname()[0] == "Darwin"
    
    def is_windows(self):
        return os.name == "nt" and os.uname()[0] == "Windows"

    def is_linux(self):
        return os.name == "posix" and os.uname()[0] == "Linux"
    
    def get_platform(self):
        if(self.is_mac()):
            return "darwin"
        elif(self.is_linux()):
            return "linux"
        elif(self.is_windows()):
            return "windows"
        else:
            raise Exception("get_platform", "Unknown platform.")

print(utilities().is_linux())