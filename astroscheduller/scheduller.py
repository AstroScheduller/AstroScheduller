import copy
from .stats import scheduller_stats
from .schedule import schedule
from .config import config

class scheduller(scheduller_stats):
    def __init__(self):
        self.config = config()
        self.objects = schedule()
        self.schedule = schedule()

    def get_schedule(self):
        self.schedule = copy.deepcopy(self.objects)
        self.schedule.schedule()

        return self.schedule
    
    def plot(self):
        return self.schedule.plot()