import os
import hashlib


class device():
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
            return "unknown_platform"

    def is_amd64(self):
        return os.uname()[4] == "x86_64"
    
    def is_arm(self):
        return os.uname()[4] == "armv7l"
    
    def is_arm64(self):
        return os.uname()[4] == "aarch64"
    
    def is_i386(self):
        return os.uname()[4] == "i386"
    
    def get_arch(self):
        if(self.is_amd64()):
            return "amd64"
        elif(self.is_arm()):
            return "arm"
        elif(self.is_arm64()):
            return "arm64"
        elif(self.is_i386()):
            return "i386"
        else:
            return "unknown_arch"

class utilities():
    def get_dir(self, filename):
        return os.path.dirname(os.path.realpath(filename))
    
    def md5(self, content):
        return hashlib.md5(content).hexdigest()
    
    def str_format(self, content):
        return content.replace("\n", "").replace("\r", "").replace("\t", "").strip()
    
    def get_platform(self):
        return device().get_platform() + "/" + device().get_arch()
    
    def is_url(self, url):
        try:
            return url.startswith("http://") or url.startswith("https://")
        except Exception as e:
            return False
    
    def is_filename(self, filename):
        try:
            return os.path.isfile(filename)
        except Exception as e:
            return False