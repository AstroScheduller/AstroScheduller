'''
Author: your name
Date: 2022-03-17 21:20:04
LastEditTime: 2022-03-17 23:36:34
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /AstroSchedullerGo/Python/core.py
'''

# go build -buildmode=c-shared -o _scheduller.so *.go

import os
import json
from sqlite3 import Timestamp
import requests
import hashlib
import ctypes
from utilities import utilities
from config import config

class core():
    def __init__(self):
        self.c = config()
        self.u = utilities()
        self.coreInfo = {
            "version": "0.9.2",
            "config": False,
            "configUrl": "https://raw.githubusercontent.com/xiawenke/AstroSchedullerGo/Dev/releases_latest/_scheduller.config",
            "corePath": self.c.corePath,
            "configPath": self.c.coreConfigPath
        }
        
        # Check if the AstroSchedullerGo Module exists\
        if(not os.path.isdir(self.u.get_dir(self.coreInfo["corePath"]))):
            os.mkdir(self.u.get_dir(self.coreInfo["corePath"]))
        
        self.get_core_info()
        
        if(not os.path.isfile(self.coreInfo["corePath"])):
            self.download_core()
        
        #self.check_integrity()
    
    def get_core_info(self):
        try:
            self.coreInfo["config"] = json.loads(requests.get(self.coreInfo["configUrl"]).text)
            try:
                self.coreInfo["config"] = self.coreInfo["config"][self.coreInfo["version"]]
            except Exception as e:
                print("get_core_info: AstroSchedullerGo no longer support for version", self.coreInfo["version"])
                exit()
                
        except Exception as e:
            print(str(e), " -> working without internet connection. ")
            
            if(os.path.isfile(self.coreInfo["configPath"])):
                self.coreInfo["config"] = json.loads(open(self.coreInfo["configPath"]).read())
            else:
                print("get_core_info: Need internet to initialize. (If you are working offline, see https://github.com/xiawenke/AstroSchedullerGo for more information.)")
                exit()
        
        open(self.coreInfo["configPath"], "w+").write(json.dumps(self.coreInfo["config"]))
        
        return True
    
    def download_core(self):
        print("Downloading AstroSchedullerGo Module...")
            
        try:
            #open(self.coreInfo["corePath"], "wb").write(requests.get(self.coreInfo["config"]["url"], stream=True).content)
            
            req = requests.get(self.coreInfo["config"]["url"], stream=True)
            with open(self.coreInfo["corePath"], 'wb') as f:
                f.write(req.content)
        except Exception as e:
            print(str(e), " -> AstroSchedullerGo Module does not exists. Try again after check the internet connection. (If you are working offline, see https://github.com/xiawenke/AstroSchedullerGo for more information.)")
            exit()
        
        print("Downloading AstroSchedullerGo Module... Done.")
        return True
    
    def check_integrity(self):
        try:
            if(self.u.md5(open(self.coreInfo["corePath"], "rb").read()).lower() == (self.coreInfo["config"]["md5"]).lower()):
                # print("check_integrity: pass")
                return True
            else:
                print("check_integrity: not pass")
                self.download_core()
                return self.check_integrity()
        except Exception as e:
            print("check_integrity: not check", str(e))
            return False
    
    def update(self):
        os.unlink(self.coreInfo["corePath"])
        os.unlink(self.coreInfo["configPath"])
        self.__init__()

        return True
    
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
    