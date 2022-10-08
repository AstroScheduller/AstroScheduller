import os
import datetime
import webbrowser

import tkinter
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename


from . import _srcs

class save():
    def __init__(self, upper):
        self.upper = upper
        self.initialfilename = "MyObservation_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".ash"
        self.filename = asksaveasfilename(filetypes = [("AstroScheduller Files", "*.ash")], defaultextension = ".ash", initialdir = os.getcwd(), initialfile = self.initialfilename)

        if self.filename != "":
            self.upper.scheduller.save(self.filename)
            self.upper.root.title("AstroScheduller - " + self.filename)

class export():
    def __init__(self, upper):
        self.upper = upper
        self.initialfilename = "MyObservation_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
        self.types = [
            {
                "name": "TXT",
                "ext": ".txt",
                "func": self.upper.scheduller.schedule.to_table
            },
            {
                "name": "CSV",
                "ext": ".csv",
                "func": self.upper.scheduller.schedule.to_csv
            }, 
            {
                "name": "HTML",
                "ext": ".html",
                "func": self.upper.scheduller.schedule.to_html
            },
            {
                "name": "JSON",
                "ext": ".json",
                "func": self.upper.scheduller.schedule.to_json
            },
            {
                "name": "XML",
                "ext": ".xml",
                "func": self.upper.scheduller.schedule.to_xml
            }, 
            {
                "name": "LaTex",
                "ext": ".tex",
                "func": self.upper.scheduller.schedule.to_latex
            }
        ]

        filetypes = []
        for i in self.types:
            filetypes.append((i["name"] + " Files", "*" + i["ext"]))

        self.filename = asksaveasfilename(filetypes = filetypes, defaultextension = ".txt", initialdir = os.getcwd(), initialfile = self.initialfilename)
        
        if self.filename != "":
            for i in self.types:
                if self.filename.endswith(i["ext"]):
                    i["func"](self.filename)
                    break