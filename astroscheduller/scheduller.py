import copy
from .stats import scheduller_stats
from .schedule import schedule
from .config import config
from .io import scheduller_io

class scheduller(scheduller_stats, scheduller_io):
    def __init__(self):
        '''
        Initialize the scheduller.
        '''

        self.config = config()
        self.objects = schedule()
        self.schedule = schedule()

    def get_schedule(self):
        '''
        Generate a schedule.

        return: scheduled schedule. objects.
        '''

        self.schedule = copy.deepcopy(self.objects)
        self.schedule.schedule()

        return self.schedule
    
    def plot(self):
        '''
        Plot the schedule.

        return: plot object.
        '''

        return self.schedule.plot()