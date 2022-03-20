from ctypes import util
import json
from math import floor
from pexpect import ExceptionPexpect
from sympy import ExactQuotientFailed, true
from utilities import utilities
from config import config
from core import core
from xml.dom import minidom

class schedule_from():
    def from_xml(self, xmlString):
        xml = minidom.parseString(xmlString)
        node = xml.getElementsByTagName("scheduller")

        # Observation
        observation = node[0].getElementsByTagName("observation")

        ## Duration
        duration = observation[0].getElementsByTagName("duration")
        ### Begin & End
        durationBegin = duration[0].getElementsByTagName("begin")
        durationEnd = duration[0].getElementsByTagName("end")
        ### Set Duration
        self.set_duration(
            begin = durationBegin[0].childNodes[0].nodeValue, 
            end = durationEnd[0].childNodes[0].nodeValue, 
            format = "timestamp"
        )
        
        ## Telescope
        telescope = observation[0].getElementsByTagName("telescope")
        ### Latitude
        telescopeLatitude = telescope[0].getElementsByTagName("latitude")
        ### Longitude
        telescopeLongitude = telescope[0].getElementsByTagName("longitude")
        ### Altitude
        telescopeAltitude = telescope[0].getElementsByTagName("altitude")
        ### Velocity
        telescopeVelocity = telescope[0].getElementsByTagName("velocity")
        #### Ra & Dec
        telescopeVelocityRa = telescopeVelocity[0].getElementsByTagName("ra")
        telescopeVelocityDec = telescopeVelocity[0].getElementsByTagName("dec")
        ### Set Telescope
        self.set_telescope(
            latitude = telescopeLatitude[0].childNodes[0].nodeValue,
            longitude = telescopeLongitude[0].childNodes[0].nodeValue,
            altitude =  telescopeAltitude[0].childNodes[0].nodeValue,
            velocity = [
                telescopeVelocityRa[0].childNodes[0].nodeValue,
                telescopeVelocityDec[0].childNodes[0].nodeValue
            ]
        )

        ## Elevation
        elevation = observation[0].getElementsByTagName("elevation")
        ### Minimal
        elevationMinimal = elevation[0].getElementsByTagName("minimal")
        ### Maximal
        elevationmaximal = elevation[0].getElementsByTagName("maximal")
        ### Set Elevation
        self.set_elevation(
            minimal = elevationMinimal[0].childNodes[0].nodeValue,
            maximal = elevationmaximal[0].childNodes[0].nodeValue
        )

        ## Escape
        escape = observation[0].getElementsByTagName("escape")
        ### Sun
        escapeSun = escape[0].getElementsByTagName("sun")
        ### Set Escape
        self.set_escape(
            sun = escapeSun[0].childNodes[0].nodeValue
        )

        # Sources
        sources = node[0].getElementsByTagName("sources")
        ## Objects
        objects = sources[0].getElementsByTagName("object")
        for thisObj in objects:
            ### Identifier
            identifier = thisObj.getElementsByTagName("identifier")
            ### Ra
            ra = thisObj.getElementsByTagName("ra")
            ### Dec
            dec = thisObj.getElementsByTagName("dec")
            ### Duration
            duration = thisObj.getElementsByTagName("duration")

            ### Weight
            weight = 1
            try:
                weight = thisObj.getElementsByTagName("weight")
            except Exception as e:
                pass

            ### Important
            important = 0
            try:
                important = thisObj.getElementsByTagName("important")
            except Exception as e:
                pass
            
            ### Add Object
            self.add_object(
                identifier = identifier[0].childNodes[0].nodeValue,
                ra = ra[0].childNodes[0].nodeValue,
                dec = dec[0].childNodes[0].nodeValue,
                weight = weight[0].childNodes[0].nodeValue,
                important = important[0].childNodes[0].nodeValue,
            )

