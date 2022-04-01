import matplotlib.pyplot as plt
import numpy as np
import math
import time
from .core import core

class plot():
    def __init__(self, self_upper):
        self.observation = self_upper.observation
        self.objects = self_upper.objects
        self.objects_all = self_upper.objects_all

        self.c = core()
        self.slices = 1000
        self.tickes = 10
        self.timestamps = np.linspace(self.observation["duration"]["begin"], self.observation["duration"]["end"], self.slices)

        self.plot()

    def __call__(self):
        self.plot()        

    def plot(self, save=False):
        plt.figure(figsize=[18, 8])

        self.plot_settings()
        self.plot_altitudes()
        self.plot_schedules()

        timeInt = 0
        timeTickes = list()
        timeStrings = list()
        for thisTime in self.timestamps:
            timeInt = timeInt - 1
            if(timeInt <= 0):
                timeTickes.append(thisTime)
                timeStrings.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(thisTime)))
                timeInt = int(self.slices / self.tickes)
        
        plt.xticks(timeTickes, timeStrings, rotation=30, fontsize=5)
        plt.xlabel("Time (s)")
        plt.ylabel("Altitude (deg)")
        plt.title("Altitude vs. Time")
        plt.grid(True, which = "major", alpha = 0.5, linestyle = "-")
        plt.grid(True, which = "minor", alpha = 0.2, linestyle = "--")
        plt.ylim(0, 90)

    def plot_settings(self):
        plt.vlines(self.observation["duration"]["begin"], 0, 90, colors="r", linewidth=2)
        plt.vlines(self.observation["duration"]["end"], 0, 90, colors="r", linewidth=2)
        plt.fill_between([self.observation["duration"]["begin"], self.observation["duration"]["end"]], self.observation["elevation"]["maximal"], 90, color="k", alpha=0.2)
        plt.fill_between([self.observation["duration"]["begin"], self.observation["duration"]["end"]], 0, self.observation["elevation"]["minimal"], color="k", alpha=0.2)
        
        return True

    def plot_schedules(self):
        time = 0
        duration = self.observation["duration"]["end"] - self.observation["duration"]["begin"]

        for thisObj in self.objects_all():
            thisObjAltAz = self.c.go_AltAz(self.observation, thisObj, self.timestamps)
            range = [math.floor(time * self.slices / duration), math.floor((time + thisObj["wait"]) * self.slices / duration)]
            plt.hlines(thisObjAltAz[0][range[1]], self.timestamps[range[0]], self.timestamps[range[1]], colors="k", linewidth=1)
            time = time + thisObj["wait"]

            range = [math.floor(time * self.slices / duration), math.floor((time + thisObj["duration"]) * self.slices / duration)]
            plt.plot(self.timestamps[range[0]: range[1]], thisObjAltAz[0][range[0]: range[1]], label=thisObj["identifier"], linewidth=3)
            plt.text(self.timestamps[range[0]], thisObjAltAz[0][range[0]], thisObj["identifier"], fontsize=5, rotation=0)
            time = time + thisObj["duration"]
        
        return True

    def plot_altitudes(self):
        for thisObj in self.objects_all():
            thisObjAltAz = self.c.go_AltAz(self.observation, thisObj, self.timestamps)
            plt.plot(self.timestamps, thisObjAltAz[0], "k-", linewidth=1, alpha=0.2)
        
        return True
    
    def show(self):
        thisPlt = plt.gcf()

        return thisPlt.show()

    def save(self, savePath):
        return plt.savefig(savePath)
    
    def savefig(self, savePath):
        return self.save(savePath)

class schedule_plot():
    def plot(self):
        return plot(self)