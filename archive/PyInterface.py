# @Author: Wenke Xia (wxia1@fandm.edu), Xiaorui Lu (xlu47@ucsc.edu)
# @Date: 2021-07-28 21:44:37 
# @Last Modified by:   Wenke Xia 
# @Last Modified time: 2021-07-28 21:44:37 

import os
import json
from posixpath import dirname
from sys import excepthook
import time
import pytz
import tkinter
import subprocess
import xmltodict
import numpy as np
from astropy.time import Time
from astropy import units as u
import matplotlib.pyplot as plt
from datetime import datetime, timezone
from xml.etree.ElementTree import Element
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

class scheduller_ultilities() :
    def Timestamp(self, timestamp):
        utcTime = datetime.fromtimestamp(timestamp).astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
        print("Set time as ", utcTime)
        
        return Time(utcTime, scale='utc')
        # return Time(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)), scale='utc')

class scheduller_load():
    def json(self, filename):
        rawJson = ""
        fileHandler = open(filename, "r")
        while  True:
            # Get next line from file
            line = fileHandler.readline()
            # If line is empty then end of file reached
            if not line :
                break
            thisLineRaw = line.strip()

            thisLine = ""
            for thisChar in thisLineRaw:
                if(thisChar == "#"): # 支持JSON中的注释
                    break
                thisLine = thisLine + thisChar
            rawJson = rawJson + "\n" + thisLine
            # Close Close    
        fileHandler.close()

        return json.loads(rawJson)

class scheduller_format():
    def __init__(self):
        pass
    
    def json2xml(self, json):
        new = self.old2new(scheduller_load().json(json))
        
        objectTexts = ""
        for thisObj in new["sources"]:
            objectTexts = objectTexts + "<object><identifier>&identifier</identifier><ra>&ra</ra><dec>&dec</dec><duration>&duration</duration></object>"
            objectTexts = objectTexts.replace("&identifier", str(thisObj["identifier"]))
            objectTexts = objectTexts.replace("&ra", str(thisObj["ra"]))
            objectTexts = objectTexts.replace("&dec", str(thisObj["dec"]))
            objectTexts = objectTexts.replace("&duration", str(thisObj["duration"]))
            
            try:
                objectTexts = objectTexts.replace("&weight", "<weight>" + str(thisObj["weight"]) + "</weight>")
            except Exception as e:
                objectTexts = objectTexts.replace("&weight", "")
            
            try:
                objectTexts = objectTexts.replace("&force", "<important>" + str(thisObj["force"]) + "</important>")
            except Exception as e:
                objectTexts = objectTexts.replace("&force", "")
            
        text = "<observation><duration><begin>&dur_begin</begin><end>&dur_end</end></duration><telescope><latitude>&lat</latitude><longitude>&lon</longitude><altitude>&alt</altitude><velocity><ra>&velo_ra</ra><dec>&velo_dec</dec></velocity></telescope><elevation><minimal>&elev_min</minimal><maximal>&elev_max</maximal></elevation><escape><sun>&esc_sun</sun></escape></observation>" + "<sources>" + objectTexts + "</sources>"
        text = text.replace("&dur_begin", str(new["observation"]["duration"]["begin"]))
        text = text.replace("&dur_end", str(new["observation"]["duration"]["end"]))
        text = text.replace("&lat", str(new["observation"]["telescope"]["latitude"]))
        text = text.replace("&lon", str(new["observation"]["telescope"]["longitude"]))
        text = text.replace("&alt", str(new["observation"]["telescope"]["altitude"]))
        text = text.replace("&velo_ra", str(new["observation"]["telescope"]["velocity"]["ra"]))
        text = text.replace("&velo_dec", str(new["observation"]["telescope"]["velocity"]["dec"]))
        text = text.replace("&elev_min", str(new["observation"]["elevation"]["minimal"]))
        text = text.replace("&elev_max", str(new["observation"]["elevation"]["maximal"]))
        text = text.replace("&esc_sun", str(new["observation"]["escape"]["sun"]))
        
        text = "<scheduller>" + text + "</scheduller>"
        
        return text
    
    def old2new(self, old):
        observation = {
            "duration": {
                "begin": int(time.mktime(time.strptime(old["obs_start"], "%Y.%m.%d %H:%M:%S"))),
                "end": int(time.mktime(time.strptime(old["obs_end"], "%Y.%m.%d %H:%M:%S")))
            },
            "telescope": {
                "latitude": old["tele_loc"][0],
                "longitude": old["tele_loc"][1],
                "altitude": old["tele_loc"][2],
                "velocity": {
                    "ra": 0.5,
                    "dec": 0.6
                }
            },
            "elevation": {
                "minimal": old["elev_range"][0],
                "maximal": old["elev_range"][1]
            }, 
            "escape": {
                "sun": old["escape_sun"]
            }
        }
        
        objects = list()
        for thisSource in old["sources"]:
            try:
                objects.append({
                    "identifier": thisSource["identifier"],
                    "ra": float(SkyCoord.from_name("PSR" + thisSource["identifier"]).to_string().split(" ")[0]),
                    "dec": float(SkyCoord.from_name("PSR" + thisSource["identifier"]).to_string().split(" ")[1]),
                    "duration": int(thisSource["dur"]),
                    "weight": float(thisSource["weight"]),
                    "force": int(thisSource["force"])
                })
            except Exception as e:
                try:
                    objects.append({
                        "identifier": thisSource["identifier"],
                        "ra": float(SkyCoord.from_name("PSR" + thisSource["identifier"]).to_string().split(" ")[0]),
                        "dec": float(SkyCoord.from_name("PSR" + thisSource["identifier"]).to_string().split(" ")[1]),
                        "duration": int(thisSource["dur"]),
                        "weight": float(thisSource["weight"])
                    })
                except Exception as e:
                    objects.append({
                        "identifier": thisSource["identifier"],
                        "ra": float(SkyCoord.from_name("PSR" + thisSource["identifier"]).to_string().split(" ")[0]),
                        "dec": float(SkyCoord.from_name("PSR" + thisSource["identifier"]).to_string().split(" ")[1]),
                        "duration": int(thisSource["dur"])
                    })
        
        return {"observation": observation, "sources": objects}
            