class schedule_to():
    def to_dict(self):
        return {
            "observation": self.observation, 
            "object": self.objects
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())

    def to_xml(self):
        xmlHandle = minidom.Document() 
        
        # Observation
        observation = xmlHandle.createElement("observation")

        ## Duration
        duration = xmlHandle.createElement("duration")
        ### Begin
        durationBegin = xmlHandle.createElement("begin")
        durationBegin.appendChild(xmlHandle.createTextNode(str(self.observation["duration"]["begin"])))
        duration.appendChild(durationBegin)
        ### End
        durationEnd = xmlHandle.createElement("end")
        durationEnd.appendChild(xmlHandle.createTextNode(str(self.observation["duration"]["end"])))
        duration.appendChild(durationEnd)

        ## Telescope
        telescope = xmlHandle.createElement("telescope")
        ### Latitude
        telescopeLatitude = xmlHandle.createElement("latitude")
        telescopeLatitude.appendChild(xmlHandle.createTextNode(str(self.observation["telescope"]["latitude"])))
        telescope.appendChild(telescopeLatitude)
        ### Longitude
        telescopeLongitude = xmlHandle.createElement("longitude")
        telescopeLongitude.appendChild(xmlHandle.createTextNode(str(self.observation["telescope"]["longitude"])))
        telescope.appendChild(telescopeLongitude)
        ### Altitude
        telescopeAltitude = xmlHandle.createElement("altitude")
        telescopeAltitude.appendChild(xmlHandle.createTextNode(str(self.observation["telescope"]["altitude"])))
        telescope.appendChild(telescopeAltitude)
        ### Velocity
        telescopeVelocity = xmlHandle.createElement("velocity")
        #### Ra
        telescopeVelocityRa = xmlHandle.createElement("ra")
        telescopeVelocityRa.appendChild(xmlHandle.createTextNode(str(self.observation["telescope"]["velocity"]["ra"])))
        telescopeVelocity.appendChild(telescopeVelocityRa)
        #### Dec
        telescopeVelocityDec = xmlHandle.createElement("dec")
        telescopeVelocityDec.appendChild(xmlHandle.createTextNode(str(self.observation["telescope"]["velocity"]["dec"])))
        telescopeVelocity.appendChild(telescopeVelocityDec)
        telescope.appendChild(telescopeVelocity)

        ## Elevation
        elevation = xmlHandle.createElement("elevation")
        ### Minimal
        elevationMinimal = xmlHandle.createElement("minimal")
        elevationMinimal.appendChild(xmlHandle.createTextNode(str(self.observation["elevation"]["minimal"])))
        elevation.appendChild(elevationMinimal)
        ### Maximal
        elevationMaximal = xmlHandle.createElement("maximal")
        elevationMaximal.appendChild(xmlHandle.createTextNode(str(self.observation["elevation"]["maximal"])))
        elevation.appendChild(elevationMaximal)

        ## Escape
        escape = xmlHandle.createElement("escape")
        ### Minimal
        escapeSun = xmlHandle.createElement("sun")
        escapeSun.appendChild(xmlHandle.createTextNode(str(self.observation["escape"]["sun"])))
        escape.appendChild(escapeSun)
        
        observation.appendChild(duration)
        observation.appendChild(telescope)
        observation.appendChild(elevation)
        observation.appendChild(escape)

        # Objects
        sources = xmlHandle.createElement("sources")
        
        ## Append Objects
        for thisObj in self.objects:
            object = xmlHandle.createElement("object")
            
            ### Identifier
            identifier = xmlHandle.createElement("identifier")
            identifier.appendChild(xmlHandle.createTextNode(str(thisObj['identifier'])))
            object.appendChild(identifier)

            ### Ra
            ra = xmlHandle.createElement("ra")
            ra.appendChild(xmlHandle.createTextNode(str(thisObj['ra'])))
            object.appendChild(ra)

            ### Dec
            dec = xmlHandle.createElement("dec")
            dec.appendChild(xmlHandle.createTextNode(str(thisObj['dec'])))
            object.appendChild(dec)

            ### Duration
            duration = xmlHandle.createElement("duration")
            duration.appendChild(xmlHandle.createTextNode(str(thisObj['duration'])))
            object.appendChild(duration)

            ### Weight
            weight = xmlHandle.createElement("weight")
            weight.appendChild(xmlHandle.createTextNode(str(thisObj['weight'])))
            object.appendChild(weight)

            ### Important
            important = xmlHandle.createElement("important")
            important.appendChild(xmlHandle.createTextNode(str(thisObj['important'])))
            object.appendChild(important)

            sources.appendChild(object)

        xml = xmlHandle.createElement("scheduller")
        xml.appendChild(observation)
        xml.appendChild(sources)

        return xml.toprettyxml()

class schedule_schedule():
    def schedule(self):
        self.xml = self.to_xml()
        self.core = core()

        importPath = self.c.tempPath + "/" + self.u.md5(self.xml.encode()) + ".xml"
        exportPath = self.c.tempPath + "/" + self.u.md5(self.xml.encode()) + ".export.xml"
        
        open(importPath, "w+").write(self.xml)

        if(self.core.go_schedule(importPath, exportPath)):
            scheduled = schedule()
            scheduled.from_xml(open(exportPath, "r+").read())
            return scheduled
        else:
            raise Exception("schedule", "failed")

        return True

