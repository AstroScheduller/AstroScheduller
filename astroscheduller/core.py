# go build -buildmode=c-shared -o _scheduller.so *.go

import os
import json
import requests
import ctypes
import shutil

from sympy import im
from .utilities import utilities
from .config import config

class core():
    def __init__(self):
        self.c = config()
        self.u = utilities()
        self.prefix = "ash.core."
        self.coreInfo = {
            "version": "*",
            "config": False,
            "configUrl": "https://raw.githubusercontent.com/xiawenke/AstroSchedullerGo/Dev/releases_latest/_scheduller.config",
            "platform": self.c.platform,
            "corePath": self.c.corePath,
            "configPath": self.c.coreConfigPath
        }
        
        # Update Core Config
        self.get_core_info()
        
        # Check if the AstroScheduller Core File is Valid
        self.check_integrity()
    
    def get_core_info(self):
        try:
            self.coreInfo["config"] = json.loads(requests.get(self.coreInfo["configUrl"]).text)
            try:
                self.coreInfo["config"] = self.coreInfo["config"][self.coreInfo["version"]][self.coreInfo["platform"]]
            except Exception as e:
                raise Exception("get_core_info", "AstroSchedullerGo no longer support for version", self.coreInfo["version"], self.coreInfo["platform"])
                
        except Exception as e:
            print(str(e), " -> working without internet connection. ")
            
            if(os.path.isfile(self.coreInfo["configPath"])):
                self.coreInfo["config"] = json.loads(open(self.coreInfo["configPath"]).read())
            else:
                raise Exception("get_core_info", "Need internet to initialize. (If you are working offline, see https://github.com/xiawenke/AstroSchedullerGo for more information.)")
        
        open(self.coreInfo["configPath"], "w+").write(json.dumps(self.coreInfo["config"]))
        
        return True
    
    def download_core(self, url = False):
        if(url == False):
            url = self.coreInfo["config"]["url"]

        print("Downloading AstroSchedullerGo Module...")
        print("", "Get ", url)
            
        try:
            req = requests.get(url, stream=True)
            with open(self.coreInfo["corePath"], 'wb') as f:
                f.write(req.content)
        except Exception as e:
            raise Exception(str(e), "AstroSchedullerGo Module does not exists. Try again after check the internet connection. (If you are working offline, see https://github.com/xiawenke/AstroSchedullerGo for more information.)")
        
        print("Downloading AstroSchedullerGo Module... Done.")
        return True
    
    def check_integrity(self):
        if(not os.path.isfile(self.coreInfo["corePath"])):
            print("AstroSchedullerGo Module does not exists. Downloading...")
            self.download_core()

        try:
            if(self.u.md5(open(self.coreInfo["corePath"], "rb").read()).lower() == (self.coreInfo["config"]["md5"]).lower()):
                # print("check_integrity: pass")
                return True
            else:
                print("New version of AstroSchedullerGo Module is available. Update by script 'astroscheduller.core.core().update()'")
                '''
                response = input("Download new version of AstroSchedullerGo Module? (y/n)")

                if (response == "y"):
                    self.download_core()
                    return True
                elif (response == "n"):
                    print("skipped.")
                    return True

                return self.check_integrity()
                '''
        except Exception as e:
            # print("check_integrity: not check", str(e))
            return False
    
    def update(self):
        print("Updating AstroSchedullerGo Module...")

        self.get_core_info() # Update Core Config
        self.download_core() # Download Core
        self.check_integrity() # Check Integrity

        return True

    def install(self, filename):
        print("Installing AstroSchedullerGo Module...")
        print("", "Get ", filename)
            
        if(self.u.is_url(filename)):
            if(self.download_core(url = filename)):
                return True
            else:
                raise Exception("install", "failed to download.")
        elif(self.u.is_filename(filename)):
            try:
                shutil.copyfile(filename, self.coreInfo["corePath"])
                print("Installing AstroSchedullerGo Module from local file... Done.")
                return True
            except IOError as e:
                raise Exception("install", "failed to copy.")
        
    def go_schedule(self, importPath, exportPath):
        goHandle = ctypes.cdll.LoadLibrary(self.coreInfo["corePath"])
        goHandle.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        goHandle.py_schedule(importPath.encode(), exportPath.encode())
        
        if(not os.path.isfile(importPath) or not os.path.isfile(exportPath)):
            return False
        
        return True
    
    def go_AltAz_raw(self, ra, dec, timestamp, tele_lat, tele_long, tele_alt):
        goHandle = ctypes.cdll.LoadLibrary(self.coreInfo["corePath"])
        #goHandle.py_AltAz.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_int64, ctypes.c_float, ctypes.c_float, ctypes.c_float]
        goHandle.py_AltAz.restype = ctypes.c_char_p
        goReturn = goHandle.py_AltAz(str(ra).encode(), str(dec).encode(), str(int(timestamp)).encode(), str(tele_lat).encode(), str(tele_long).encode(), str(tele_alt).encode()).decode()
        
        try:
            return [float(goReturn.split(",")[0]), float(goReturn.split(",")[1])]
        except Exception as e:
            raise Exception("go_AltAz: " + str(e), "unexpected core return")

    def go_AltAz(self, observation, object, timestamps):
        Alts = list()
        Azs = list()

        for timestamp in timestamps:
            thisRes = self.go_AltAz_raw(object["ra"], object["dec"], timestamp, observation["telescope"]["latitude"], observation["telescope"]["longitude"], observation["telescope"]["altitude"])
            Alts.append(thisRes[0])
            Azs.append(thisRes[1])
            
        return [Alts, Azs]