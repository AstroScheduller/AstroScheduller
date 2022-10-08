import copy

from .stats import scheduller_stats
from .schedule import schedule
from .config import config
from .io import scheduller_io
from .time import time_converter
from .editor import editor
from .info import package_info

class schedule_observation():
    def __init__(self, self_upper):
        self.upper = self_upper
    
    def __call__(self):
        return self.upper.observation
    
    def __str__(self):
        string = ""
        for key in self.upper.observation:
            string += key + ": " + str(self.upper.observation[key]) + "\n"
        return string
    
    def __repr__(self):
        return self.upper.observation

class schedule_set():
    def __init__(self, upper_self):
        '''
        Initialize a schedule observation set object.
        This object is making shortcut to the set observation parameters.
        '''

        self.upper = upper_self
        self.status = {
            "set_duration": False,
            "set_telescope": False,
            "set_elevation": False,
            "set_escape": False
        }
    
    def duration(self, begin, end, format = "timestamp"):
        '''
        Set the duration of the observation. 
        begin: The begin of the observation. (e.g. 1234567890.0 or "2018-01-01 00:00:00")
        end: The end of the observation. (e.g. 1234567890.0 or "2018-01-01 00:00:00")
        format: The format of the begin and end, default: "Timestamp".

        return: The duration of the observation.
        '''

        if(self.status["set_duration"]):
            print("[WARNING] The duration parameters is already set. To update the duration, please use the 'update_duration' function again.")

        return self.upper.set_duration(begin, end, format)
    
    def telescope(self, latitude = 0, longitude = 0, altitude = 0, velocity = [0.5, 0.5]):
        '''
        Set the telescope.
        latitude: The latitude of the telescope in degree. (e.g. "50.0")
        longitude: The longitude of the telescope in degree. (e.g. "10.0")
        altitude: The altitude of the telescope in meters. (e.g. "500.0")
        velocity: The velocity of the telescope, a list: [V_ra, V_dec] in deg./sec.. (e.g. [0.5, 0.5], default: [0.5, 0.5])
        
        return: The telescope object.
        '''

        if(self.status["set_telescope"]):
            print("[WARNING] The telescope parameters is already set. To update the telescope, please use the 'update_telescope' function again.")

        return self.upper.set_telescope(latitude, longitude, altitude, velocity)

    def elevation(self, minimal = 0, maximal = 90):
        '''
        Set the elevation.
        minimal: The minimal elevation in degree. (5 = minimal elevation 5 degree)
        maximal: The maximal elevation in degree. (90 = maximal elevation 90 degree)

        return: The elevation object.
        '''

        if(self.status["set_elevation"]):
            print("[WARNING] The elevation parameters is already set. To update the elevation, please use the 'update_elevation' function again.")

        return self.upper.set_elevation(minimal, maximal)
    
    def escape(self, sun = 0):
        '''
        Set the escape (stay away) from celestial objects. 
        Sun: Stay away from the Sun in degree. (0 = no stay away; 5 = stay away from the Sun 5 degree)

        return: The escape object.
        '''

        if(self.status["set_escape"]):
            print("[WARNING] The escape parameters is already set. To update the escape, please use the 'update_escape' function again.")
        
        return self.upper.set_escape(sun)
    
