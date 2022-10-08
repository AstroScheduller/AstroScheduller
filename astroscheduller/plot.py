import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import time
import copy
from .core import core

class plot():
    def __init__(self, self_upper, quality="high", engine="ashGo", guimode=False):
        '''
        Initialize the plotter.
        '''

        self.guimode = guimode
        
        self.observation = self_upper.observation
        self.objects = self_upper.objects
        self.objects_all = self_upper.objects_all

        self.c = core()
        self.plt = plt.figure(figsize=self.figsize())
        self.fig = self.plt.subplots()
        self.fontsize = 5

        if(self.guimode):
            print("Plotting in GUI mode. ")
            matplotlib.use("Agg")
            self.plt = plt.figure(facecolor=(236/255, 236/255, 236/255))
            self.fig = self.plt.subplots()
            self.fontsize = 6

        self.slices = 1000
        self.bkgSlices = 1000
        self.tickes = 10
        self.timestamps = []
        self.bkgTimestamps = []
        self.set_quality(quality)

        self.AltAz = self.c.go_AltAz
        self.set_engine(engine)

        self.plot()

    def __call__(self):
        '''
        Call the plotter.
        '''

        self.plot()        
    
    def figsize(self):
        '''
        Get the figure size.
        '''

        obsDuration = self.observation["duration"]["end"] - self.observation["duration"]["begin"]

        return [int(obsDuration/60/60), 8]
    
    def set_engine(self, engine='ashGo'):
        '''
        Set the engine to use.
        engine: astroschedullerGo or astropy.
        '''

        if("ash" in engine.lower() or "astroscheduller" in engine.lower() or "go" in engine.lower()):
            self.AltAz = self.c.go_AltAz
            print("Plotting Engine: astroschedullerGo")
        elif(engine.lower() == "astropy" or "py" in engine.lower()):
            self.AltAz = self.c.astropy_AltAz
            print("Plotting Engine: astropy")
        else:
            print("Error: engine not recognized.")
            return False
            
        return True
    
    def set_quality(self, quality):
        '''
        Set the quality of the plot.
        quality: quality of the plot, max, high, med, low, and quick.
        '''

        if(quality == "maximal" or quality == "maximum"):
            quality = "max"
        elif(quality == "medium"):
            quality = "med"

        self.quality = quality
        obeDuration = self.observation["duration"]["end"] - self.observation["duration"]["begin"]

        self.realObsDuration = {
            "begin": self.observation["duration"]["begin"], 
            "end": 0,
            "length": 0
        }

        for thisObj in self.objects:
            self.realObsDuration["length"] = self.realObsDuration["length"] + thisObj["duration"] + thisObj["wait"]

        self.realObsDuration["end"] = self.realObsDuration["begin"] + self.realObsDuration["length"]

        if(self.realObsDuration["end"] < self.observation["duration"]["end"]):
            self.realObsDuration["end"] = self.observation["duration"]["end"]

        self.realObsDuration["end"] = self.realObsDuration["end"] + 1
        self.realObsDuration["length"] = self.realObsDuration["end"] - self.realObsDuration["begin"]

        if(self.quality == "max"):
            self.slices = int(self.realObsDuration["length"]/60)
            self.bkgSlices = int(self.realObsDuration["length"]/60)
            self.tickes = 10
            self.timestamps = np.linspace(self.realObsDuration["begin"], self.realObsDuration["end"], self.slices)
            self.bkgTimestamps = np.linspace(self.realObsDuration["begin"], self.realObsDuration["end"], self.bkgSlices)
        elif(self.quality == "high"):
            self.slices = int(self.realObsDuration["length"]/300)
            self.bkgSlices = int(self.realObsDuration["length"]/600)
            self.tickes = 10
            self.timestamps = np.linspace(self.realObsDuration["begin"], self.realObsDuration["end"], self.slices)
            self.bkgTimestamps = np.linspace(self.realObsDuration["begin"], self.realObsDuration["end"], self.bkgSlices)
        elif(self.quality == "med"):
            self.slices = int(self.realObsDuration["length"]/600)
            self.bkgSlices = int(self.realObsDuration["length"]/1200)
            self.timestamps = np.linspace(self.realObsDuration["begin"], self.realObsDuration["end"], self.slices)
            self.bkgTimestamps = np.linspace(self.realObsDuration["begin"], self.realObsDuration["end"], self.bkgSlices)
        elif(self.quality == "low"):
            self.slices = int(self.realObsDuration["length"] / 900)
            self.bkgSlices = int(self.realObsDuration["length"] / 2400)
            self.timestamps = np.linspace(self.realObsDuration["begin"], self.realObsDuration["end"], self.slices)
            self.bkgTimestamps = np.linspace(self.realObsDuration["begin"], self.realObsDuration["end"], self.bkgSlices)
        elif(self.quality == "quick"):
            self.slices = int(self.realObsDuration["length"]/600)
            self.bkgSlices = 0
            self.timestamps = np.linspace(self.realObsDuration["begin"], self.realObsDuration["end"], self.slices)
            self.bkgTimestamps = np.linspace(self.realObsDuration["begin"], self.realObsDuration["end"], self.bkgSlices)
        else:
            print("Error: quality not recognized.")
            return False

            
        print("Plotting Quality: " + self.quality)
        return True

    def plot(self, save=False, **kwargs):
        '''
        Plot the schedule.
        save: filename to save the plot to.
        quality: quality of the plot, max, high, med, low.
        '''
        
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
                
        if(kwargs.get("grid", False)):
            self.fig.grid(True, which = "major", alpha = 0.5, linestyle = "-")
            self.fig.grid(True, which = "minor", alpha = 0.2, linestyle = "--")
        
        self.fig.set_xlabel("Time (s)")
        self.fig.set_ylabel("Altitude (deg)")
        self.fig.set_title("Altitude vs. Time")
        self.fig.set_ylim(0, 90)
        
        plt.xticks(timeTickes, timeStrings, rotation=30, fontsize=5)

        if(self.guimode):
            self.fig.patch.set_alpha(0.25)
            plt.tight_layout()

    def plot_settings(self):
        '''
        Plot the settings.
        '''

        self.fig.vlines(self.observation["duration"]["begin"], 0, 90, colors="r", linewidth=1.5)
        self.fig.vlines(self.observation["duration"]["end"], 0, 90, colors="r", linewidth=1.5)
        self.fig.fill_between([self.observation["duration"]["begin"], self.observation["duration"]["end"]], self.observation["elevation"]["maximal"], 90, color="k", alpha=0.2)
        self.fig.fill_between([self.observation["duration"]["begin"], self.observation["duration"]["end"]], 0, self.observation["elevation"]["minimal"], color="k", alpha=0.2)
        
        return True

    def plot_schedules(self):
        '''
        Plot the schedules.
        '''

        time = 0
        duration = self.realObsDuration["end"] - self.realObsDuration["begin"]

        for i in range(len(self.objects_all())):
            thisObj = self.objects_all()[i]
            thisObjAltAz = self.AltAz(self.observation, thisObj, self.timestamps)
            interval = [math.floor(time * self.slices / duration), math.floor((time + thisObj["wait"]) * self.slices / duration)]
            self.fig.hlines(thisObjAltAz[0][interval[1]], self.timestamps[interval[0]], self.timestamps[interval[1]], colors="k", linewidth=1)
            time = time + thisObj["wait"]

            interval = [math.floor(time * self.slices / duration), math.floor((time + thisObj["duration"]) * self.slices / duration)]
            schedLine, = self.fig.plot(self.timestamps[interval[0]: interval[1]], thisObjAltAz[0][interval[0]: interval[1]], label=thisObj["identifier"], linewidth=3)

            self.fig.vlines(self.timestamps[interval[0]], 0, 90, colors="k", linewidth=1, alpha=0.2, linestyles="dotted")
            self.fig.vlines(self.timestamps[interval[1]], 0, 90, colors="k", linewidth=1, alpha=0.2, linestyles="dotted")

            # self.fig.text(self.timestamps[interval[0]], thisObjAltAz[0][interval[0]], "#" + str(i+1) + " " + thisObj["identifier"], fontsize=self.fontsize, rotation=0)
            if(thisObjAltAz[0][interval[0]] < (self.observation["elevation"]["maximal"] - 10)):
                self.fig.text(self.timestamps[interval[0]] + 35, self.observation["elevation"]["maximal"] - 0.5, "(" + str(i) + ") " + thisObj["identifier"], fontsize=self.fontsize, rotation=90, horizontalalignment="left", verticalalignment="top", color="k")
            elif(thisObjAltAz[0][interval[0]] < (self.observation["elevation"]["maximal"] - 5)):
                self.fig.text(self.timestamps[interval[0]] + 35, thisObjAltAz[0][interval[0]] - 0.5, "(" + str(i) + ") " + thisObj["identifier"], fontsize=self.fontsize, rotation=90, horizontalalignment="left", verticalalignment="bottom", color="k")
            else:
                self.fig.text(self.timestamps[interval[0]] + 35, thisObjAltAz[0][interval[0]] - 0.5, "(" + str(i) + ") " + thisObj["identifier"], fontsize=self.fontsize, rotation=90, horizontalalignment="left", verticalalignment="top", color="k")

            if(self.guimode):
                self.fig.fill_between(self.timestamps[interval[0]: interval[1]], self.observation["elevation"]["minimal"], self.observation["elevation"]["maximal"], color=schedLine.get_color(), alpha=0.2)
            
            time = time + thisObj["duration"]
        
        return True

    def plot_altitudes(self):
        '''
        Plot the altitudes.
        '''

        for thisObj in self.objects_all():
            thisObjAltAz = self.AltAz(self.observation, thisObj, self.bkgTimestamps)
            self.fig.plot(self.bkgTimestamps, thisObjAltAz[0], "k-", linewidth=1, alpha=0.2)
        
        return True
    
    def show(self):
        '''
        Show the plot.
        '''

        self.plt.show()

        return True

    def save(self, savePath):
        '''
        Save the plot.
        savePath: path to save the plot to.
        '''
        
        return self.plt.savefig(savePath)
    
    def savefig(self, savePath):
        '''
        Save the plot.
        savePath: path to save the plot to.
        '''

        return self.save(savePath)

class schedule_plot():
    def plot(self, **kwargs):
        '''
        Plot the schedule.
        quality: quality of the plot, max, high, med, low.
        '''

        return plot(self, **kwargs)