class scheduller_plot():
    def xml(self, xmlText):
        loadedXml = xmltodict.parse(xmlText)
        
        try:
            objects = loadedXml['scheduller']['sources']['object']
        except Exception as e:
            print("No valid schedule found. Exit.")
            exit()
        
        observation = loadedXml['scheduller']['observation']
        objects = loadedXml['scheduller']['sources']['object']
        self.preview(observation, objects)
            
        return xmltodict.parse(xmlText)
        
    def preview(self, observation, objects):
        points = 1000
        obsDuration = int(observation['duration']['end']) - int(observation['duration']['begin'])
        slices = np.linspace(0, obsDuration, points)
        obsLocation = EarthLocation(lat = float(observation['telescope']['latitude']) * u.deg, lon = float(observation['telescope']['longitude']) * u.deg, height=0 * u.m)
        obsTime = scheduller_ultilities().Timestamp(int(observation['duration']['begin'])) + slices * u.s
        AltAzFrame = AltAz(obstime=obsTime, location=obsLocation)
        
        plt.rcParams['figure.figsize'] = (16,8)
        
        print("Plotting...")
        for thisObj in objects:
            thisCoord = SkyCoord(ra=float(thisObj["ra"]) * u.deg, dec=float(thisObj["dec"]) * u.deg)
            plt.scatter(slices, thisCoord.transform_to(AltAzFrame).alt, lw=0, s=2, c='k', alpha=0.1)
            
        for thisObj in objects:
            obsStartSlice = int(((int(thisObj['Schedule']['Duration'][0]) - int(observation['duration']['begin']))/obsDuration) * points)
            obsEndSlice = int(((int(thisObj['Schedule']['Duration'][1]) - int(observation['duration']['begin']))/obsDuration) * points)
            thisCoord = SkyCoord(ra=float(thisObj["ra"]) * u.deg, dec=float(thisObj["dec"]) * u.deg)
            
            #print(thisObj)
            #print(thisCoord.transform_to(AltAzFrame).alt[obsStartSlice : obsEndSlice])
            
            plt.scatter(slices[obsStartSlice : obsEndSlice], thisCoord.transform_to(AltAzFrame).alt[obsStartSlice : obsEndSlice], lw=2, s=3, alpha=0.85, cmap='coolwarm')
        
        plt.show()