class schedule_stats():
    def obj_num(self):
        return len(self.objects)

    def obs_len(self):
        duration = 0

        for thisObj in self.objects:
            duration = duration + thisObj["duration"]
        
        return duration
    
    def obj_ids(self):
        ids = list()

        for thisObj in self.objects:
            ids.append(thisObj["identifier"])
        
        return ids

class schedule(schedule_from, schedule_to, schedule_schedule, schedule_stats):
    def __init__(self):
        self.u = utilities()
        self.c = config()
        self.observation = dict()
        self.objects = list()

        self.observation = {
            "duration": {
                "begin": 0,
                "end": 0
            }, 
            "telescope": {
                "latitude": 0, 
                "longitude": 0, 
                "altitude": 0, 
                "velocity": {
                    "ra": 0.5, 
                    "dec" : 0.5
                }
            }, 
            "elevation": {
                "minimal": 0, 
                "maximal": 90
            }, 
            "escape": {
                "sun": 0
            }
        }
    
    def set_duration(self, begin, end, format = "timestamp"):
        begin = int(begin)
        end = int(end)

        if(format == "timestamp"):
            if(begin < 0):
                raise Exception("begin", begin)

            if(end < 0):
                raise Exception("begin", end)

            self.observation["duration"]["begin"] = begin
            self.observation["duration"]["end"] = end
        else:
            raise Exception("format", format)
        
        return self.observation["duration"]

    def set_telescope(self, latitude = 0, longitude = 0, altitude = 0, velocity = [0.5, 0.5]):
        latitude = float(latitude)
        longitude = float(longitude)
        altitude = float(altitude)
        velocity[0] = float(velocity[0])
        velocity[1] = float(velocity[1])

        if(latitude < 0 or latitude > 90):
            raise Exception("latitude", latitude)
        
        if(longitude < -180 or longitude > 180):
            raise Exception("longitude", longitude)
        
        if(altitude < 0):
            raise Exception("altitude", altitude)
        
        if(velocity[0] < 0 or velocity[1] < 0 or len(velocity) != 2):
            raise Exception("velocity", velocity)
        
        self.observation["telescope"]["latitude"] = latitude
        self.observation["telescope"]["longitude"] = longitude
        self.observation["telescope"]["altitude"] = altitude
        self.observation["telescope"]["velocity"]["ra"] = velocity[0]
        self.observation["telescope"]["velocity"]["dec"] = velocity[1]

        return self.observation["telescope"]

    def set_elevation(self, minimal = 0, maximal = 90):
        minimal = float(minimal)
        maximal = float(maximal)

        if(minimal < 0):
            raise Exception("minimal", minimal)

        if(maximal > 90):
            raise Exception("maximal", maximal)
        
        self.observation["elevation"]["minimal"] = minimal
        self.observation["elevation"]["maximal"] = maximal

        return self.observation["elevation"]
    
    def set_escape(self, sun = 0):
        sun = float(sun)

        if(sun < 0 or sun > 90):
            raise Exception("sun", sun)
        
        self.observation["escape"]["sun"] = sun

        return self.observation["escape"]
    
    def add_object(self, identifier = "", ra = 0, dec = 0, duration = 0, weight = 1, important = False):
        identifier = str(identifier)
        ra = float(ra)
        dec = float(dec)
        duration = int(duration)
        weight = float(weight)
        important = bool(int(important)) * 1

        if(weight > 1 or weight < 0):
            raise Exception("weight", weight)

        self.objects.append({
            "identifier": identifier, 
            "ra": ra, 
            "dec": dec, 
            "duration": duration, 
            "weight": weight, 
            "important": important
        })

        return True
        
s = schedule()
s.set_duration(begin = 1627110000, end = 1627196340, format = "timestamp")
s.set_telescope(latitude = 32.7015, longitude = -109.891284, altitude = 3185, velocity = [0.5, 0.6])
s.set_elevation(minimal = 30, maximal = 80)
s.set_escape(sun = 20)
s.add_object(
    identifier= "J0437–4715", 
    ra= "69.3167",
    dec= "-47.2527", 
    duration= "3555"
)
s.add_object(
    identifier= "J1012+5307", 
    ra= "153.13930897",
    dec= "53.11737904", 
    duration= "800", 
    weight= "0.2", 
    important= True
)
# (print(s.to_dict()))
# (print(s.to_json()))
# print(s.to_xml())

coreHandle = core()
coreHandle.update()

s2 = schedule()
s2.from_xml(open("./export.xml").read())
# print(s2.to_xml())
s2_scheduled = s2.schedule()

print(s2.obj_num(), s2_scheduled.obj_num())
print(s2_scheduled.obs_len())
print(s2_scheduled.obj_ids())