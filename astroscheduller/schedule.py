from .utilities import utilities
from .config import config
from .core import core
from .stats import schedule_stats
from .schedule_io import schedule_from, schedule_to
from .schedule_edit import schedule_edit
from .plot import schedule_plot

class schedule_scheduller():
    def schedule(self):
        self.xml = self.to_xml()
        self.core = core()

        self.importPath = self.c.tempPath + "/" + self.u.md5(self.xml.encode()) + ".xml"
        self.exportPath = self.c.tempPath + "/" + self.u.md5(self.xml.encode()) + ".export.xml"
        
        open(self.importPath, "w+").write(self.xml)

        if(self.core.go_schedule(self.importPath, self.exportPath)):
            self.objects = self.get_scheduled_return()
        else:
            raise Exception("schedule", "failed", self.exportPath)

        return True
    
    def get_scheduled_return(self):
        scheduled = schedule()
        scheduled.from_xml(open(self.exportPath, "r+").read())

        return scheduled.objects

class schedule(schedule_from, schedule_to, schedule_scheduller, schedule_stats, schedule_edit, schedule_plot):
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
    
    def add_object(self, identifier = "", ra = 0, dec = 0, duration = 0, weight = 1, important = False, wait = 0):
        identifier = str(identifier)
        ra = float(ra)
        dec = float(dec)
        duration = int(duration)
        weight = float(weight)
        important = bool(int(important)) * 1
        wait = int(wait)

        if(weight > 1 or weight < 0):
            raise Exception("weight", weight)

        self.objects.append({
            "identifier": identifier, 
            "ra": ra, 
            "dec": dec, 
            "duration": duration, 
            "weight": weight, 
            "important": important,
            "wait": wait
        })

        return True
