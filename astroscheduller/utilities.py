import os
import hashlib

class device():
    def is_mac(self):
        '''
        Return True if the platform is Mac.
        
        return: True if the platform is Mac, False if not.
        '''
        
        return os.name == "posix" and os.uname()[0] == "Darwin"
    
    def is_windows(self):
        '''
        Return True if the platform is Windows.
        
        return: True if the platform is Windows, False if not.
        '''
        
        return os.name == "nt" and os.uname()[0] == "Windows"

    def is_linux(self):
        '''
        Return True if the platform is Linux.
        
        return: True if the platform is Linux, False if not.
        '''
        
        return os.name == "posix" and os.uname()[0] == "Linux"

    def get_platform(self):
        '''
        Get the platform of the user system.
        
        return: The platform.
        '''
        
        if(self.is_mac()):
            return "darwin"
        elif(self.is_linux()):
            return "linux"
        elif(self.is_windows()):
            return "windows"
        else:
            return "unknown_platform"

    def is_amd64(self):
        '''
        Return True if the arch is amd64.
        
        return: True if the arch is amd64, False if not.
        '''
        
        return os.uname()[4] == "x86_64"
    
    def is_arm(self):
        '''
        Return True if the arch is arm.
        
        return: True if the arch is arm, False if not.
        '''
        
        return os.uname()[4] == "armv7l"
    
    def is_arm64(self):
        '''
        Return True if the arch is arm64.
        
        return: True if the arch is arm64, False if not.
        '''
        
        return os.uname()[4] == "aarch64"
    
    def is_i386(self):
        '''
        Return True if the arch is i386.
        
        return: True if the arch is i386, False if not.
        '''
        
        return os.uname()[4] == "i386"
    
    def get_arch(self):
        '''
        Get the arch of the user system.
        
        return: The arch.
        '''
        
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
    def package_dir(self):
        '''
        Get the directory of the package.
        
        return: The directory.
        '''
        
        return self.get_dir(__file__)
        
    def get_dir(self, filename):
        '''
        Get the directory of a file.
        filename: The file.

        return: The directory.
        '''

        return os.path.dirname(os.path.realpath(filename))
    
    def md5(self, content):
        '''
        Get the md5 of a string.
        content: The string.
        
        return: The md5.
        '''
        
        return hashlib.md5(content).hexdigest()
    
    def str_format(self, content):
        '''
        Format a string.
        content: The string.
        
        return: The formatted string.
        '''

        if(type(content) is float):
            content = int(content)
        elif(type(content) is bool):
            content = int(content)
        
        return str(content).replace("\n", "").replace("\r", "").replace("\t", "").strip()
    
    def get_platform(self):
        '''
        Get the platform of the user system.
        
        return: The platform.
        '''
        
        return device().get_platform() + "/" + device().get_arch()
    
    def is_url(self, url):
        '''
        Return True if the text is a url.
        
        return: True if the text is a url, False if not.
        '''
        
        try:
            return url.startswith("http://") or url.startswith("https://")
        except Exception as e:
            return False
    
    def is_file(self, filename):
        '''
        Return True if the text is a filename.
        
        return: True if the text is a filename, False if not.
        '''
        
        try:
            return os.path.isfile(filename)
        except Exception as e:
            return False
    
    def is_filename(self, filename):
        '''
        Return True if the text is a filename. As a shortcut. 
        
        return: True if the text is a filename, False if not.
        '''
        
        self.is_file(filename)