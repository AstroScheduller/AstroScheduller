class ash_item():
    def __init__(self, **kwargs):
        '''
        Initialize an object with default values.
        '''

        self.identifier = ""
        self.ra = 0.0
        self.dec = 0.0
        self.duration = 0
        self.weight = 1.0
        self.important = False
        self.wait = 0.0

        for key, value in kwargs.items():
            if key == "identifier":
                self.set_identifier(value)
            elif key == "ra":
                self.set_ra(value)
            elif key == "dec":
                self.set_dec(value)
            elif key == "duration":
                self.set_duration(value)
            elif key == "weight":
                self.set_weight(value)
            elif key == "important":
                self.set_important(value)
            elif key == "wait":
                self.set_wait(value)
            else:
                print("Unknown key: " + key)

    def __str__(self):
        '''
        Return a string representation of the object.
        '''

        return self.to_string()
        
    def __repr__(self):
        '''
        Return a string representation of the object.
        '''

        return self.to_string()

    def __setitem__(self, key, value):
        '''
        Set the value of the object.
        key: The key.
        value: The value.
        '''

        if key == "identifier":
            self.set_identifier(value)
        elif key == "ra":
            self.set_ra(value)
        elif key == "dec":
            self.set_dec(value)
        elif key == "duration":
            self.set_duration(value)
        elif key == "weight":
            self.set_weight(value)
        elif key == "important":
            self.set_important(value)
        elif key == "wait":
            self.set_wait(value)
        else:
            print("Unknown key: " + key)
    
    def __getitem__(self, key):
        '''
        Return the value of the object.
        key: The key.
        '''

        if key == "identifier":
            return self.get_identifier()
        elif key == "ra":
            return self.get_ra()
        elif key == "dec":
            return self.get_dec()
        elif key == "duration":
            return self.get_duration()
        elif key == "weight":
            return self.get_weight()
        elif key == "important":
            return self.get_important()
        elif key == "wait":
            return self.get_wait()
        else:
            print("Unknown key: " + key)
            return None
    
    @property
    def __call__(self):
        '''
        Return the object.
        '''

        return self.to_dict()
    
    def to_string(self):
        '''
        Return a string representation of the object.
        '''

        return "Object: " + self.identifier + " RA: " + str(self.ra) + " Dec: " + str(self.dec) + " Duration: " + str(self.duration) + " Weight: " + str(self.weight) + " Important: " + str(self.important) + " Wait: " + str(self.wait)
    
    def to_dict(self):
        '''
        Return a dictionary representation of the object.
        '''

        return {
            "identifier": self.identifier,
            "ra": self.ra,
            "dec": self.dec,
            "duration": self.duration,
            "weight": self.weight,
            "important": self.important,
            "wait": self.wait
        }

    def set_identifier(self, identifier = ""):
        '''
        Set the identifier.
        identifier: The identifier.
        '''

        self.identifier = str(identifier)
    
    def set_ra(self, ra = 0.0):
        '''
        Set the right ascension.
        ra: The right ascension in degree.
        '''

        self.ra = float(ra)

    def set_dec(self, dec = 0.0):
        '''
        Set the declination.
        dec: The declination in degree.
        '''

        self.dec = float(dec)

    def set_duration(self, duration = 0):
        '''
        Set the duration.
        duration: The duration in seconds.
        '''

        self.duration = int(duration)
    
    def set_weight(self, weight = 1.0):
        '''
        Set the weight.
        weight: The weight.
        '''

        self.weight = float(weight)
    
    def set_important(self, important = False):
        '''
        Set the important.
        important: Is the object important?
        '''

        self.important = bool(int(important)) * 1

    def set_wait(self, wait = 0.0):
        '''
        Set the wait.
        wait: The wait in seconds.
        '''

        self.wait = float(wait)

    def get_identifier(self):
        '''
        Return the identifier.
        '''

        return self.identifier

    def get_ra(self):
        '''
        Return the right ascension.
        '''

        return self.ra

    def get_dec(self):
        '''
        Return the declination.
        '''

        return self.dec

    def get_duration(self):
        '''
        Return the duration.
        '''

        return self.duration

    def get_weight(self):
        '''
        Return the weight.
        '''

        return self.weight

    def get_important(self):
        '''
        Return the important.
        '''

        return self.important

    def get_wait(self):
        '''
        Return the wait.
        '''

        return self.wait

i = ash_item()
import json
print(json.dumps(i))

class ash_objects():
    def __init__(self):
        '''
        Initialize an object with default values.
        '''

        self.items = []
    
    def __str__(self):
        '''
        Return a string representation of the object.
        '''

        return self.to_string()
    
    def __repr__(self):
        '''
        Return a string representation of the object.
        '''

        return self.to_string()

    def __setitem__(self, key, value):
        '''
        Set the value of the object.
        key: The key.
        value: The value.
        '''

        try:
            self.items[key] = value
        except IndexError:
            print("IndexError: " + str(key))
    
    def __getitem__(self, key):
        '''
        Return the value of the object.
        key: The key.
        '''

        try:
            return self.items[key]
        except IndexError:
            print("IndexError: " + str(key))
            return None

    def __call__(self):
        '''
        Return the object.
        '''

        return self.to_dict()

    def to_string(self):
        """
        Return a string representation of the object.
        """

        str  = ""
        for item in self.items:
            str = item.to_string() + "\n"
        
        return str

    def to_list(self):
        '''
        Return a list representation of the object.
        '''

        list = []
        for item in self.items:
            list.append(item.to_dict())
        
        return list

    def to_dict(self):
        '''
        Return a dictionary representation of the object.
        '''

        return self.to_list()

    def add(self, object = None):
        '''
        Add an object.
        object: The object.
        '''

        if object is None:
            object = ash_item()
        
        self.items.append(object)
    
    def append(self, object = None):
        '''
        Append an object.
        object: The object.
        '''

        self.add(object)
    
    def remove(self, index):
        '''
        Remove an object.
        index: The index.
        '''

        try:
            self.items.pop(index)
        except IndexError:
            print("IndexError: " + str(index))
    
    def clear(self):
        '''
        Clear the object.
        '''

        self.items = []
    
    def get_item(self, index):
        '''
        Return an object.
        index: The index.
        '''

        try:
            return self.items[index]
        except IndexError:
            print("IndexError: " + str(index))
            return None
    
    def length(self):
        '''
        Return the length of the object.
        '''

        return len(self.items)
    
    def len(self):
        '''
        Return the length of the object.
        '''

        return self.length()
