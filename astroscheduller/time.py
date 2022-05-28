import datetime

class time_converter():
    def __init__(self, timeInput):
        '''
        Initialize the time converter.
        '''
        self.timeInput = timeInput
        self.timeOutput = 0
    
    def is_timestamp(self):
        '''
        Is the time input a timestamp?
        '''
        if(isinstance(self.timeInput, str)):
            try:
                self.timeInput = float(self.timeInput)
            except:
                return False

        if(isinstance(self.timeInput, float) or isinstance(self.timeInput, int)):
            self.timeOutput = self.timeInput
            return True
        else:
            return False

    def is_datetime_object(self):
        '''
        Is the time input a datetime object?
        '''
        if(isinstance(self.timeInput, datetime.datetime)):
            self.timeOutput = self.timeInput.timestamp() # Convert to timestamp.
            return True
        else:
            return False
    
    def is_astropy_time_object(self):
        '''
        Is the time input a astropy time object?
        '''
        try:
            import astropy.time
            if(isinstance(self.timeInput, astropy.time.Time)):
                isoText = self.timeInput.strftime("%Y-%m-%d %H:%M:%S")
                self.timeOutput = datetime.datetime.strptime(isoText + " +0000", "%Y-%m-%d %H:%M:%S %z").timestamp() # Convert to timestamp.
                return True
            else:
                return False
        except:
            return False
            
    def is_iso_string(self):
        '''
        Is the time input a ISO string?
        '''
        if(isinstance(self.timeInput, str)):
            if(self.timeInput.count("-") == 2):
                self.timeOutput = datetime.datetime.strptime(self.timeInput + " +0000", "%Y-%m-%d %H:%M:%S %z").timestamp() # Convert to timestamp.
                return True
            else:
                return False
        else:
            return False

    def to_timestamp(self):
        '''
        Convert the time input to a timestamp.
        '''
        if(self.is_datetime_object()):
            return float(self.timeOutput)
        elif(self.is_astropy_time_object()):
            return float(self.timeOutput)
        elif(self.is_iso_string()):
            return float(self.timeOutput)
        elif(self.is_timestamp()):
            return float(self.timeOutput)
        else:
            raise Exception("timeInput", self.timeInput, "is not a valid time input. AstroScheduller only accepts timestamp, datetime, astropy.time.Time and ISO strings (%Y-%m-%d %H:%M:%S).")
            
