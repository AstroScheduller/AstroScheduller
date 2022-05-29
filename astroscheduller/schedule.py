from os import unlink
from .utilities import utilities
from .config import config
from .core import core
from .stats import schedule_stats
from .io import schedule_from, schedule_to
from .schedule_edit import schedule_edit
from .plot import schedule_plot
from .time import time_converter

class schedule_scheduller():
    def schedule(self):
        '''
        Generate a schedule.

        return: True if the schedule was generated, False if not.
        '''

        self.xml = self.to_xml()
        self.core = core()
        self.config = config()

        self.importPath = self.c.tempPath + "/" + self.core.prefix + self.u.md5(self.xml.encode()) + ".xml"
        self.exportPath = self.c.tempPath + "/" + self.core.prefix + self.u.md5(self.xml.encode()) + ".export.xml"
        
        open(self.importPath, "w+").write(self.xml)

        if(self.core.go_schedule(self.importPath, self.exportPath)):
            self.objects = self.get_scheduled_return()
            unlink(self.importPath)
            unlink(self.exportPath)
        else:
            unlink(self.importPath)
            raise Exception("schedule", "failed", self.exportPath)

        return True
    
    def get_scheduled_return(self):
        '''
        Get the scheduled return.

        return: The scheduled return.
        '''

        scheduled = schedule()
        scheduled.from_xml(open(self.exportPath, "r+").read())

        return scheduled.objects

class schedule(schedule_from, schedule_to, schedule_scheduller, schedule_stats, schedule_edit, schedule_plot):
    def __init__(self):
        '''
        Initialize a schedule object.
        '''

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

    def __call__(self):
        '''
        Get the schedule.

        return: The schedule.
        '''

        return self.to_dict()
    
    def __str__(self):
        '''
        Get the schedule as string.

        return: The schedule as string.
        '''

        return self.to_table()

    def set_duration(self, begin, end, format = "timestamp"):
        '''
        Set the duration of the observation. 
        begin: The begin of the observation. (e.g. 1234567890.0 or "2018-01-01 00:00:00")
        end: The end of the observation. (e.g. 1234567890.0 or "2018-01-01 00:00:00")
        format: The format of the begin and end, default: "Timestamp".

        return: The duration of the observation.
        '''

        begin = time_converter(begin).to_timestamp()
        end = time_converter(end).to_timestamp()

        if(begin < 0):
            raise Exception("begin", begin)

        if(end < 0):
            raise Exception("begin", end)

        self.observation["duration"]["begin"] = int(begin)
        self.observation["duration"]["end"] = int(end)
        
        return self.observation["duration"]

    def set_telescope(self, latitude = 0, longitude = 0, altitude = 0, velocity = [0.5, 0.5]):
        '''
        Set the telescope.
        latitude: The latitude of the telescope in degree. (e.g. "50.0")
        longitude: The longitude of the telescope in degree. (e.g. "10.0")
        altitude: The altitude of the telescope in meters. (e.g. "500.0")
        velocity: The velocity of the telescope, a list: [V_ra, V_dec] in deg./sec.. (e.g. [0.5, 0.5], default: [0.5, 0.5])
        
        return: The telescope object.
        '''

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
        '''
        Set the elevation.
        minimal: The minimal elevation in degree. (5 = minimal elevation 5 degree)
        maximal: The maximal elevation in degree. (90 = maximal elevation 90 degree)

        return: The elevation object.
        '''

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
        '''
        Set the escape (stay away) from celestial objects. 
        Sun: Stay away from the Sun in degree. (0 = no stay away; 5 = stay away from the Sun 5 degree)

        return: The escape object.
        '''
        
        sun = float(sun)

        if(sun < 0 or sun > 90):
            raise Exception("sun", sun)
        
        self.observation["escape"]["sun"] = sun

        return self.observation["escape"]
    
    def add_object(self, identifier = "", ra = 0, dec = 0, duration = 0, weight = 1, important = False, SkyCoord = False, wait = 0):
        '''
        Add an object to the observation.
        identifier: The identifier of the object.(e.g. "M31")
        ra: The right ascension of the object in degree. (e.g. "50.0")
        dec: The declination of the object in degree. (e.g. "10.0")
        duration: The duration of the observation in seconds. (e.g. "3600")
        weight: The weight of the object. (0 - 1.0, default: 1.0)
        important: Is the object important? (True/False, default: False).
        wait: The wait time in seconds. (e.g. "3600")
        SkyCoord (optional): Import from the SkyCoord object. (astropy SkyCoord object, e.g. SkyCoord(ra = 50.0, dec = 10.0, unit = "deg")).

        return: True if the object was added, False if not.
        '''

        if(SkyCoord != False):
            try:
                ra = SkyCoord.ra.deg
                dec = SkyCoord.dec.deg
            except:
                raise Exception("SkyCoord", SkyCoord, "not an astropy SkyCoord object")

        if(identifier == ""):
            try:
                identifier = SkyCoord.name + str(ra) + "-" + str(dec)
            except:
                identifier = "unknown-" + str(ra) + "-" + str(dec)
            

        identifier = self.u.str_format(str(identifier))
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
