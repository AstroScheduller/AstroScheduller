import os
import datetime

class package_info():
    def __init__(self):
        self.version = "unknown"
        self.author = "AstroScheduller Developers"
        self.SP = "AstroScheduller SP"
        self.license = "MIT"
        self.website = "https://github.com/AstroScheduller"

        self.load_version()
        self.load_author()
        self.load_SP()
        self.load_license()
        self.load_website()
    
    def load_version(self):
        try:
            with open(os.path.dirname(__file__) + "/__version__.py") as f:
                self.version = f.read().split("=")[1].strip()[1:-1]
        except Exception as e:
            self.version = "Unknown"

    def load_author(self):
        return "AstroScheduller Developers"
    
    def load_SP(self):
        try:
            with open(os.path.dirname(__file__) + "/__init__.py") as f:
                self.SP = f.read().split("'''")[1]
        except Exception as e:
            self.SP = "*AstroScheduller SP unavailable*"
    
    def load_license(self):
        self.license = "Copyright © 2020-%today, AstroScheduller Developers\nReleased under the MIT License.".replace("%today", str(datetime.date.today().year))
        
    def load_website(self):
        self.website = "https://github.com/AstroScheduller"
    
    def __str__(self):
        return "=" * 90 + "\n" + self.SP + "\n" + "AstroScheduller v" + self.version + "\n" + self.author + "\n" + self.license + "\n" + self.website + "\n" + "=" * 90 + "\n"
    
    def __repr__(self):
        return self.__str__()
    
    def __dict__(self):
        return {"version": self.version, "author": self.author, "SP": self.SP, "license": self.license, "website": self.website}

    def get_version(self):
        return self.version
    
    def get_author(self):
        return self.author
    
    def get_copyright(self):
        return self.license
    
    def get_website(self):
        return self.website