class schedule_update():
    def __init__(self, upper_self):
        '''
        Initialize a schedule observation set object.
        This object is making shortcut to the update observation parameters.
        '''

        self.upper = upper_self
    
    def duration(self, begin = False, end = False, format = "timestamp"):
        '''
        Update the duration of the observation. 
        begin: The begin of the observation. (e.g. 1234567890.0 or "2018-01-01 00:00:00")
        end: The end of the observation. (e.g. 1234567890.0 or "2018-01-01 00:00:00")
        format: The format of the begin and end, default: "Timestamp".

        return: The duration of the observation.
        '''
        
        if(begin == False):
            begin = self.upper.observation["duration"]["begin"]
        else:
            begin = time_converter(begin).to_timestamp()
        
        if(end == False):
            end = self.upper.observation["duration"]["end"]
        else:
            end = time_converter(end).to_timestamp()

        return self.upper.set_duration(begin, end, "timestamp")

    def telescope(self, latitude = False, longitude = False, altitude = False, velocity = False):
        '''
        Update the telescope.
        latitude: The latitude of the telescope in degree. (e.g. "50.0")
        longitude: The longitude of the telescope in degree. (e.g. "10.0")
        altitude: The altitude of the telescope in meters. (e.g. "500.0")
        velocity: The velocity of the telescope, a list: [V_ra, V_dec] in deg./sec.. (e.g. [0.5, 0.5], default: [0.5, 0.5])
        
        return: The telescope object.
        '''

        if(latitude == False):
            latitude = self.upper.observation["telescope"]["latitude"]
        
        if(longitude == False):
            longitude = self.upper.observation["telescope"]["longitude"]

        if(altitude == False):
            altitude = self.upper.observation["telescope"]["altitude"]

        if(velocity == False):
            velocity = [self.upper.observation["telescope"]["velocity"]["ra"], self.upper.observation["telescope"]["velocity"]["dec"]]

        return self.upper.set_telescope(latitude, longitude, altitude, velocity)

    def elevation(self, minimal = False, maximal = False):
        '''
        Update the elevation.
        minimal: The minimal elevation in degree. (5 = minimal elevation 5 degree)
        maximal: The maximal elevation in degree. (90 = maximal elevation 90 degree)

        return: The elevation object.
        '''

        if(minimal == False):
            minimal = self.upper.observation["elevation"]["minimal"]
        
        if(maximal == False):
            maximal = self.upper.observation["elevation"]["maximal"]

        return self.upper.set_elevation(minimal, maximal)
    
    def escape(self, sun = False):
        '''
        Update the escape (stay away) from celestial objects. 
        Sun: Stay away from the Sun in degree. (0 = no stay away; 5 = stay away from the Sun 5 degree)

        return: The escape object.
        '''

        if(sun == False):
            sun = self.upper.observation["escape"]["sun"]
        
        return self.upper.set_escape(sun)

class schedule_add():
    def __init__(self, upper_self):
        '''
        Initialize a schedule observation set object.
        This object is making shortcut to the add objects.
        '''

        self.upper = upper_self
    
    def object(self, identifier = "", ra = 0, dec = 0, duration = 0, weight = 1, important = False, SkyCoord = False, wait = 0):
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

        return self.upper.add_object(
            identifier = identifier,
            ra = ra,
            dec = dec,
            duration = duration,
            weight = weight,
            important = important,
            SkyCoord = SkyCoord,
            wait = wait
        )

    def item(self, identifier = "", ra = 0, dec = 0, duration = 0, weight = 1, important = False, SkyCoord = False, wait = 0):
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

        return self.object(
            identifier = identifier,
            ra = ra,
            dec = dec,
            duration = duration,
            weight = weight,
            important = important,
            SkyCoord = SkyCoord,
            wait = wait
        )
    
class scheduller(scheduller_stats, scheduller_io):
    def __init__(self):
        '''
        Initialize the scheduller.
        '''

        self.info = package_info()
        self.config = config()
        self.objects = schedule()
        self.schedule = schedule()
        self.set = schedule_set(self.objects)
        self.update = schedule_update(self.objects)
        self.add = schedule_add(self.objects)
        self.observation = schedule_observation(self.objects)

    def get_schedule(self):
        '''
        Generate a schedule.

        return: scheduled schedule. objects.
        '''

        self.schedule = copy.deepcopy(self.objects)
        self.schedule.schedule()

        return self.schedule
    
    def plot(self, **kwargs):
        '''
        Plot the schedule.

        return: plot object.
        '''

        return self.schedule.plot(**kwargs)

    def edit(self):
        '''
        Edit the schedule using AstroScheduller Editor.
        '''

        editor(self)