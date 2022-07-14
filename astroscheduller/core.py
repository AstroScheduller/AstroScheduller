# go build -buildmode=c-shared -o _scheduller.so *.go

import os
import time
import json
import requests
import ctypes
import shutil

try:
    import astropy
except ImportError:
    pass

from .utilities import utilities
from .config import config

class core():
    def __init__(self):
        '''
        Initialize Core
        '''

        self.c = config()
        self.u = utilities()
        self.prefix = "ash.core."
        self.coreInfo = {
            "version": "*",
            "config": False,
            "configUrl": "https://raw.githubusercontent.com/xiawenke/AstroScheduller/Dev/releases_latest/_scheduller.config",
            "platform": self.c.platform,
            "corePath": self.c.corePath,
            "configPath": self.c.coreConfigPath
        }

        # Update Core Config
        self.get_core_info()
    
    def get_core_info(self):
        '''
        Get Core Info from the Github

        Return: True if success
        '''

        try:
            self.coreInfo["config"] = json.loads(requests.get(self.coreInfo["configUrl"]).text)
            try:
                self.coreInfo["config"] = self.coreInfo["config"][self.coreInfo["version"]][self.coreInfo["platform"]]
            except Exception as e:
                raise Exception("get_core_info", "The pre-build version of the AstroScheduller Module is not available for this platform. ", self.coreInfo["version"], self.coreInfo["platform"])
                
        except Exception as e:
            print(str(e), " -> working without internet connection. ")
            
            if(os.path.isfile(self.coreInfo["configPath"])):
                self.coreInfo["config"] = json.loads(open(self.coreInfo["configPath"]).read())
            else:
                raise Exception("get_core_info", "Need internet to initialize. (If you are working offline, see https://github.com/AstroScheduller/AstroScheduller for more information.)")
        
        open(self.coreInfo["configPath"], "w+").write(json.dumps(self.coreInfo["config"]))
        
        return True
    
    def download_core(self, url = False):
        '''
        Download Core
        url: url to download from

        Return: True if success
        '''

        print("The AstroSchedullerGo Module will be downloaded. Press Ctrl+C to cancel.")
        time.sleep(3)

        if(url == False):
            url = self.coreInfo["config"]["url"]

        print("Downloading AstroSchedullerGo Module...")
        print("", "Get ", url)
            
        try:
            req = requests.get(url, stream=True)
            with open(self.coreInfo["corePath"], 'wb') as f:
                f.write(req.content)
        except Exception as e:
            print(str(e), "Failed to download the AstroSchedullerGo Module. Try again after check the internet connection. (If you are working offline, see https://github.com/AstroScheduller/AstroScheduller for more information.)")
        
        print("Downloading AstroSchedullerGo Module... Done.")
        return True

    def check_validaity(self, path = False):
        '''
        Check if the AstroScheduller Core File is Valid

        Return: True if passed; False if failed
        '''

        if(path == False):
            path = self.coreInfo["corePath"]

        try:
            ctypes.cdll.LoadLibrary(path)
        except Exception as e:
            return False

        return True
    
    def check_integrity(self):
        '''
        Check if the AstroScheduller Core File is Valid

        Return: True if passed; False if failed
        '''

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
        '''
        Update Core

        Return: True if success
        '''

        print("Updating AstroSchedullerGo Module...")

        self.get_core_info() # Update Core Config
        self.download_core() # Download Core
        self.check_integrity() # Check Integrity

        return True

    def install(self, filename):
        '''
        Install Core from file
        filename: file to install

        Return: True if success
        '''

        print("Installing AstroSchedullerGo Module...")
        print("", "Get ", filename)
            
        if(self.u.is_url(filename)):
            if(self.download_core(url = filename)):
                print("Installing AstroSchedullerGo Module from internet... Done.")
            else:
                raise Exception("install", "failed to download.")
        else:
            filename = os.path.abspath(filename)

            try:
                if(not os.path.isfile(filename)):
                    raise Exception("install", "file does not exists.")

                if(os.path.isfile(self.coreInfo["corePath"])):
                    os.remove(self.coreInfo["corePath"])
                
                shutil.copyfile(filename, self.coreInfo["corePath"])
                print("Installing AstroSchedullerGo Module from local file... Done.")
            except IOError as e:
                raise Exception("install", "failed to copy.")
        
        if(self.check_validaity()):
            return True
        else:
            raise Exception("install", "AstroSchedullerGo Module is invalid.")
        
    def go_schedule(self, importPath, exportPath):
        '''
        GoLang Schedule
        importPath: path to import schedule from
        exportPath: path to export schedule to

        Return: True if success
        '''

        goHandle = ctypes.cdll.LoadLibrary(self.coreInfo["corePath"])
        goHandle.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        goHandle.py_schedule(importPath.encode(), exportPath.encode())
        
        if(not os.path.isfile(importPath) or not os.path.isfile(exportPath)):
            return False
        
        return True
    
    def go_AltAz_raw(self, ra, dec, timestamp, tele_lat, tele_long, tele_alt):
        '''
        GoLang AltAz Raw
        ra: right ascension in degree
        dec: declination in degree
        timestamp: timestamp in unix time
        tele_lat: telescope latitude in degree
        tele_long: telescope longitude in degree
        tele_alt: telescope altitude in meter

        Return: [alt, az]
        '''

        goHandle = ctypes.cdll.LoadLibrary(self.coreInfo["corePath"])
        #goHandle.py_AltAz.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_int64, ctypes.c_float, ctypes.c_float, ctypes.c_float]
        goHandle.py_AltAz.restype = ctypes.c_char_p
        goReturn = goHandle.py_AltAz(str(ra).encode(), str(dec).encode(), str(int(timestamp)).encode(), str(tele_lat).encode(), str(tele_long).encode(), str(tele_alt).encode()).decode()
        
        try:
            return [float(goReturn.split(",")[0]), float(goReturn.split(",")[1])]
        except Exception as e:
            raise Exception("go_AltAz: " + str(e), "unexpected core return")

    def go_AltAz(self, observation, object, timestamps):
        '''
        GoLang AltAz
        observation: observation object
        object: "object" object
        timestamps: timestamps in unix time (list)

        Return: [alts, azs]
        '''

        Alts = list()
        Azs = list()

        for timestamp in timestamps:
            thisRes = self.go_AltAz_raw(object["ra"], object["dec"], timestamp, observation["telescope"]["latitude"], observation["telescope"]["longitude"], observation["telescope"]["altitude"])
            Alts.append(thisRes[0])
            Azs.append(thisRes[1])
            
        return [Alts, Azs]

    def astropy_AltAz(self, observation, object, timestamps):
        '''
        Astropy AltAz
        observation: observation object
        object: "object" object
        timestamps: timestamps in unix time (list)

        Return: [alts, azs]
        '''

        Alts = list()
        Azs = list()

        coord = astropy.coordinates.SkyCoord(ra = object["ra"], dec = object["dec"], unit = "deg", frame = "icrs")
        loc = astropy.coordinates.EarthLocation(lat = observation["telescope"]["latitude"], lon = observation["telescope"]["longitude"], height = observation["telescope"]["altitude"])
        times = astropy.time.Time(timestamps, format = "unix")
        altAzFrame = astropy.coordinates.AltAz(obstime = times, location = loc)

        altAz = coord.transform_to(altAzFrame)
        Alts = altAz.alt.deg
        Azs = altAz.az.deg
        
        return [Alts, Azs]