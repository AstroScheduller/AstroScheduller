import copy
from .stats import scheduller_stats
from .schedule import schedule
from .plot import plot

class scheduller(scheduller_stats, plot):
    def __init__(self):
        self.objects = schedule()
        self.schedule = schedule()

    def get_schedule(self):
        self.schedule = copy.deepcopy(self.objects)
        self.schedule.schedule()

        return self.schedule