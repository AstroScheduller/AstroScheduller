import matplotlib.pyplot as plt
import numpy as np
import math
import time
from .core import core

class plot():
    def __init__(self, self_upper):
        '''
        Initialize the plotter.
        '''

        self.observation = self_upper.observation
        self.objects = self_upper.objects
        self.objects_all = self_upper.objects_all

        self.c = core()
        self.slices = 1000
        self.tickes = 10
        self.timestamps = np.linspace(self.observation["duration"]["begin"], self.observation["duration"]["end"], self.slices)

        self.plot()

    def __call__(self):
        '''
        Call the plotter.
        '''

        self.plot()        

    def plot(self, save=False):
        '''
        Plot the schedule.
        save: filename to save the plot to.
        '''
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
        '''
        Plot the settings.
        '''

        plt.vlines(self.observation["duration"]["begin"], 0, 90, colors="r", linewidth=2)
        plt.vlines(self.observation["duration"]["end"], 0, 90, colors="r", linewidth=2)
        plt.fill_between([self.observation["duration"]["begin"], self.observation["duration"]["end"]], self.observation["elevation"]["maximal"], 90, color="k", alpha=0.2)
        plt.fill_between([self.observation["duration"]["begin"], self.observation["duration"]["end"]], 0, self.observation["elevation"]["minimal"], color="k", alpha=0.2)
        
        return True

    def plot_schedules(self):
        '''
        Plot the schedules.
        '''

        time = 0
        duration = self.observation["duration"]["end"] - self.observation["duration"]["begin"]

        for i in range(len(self.objects_all())):
            thisObj = self.objects_all()[i]
            thisObjAltAz = self.c.go_AltAz(self.observation, thisObj, self.timestamps)
            interval = [math.floor(time * self.slices / duration), math.floor((time + thisObj["wait"]) * self.slices / duration)]
            plt.hlines(thisObjAltAz[0][interval[1]], self.timestamps[interval[0]], self.timestamps[interval[1]], colors="k", linewidth=1)
            time = time + thisObj["wait"]

            interval = [math.floor(time * self.slices / duration), math.floor((time + thisObj["duration"]) * self.slices / duration)]
            plt.plot(self.timestamps[interval[0]: interval[1]], thisObjAltAz[0][interval[0]: interval[1]], label=thisObj["identifier"], linewidth=3)
            plt.text(self.timestamps[interval[0]], thisObjAltAz[0][interval[0]], "#" + str(i+1) + " " + thisObj["identifier"], fontsize=5, rotation=0)
            time = time + thisObj["duration"]
        
        return True

    def plot_altitudes(self):
        '''
        Plot the altitudes.
        '''

        for thisObj in self.objects_all():
            thisObjAltAz = self.c.go_AltAz(self.observation, thisObj, self.timestamps)
            plt.plot(self.timestamps, thisObjAltAz[0], "k-", linewidth=1, alpha=0.2)
        
        return True
    
    def show(self):
        '''
        Show the plot.
        '''

        plt.show()

        return True

    def save(self, savePath):
        '''
        Save the plot.
        savePath: path to save the plot to.
        '''
        
        return plt.savefig(savePath)
    
    def savefig(self, savePath):
        '''
        Save the plot.
        savePath: path to save the plot to.
        '''

        return self.save(savePath)

class schedule_plot():
    def plot(self):
        '''
        Plot the schedule.
        '''

        return plot(self)