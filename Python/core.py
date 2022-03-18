'''
Author: your name
Date: 2022-03-17 21:20:04
LastEditTime: 2022-03-17 22:26:40
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /AstroSchedullerGo/Python/core.py
'''

import os
import json
import requests
import hashlib

class core():
    def __init__(self):
        self.coreInfo = {
            "version": "0.9.2",
            "config": False,
            "configUrl": "https://raw.githubusercontent.com/xiawenke/AstroSchedullerGo/Dev/releases_latest/_scheduller.config",
            "corePath": os.path.abspath(__file__) + "/lib/_scheduller.so",
            "configPath": os.path.abspath(__file__) + "/lib/_scheduller.config"
        }
        
        self.get_core_info()
        
        # Check if the AstroSchedullerGo Module exists
        if(not os.path.isdir(dir(self.coreInfo["corePath"]))):
            os.mkdir(dir(self.coreInfo["corePath"]))
        
        if(not os.path.isfile(self.coreInfo["corePath"])):
            self.download_core()
        
        self.check_integrity()
    
    def get_core_info(self):
        try:
            print(requests.get(self.coreInfo["configUrl"]).text)
            self.coreInfo["config"] = json.loads(requests.get(self.coreInfo["configUrl"]).text)
            try:
                self.coreInfo["config"] = self.coreInfo["config"][self.coreInfo["version"]]
            except Exception as e:
                input("get_core_info: AstroSchedullerGo no longer support for version", self.coreInfo["version"])
                exit()
                
        except Exception as e:
            print(str(e), " -> working without internet connection. ")
            
            if(os.path.isfile(self.coreInfo["configPath"])):
                self.coreInfo["config"] = json.loads(open(self.coreInfo["configPath"]).read())
            else:
                input("get_core_info: Need internet to initialize. (If you are working offline, see https://github.com/xiawenke/AstroSchedullerGo for more information.)")
                exit()
        
        open(self.coreInfo["configPath"], "w+").write(json.dumps(self.coreInfo["config"]))
        
        return True
    
    def download_core(self):
        print("Downloading AstroSchedullerGo Module...")
            
        try:
            open(self.coreInfo["corePath"], "wb").write(requests.get(self.coreInfo["config"]["url"]).text)
        except Exception as e:
            input(e, " -> AstroSchedullerGo Module does not exists. Try again after check the internet connection. (If you are working offline, see https://github.com/xiawenke/AstroSchedullerGo for more information.)")
            exit()
        
        print("Downloading AstroSchedullerGo Module... Done.")
        return True
    
    def check_integrity(self):
        try:
            if(hashlib.md5(open(self.coreInfo["corePath"], "rb").read()) == self.coreInfo["config"]["md5"]):
                print("check_integrity: pass")
                return True
            else:
                print("check_integrity: not pass")
                self.download_core()
                return self.check_integrity()
        except Exception as e:
            print("check_integrity: not check")
            return False
            
core()