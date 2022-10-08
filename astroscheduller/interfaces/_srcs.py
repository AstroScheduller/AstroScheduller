import os

import tkinter
from PIL import Image, ImageTk

class icons():
    def __init__(self):
        self.__dict__["ashrel"] = os.path.dirname(__file__) + "/../ashrel"
        self.__dict__["icons"] = {}
        
        files = os.listdir(self.__dict__["ashrel"])
        for file in files:
            if file.startswith("icon") and file.endswith(".png"):
                self.__dict__["icons"][file.split("_")[1]] = self.__dict__["ashrel"] + "/" + file

    def load(self, path: str) -> tkinter.PhotoImage:
        return tkinter.PhotoImage(file=path)
    
    def __getattr__(self, __name: str) -> any:
        if __name in self.__dict__["icons"]:
            return self.load(self.__dict__["icons"][__name])
        print("[WARNNING] icon '" + __name + "' not found.")
        return None

class colors():
    def __init__(self) -> None:
        self.link = "#004080"

        self.idle = "#4c4c4c"
        self.running = "#804000"
        self.busy = "#800000"
        self.error = "#808000"
        self.success = "#008040"
        self.initialized = "#4c4c4c"
        self.icon_bkg = "#004080"