from urllib import response
from . import object_info

import tkinter
from tkinter import ttk, messagebox


class add_object():
    def __init__(self, upper):
        self.upper = upper
        self.objects = list()
        self.objectsInfo = list()

        self.get_objects()

        self.setup_window()
        self.setup_widgets()

        self.root.mainloop
    
    def get_objects(self):
        self.objects.append("New...")

        for thisObject in self.upper.scheduller.objects_all():
            self.objects.append(thisObject["identifier"])
            self.objectsInfo.append(thisObject)
    
    def setup_window(self):
        self.root = tkinter.Toplevel(self.upper.root)
        self.root.title("Add Object...")
        self.root.geometry("500x100")
        self.root.resizable(False, True)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def setup_widgets(self):
        self.mainInterface = tkinter.Frame(self.root)
        self.mainInterface.pack(pady=10, padx=10, fill="both", expand=True)

        self.actionsInterface = tkinter.Frame(self.root)
        self.actionsInterface.pack(pady=10, padx=10, fill="both", expand=True)

        tkinter.Label(self.mainInterface, text="Select an object: ").grid(row=0, column=0, sticky="w")

        self.objectSelector = ttk.Combobox(self.mainInterface, state="readonly")
        self.objectSelector.grid(row=0, column=1, sticky="w")
        self.objectSelector['value'] = (self.objects)
        self.objectSelector.current(0)

        self.cancelButton = tkinter.Button(self.actionsInterface, text="What is this?", command=self.help)
        self.cancelButton.pack(side="left", fill="x")
        self.comfirmButton = tkinter.Button(self.actionsInterface, text="Confirm", command=self.confirm)
        self.comfirmButton.pack(side="right", fill="x")
        self.cancelButton = tkinter.Button(self.actionsInterface, text="Cancel", command=self.cancel)
        self.cancelButton.pack(side="right", fill="x")
    
    def close(self, event=None):
        self.root.destroy()
        self.upper.root.focus_force()
    
    def confirm(self):
        self.selected = self.objectSelector.get()
        self.selectedObjectInfo = {
            "identifier": "%NEW_OBJECT%", 
            "ra": 0.0,
            "dec": 0.0,
            "duration": 0,
            "weight": 1,
            "important": 0,
            "wait": 0
        }

        for thisObject in self.objectsInfo:
            if(self.selected == thisObject["identifier"]):
                self.selectedObjectInfo = thisObject
                break
        
        self.close()
        new_object(self.upper, self.selectedObjectInfo)
    
    def cancel(self):
        self.close()
    
    def help(self):
        text = "This is the add object window. Here you can add a new object to the scheduller, or select an existing one."
        messagebox.showinfo("Help", text)

class new_object():
    def __init__(self, upper, info):
        self.upper = upper
        self.objects = list()
        self.objectsInfo = list()
        self.newObjectInfo = info

        self.get_objects()

        self.setup_window()
        self.setup_widgets()

        self.root.mainloop

        if(self.newObjectInfo["identifier"] != "%NEW_OBJECT%"):
            self.close()

    def get_objects(self):
        self.objects.append("New...")

        for thisObject in self.upper.scheduller.objects_all():
            self.objects.append(thisObject["identifier"])
            self.objectsInfo.append(thisObject)
    
    def setup_window(self):
        self.root = tkinter.Toplevel(self.upper.root)
        self.root.title("New Object...")
        self.root.geometry("500x100")
        self.root.resizable(False, True)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def setup_widgets(self):
        self.mainInterface = tkinter.Frame(self.root)
        self.mainInterface.pack(pady=10, padx=10, fill="both", expand=True)

        self.actionsInterface = tkinter.Frame(self.root)
        self.actionsInterface.pack(pady=10, padx=10, fill="both", expand=True)

        tkinter.Label(self.mainInterface, text="Object Identifier: ").grid(row=0, column=0, sticky="w")

        self.inputIdentifier = tkinter.Entry(self.mainInterface)
        self.inputIdentifier.grid(row=0, column=1, sticky="w")

        self.cancelButton = tkinter.Button(self.actionsInterface, text="What is this?", command=self.help)
        self.cancelButton.pack(side="left", fill="x")
        self.comfirmButton = tkinter.Button(self.actionsInterface, text="Confirm", command=self.confirm)
        self.comfirmButton.pack(side="right", fill="x")
        self.cancelButton = tkinter.Button(self.actionsInterface, text="Cancel", command=self.cancel)
        self.cancelButton.pack(side="right", fill="x")
    
    def close(self, cancel=False, event=None):
        self.root.destroy()
        self.upper.root.focus_force()

        if(not cancel):
            object_info.get_info(self.upper, self.newObjectInfo, "new", len(self.objectsInfo))
    
    def confirm(self):
        self.newObjectInfo["identifier"] = self.inputIdentifier.get()

        for thisObject in self.objectsInfo:
            if(thisObject["identifier"] == self.newObjectInfo["identifier"]):
                messagebox.showerror("Error", "The identifier \"" + self.newObjectInfo["identifier"] + "\" is already in use. Please choose another one.")
                return

        self.close()
    
    def cancel(self):
        self.close(cancel=True)
    
    def help(self):
        text = "This is the new object window. Here you can add a new object to the scheduller. The identifier is the name of the object, and must be unique."
        messagebox.showinfo("Help", text)