class scheduller_core_controller():
    selectedCore = ""

    def __init__(self, selectedCore = False):
        if(os.path.isfile(self.selectedCore) == False):
            print("Specified core not found... Searching for available cores...")
            selectedCore = self.search_cores()
        self.selectedCore = selectedCore

    def search_cores(self):
        files = os.listdir(dirname(__file__))
        searchedCores = list()
        for thisFile in files: 
            try:
                if(thisFile[0:17] == "AstroSchedullerGo"):
                    searchedCores.append(thisFile)
            except Exception as e:
                pass
        
        if len(searchedCores) > 1:
            while True:
                print("There are several AstroSchedullerGo Core found: ")
                for i in range(len(searchedCores)):
                    print(" ", i+1, searchedCores[i])
                selectedCore = input("Please specify the core to use (1-" + str(i+1) + "): ")

                try:
                    selectedCore = selectedCore.replace(" ", "")

                    if(int(selectedCore) <= 0):
                        raise Exception("NP INPUT")

                    selectedCore = searchedCores[int(selectedCore) - 1]
                    break
                except Exception as e:
                    print("Exception: Unexpected input", selectedCore)
                    print()
        else:
            try:
                selectedCore = searchedCores[0]
            except Exception as e:
                print("No core found... See https://github.com/AstroScheduller/AstroScheduller for documentation.")
                print("Note: The file name of the core should begin with \"AstroSchedullerGo\". E.g.: AstroSchedullerGo_v0_9_1_dev_MacOSX")
                exit()
                
        print("AstroSchedullerGo Core", selectedCore, "been used.")
        self.selectedCore = selectedCore

        return self.selectedCore
    
    def run(self, importXml, exportXml):
        error = False

        command = "./" + self.selectedCore + " \"" + importXml + "\" \"" + exportXml + "\""
        print(command)
        coreProcess = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while coreProcess.poll() is None:
            thisRet = coreProcess.stdout.readline().strip().decode("utf-8", 'ignore')
            print(thisRet)
        
        return subprocess.Popen.poll

# Reference: https://blog.csdn.net/u010039733/article/details/50004831
class DDList(tkinter.Listbox):

    def __init__(self,master,**kw):
        kw['selectmode'] = tkinter.SINGLE
        tkinter.Listbox.__init__(self,master,kw)
        self.bind("<Button-1>",self.setCurrent)
        self.bind("<B1-Motion>",self.shiftSelection)
        self.curIndex = None
    def setCurrent(self,event):
        self.curIndex = self.nearest(event.y)
    def shiftSelection(self,event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1,x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1,x)
            self.curIndex = i

class scheduller_editor():
    def __init__(self, loadedXml):
        tk = tkinter.Tk()
        dd = DDList(tk, height = len(loadedXml['scheduller']['sources']['object']))
        dd.pack()

        for thisObj in loadedXml['scheduller']['sources']['object']:
            dd.insert(tkinter.END, thisObj['identifier'])
        
        tk.mainloop()

#scheduller_editor(xmltodict.parse(open("./tests/psr_list_long.xml.gitignore").read()))

class scheduller():
    loadedObsConfig = ""
    xmlText = ""
    
    def load_from_json(self, filename):
        self.loadedObsConfig = scheduller_format().json2xml(filename)
        return True
    
    def load_from_xml(self, filename):
        self.loadedObsConfig = open(filename).read()
        return True

    def schedule(self):
        importXmlPath = os.path.abspath('./') + "/scheduller_temp"
        exportXmlPath = os.path.abspath('./') + "/scheduller_temp_schedule"
        open(importXmlPath, "w+").write(self.loadedObsConfig.replace("><", ">\n<"))

        controllerHandle = scheduller_core_controller()
        controllerHandle.run(importXmlPath, exportXmlPath)
        
        if(os.path.isfile(exportXmlPath) == False):
            raise Exception("Unexpected return.")
        else:
            self.xmlText = open(exportXmlPath).read()

        return self.xmlText

    def plot(self):
        scheduller_plot().xml(self.xmlText)
    
    def edit(self):
        pass

    def save(self, filename):
        try:
            open(filename, "w+").write(self.xmlText)
            print("Saved as", filename)
        except Exception as e:
            print("Notice: Unable to save as", self.xmlText)
            print("Schedule is print as below:")
            print(self.xmlText)

schedullerHandle = scheduller()
#schedullerHandle.load_from_json("./tests/psr_list_long.txt.gitignore")
schedullerHandle.load_from_xml("./tests/psr_list_debug.xml")
schedullerHandle.schedule()
schedullerHandle.plot()
schedullerHandle.save("./tests/psr_list_debug_schedule.xml")
