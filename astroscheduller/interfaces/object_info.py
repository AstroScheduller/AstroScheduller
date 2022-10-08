import tkinter
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

from . import main
from .. import scheduller

class object_preview(main.previewInterface):
    def update(self, upper):
        pass

class object_info():
    def __init__(self, upper):
        self.upper = upper
        
        self.load()
        self.update()
    
    def load(self):
        self.viewLeft = tkinter.Frame(self.upper.infoInterface)
        self.viewLeft.pack(side="left", fill="both", expand=True)
        self.viewRight = tkinter.Frame(self.upper.infoInterface)
        self.viewRight.pack(side="right", fill="both", expand=True)

        tkinter.Label(self.viewLeft, text="R.A.:").grid(row=0, column=0, sticky="w")
        self.entryRa = tkinter.Entry(self.viewLeft, width=10)
        self.entryRa.grid(row=0, column=1, sticky="w")
        tkinter.Label(self.viewLeft, text="deg.").grid(row=0, column=2, sticky="w")

        tkinter.Label(self.viewLeft, text="Dec.:").grid(row=1, column=0, sticky="w")
        self.entryDec = tkinter.Entry(self.viewLeft, width=10)
        self.entryDec.grid(row=1, column=1, sticky="w")
        tkinter.Label(self.viewLeft, text="deg.").grid(row=1, column=2, sticky="w")

        tkinter.Label(self.viewLeft, text="Duration:").grid(row=2, column=0, sticky="w")
        self.entryDuration = tkinter.Entry(self.viewLeft, width=10)
        self.entryDuration.grid(row=2, column=1, sticky="w")
        tkinter.Label(self.viewLeft, text="sec.").grid(row=2, column=2, sticky="w")

        tkinter.Label(self.viewRight, text="Weight:").grid(row=0, column=0, sticky="w")
        self.entryWeight = tkinter.Entry(self.viewRight, width=10)
        self.entryWeight.grid(row=0, column=1, sticky="w")
        tkinter.Label(self.viewRight, text="range 0-1").grid(row=0, column=2, sticky="w")
        
        tkinter.Label(self.viewRight, text="Important:").grid(row=1, column=0, sticky="w")
        self.entryImportant = ttk.Combobox(self.viewRight, width= 10)
        self.entryImportant['values'] = ["Yes", "No"]
        self.entryImportant.grid(row=1, column=1, sticky="w")
        tkinter.Label(self.viewRight, text="yes / no").grid(row=1, column=2, sticky="w")

        tkinter.Label(self.viewRight, text="Wait:").grid(row=2, column=0, sticky="w")
        self.entryWait = tkinter.Entry(self.viewRight, width=10)
        self.entryWait.grid(row=2, column=1, sticky="w")
        tkinter.Label(self.viewRight, text="sec.").grid(row=2, column=2, sticky="w")

    def update(self):
        self.entryRa.delete(0, "end")
        self.entryRa.insert(0, self.upper.info["ra"])
        self.entryDec.delete(0, "end")
        self.entryDec.insert(0, self.upper.info["dec"])
        self.entryDuration.delete(0, "end")
        self.entryDuration.insert(0, self.upper.info["duration"])
        self.entryWeight.delete(0, "end")
        self.entryWeight.insert(0, self.upper.info["weight"])
        self.entryImportant.set(self.format(self.upper.info["important"], "important"))
        self.entryWait.delete(0, "end")
        self.entryWait.insert(0, self.upper.info["wait"])
    
    def format(self, data, format=""):
        if(format == "important"):
            if(str(data) == "1"):
                return "Yes"
            else:
                return "No"
        else:
            return str(data)

class object_actions_edit():
    def __init__(self, upper):
        self.upper = upper
        
        self.load()
    
    def load(self):
        if(self.upper.mode == "new"):
            self.buttonDone = tkinter.Button(self.upper.actionsInterface, text="Add", command=self.done)
            self.buttonDone.pack(side="right", fill="x")

            self.buttonPreview = tkinter.Button(self.upper.actionsInterface, text="Preview", command=self.preview)
            self.buttonPreview.pack(side="left", fill="x")
        else:
            self.buttonDone = tkinter.Button(self.upper.actionsInterface, text="Done", command=self.done)
            self.buttonDone.pack(side="right", fill="x")

            self.buttonSave = tkinter.Button(self.upper.actionsInterface, text="Save", command=self.save)
            self.buttonSave.pack(side="left", fill="x")
            self.buttonPreview = tkinter.Button(self.upper.actionsInterface, text="Preview", command=self.preview)
            self.buttonPreview.pack(side="left", fill="x")
    
    def input(self):
        return {
            "identifier": self.format(self.upper.info["identifier"], format="identifier"),
            "ra": self.format(self.upper.infoInterfaceHandle.entryRa.get(), format="ra"),
            "dec": self.format(self.upper.infoInterfaceHandle.entryDec.get(), format="dec"),
            "duration": self.format(self.upper.infoInterfaceHandle.entryDuration.get(), format="duration"),
            "weight": self.format(self.upper.infoInterfaceHandle.entryWeight.get(), format="weight"),
            "important": self.format(self.upper.infoInterfaceHandle.entryImportant.get(), format="important"),
            "wait": self.format(self.upper.infoInterfaceHandle.entryWait.get(), format="wait")
        }
    
    def preview(self):
        self.upper.info = self.input()
        self.upper.load_info()
        for widget in self.upper.previewInterface.winfo_children():
            widget.destroy()
        self.previewInterfaceHandle = object_preview(self.upper)

    def save(self):
        if(self.upper.mode == "edit"):
            self.upper.upper.objectsInterfaceHandle.objects[self.upper.index] = self.input()
            self.upper.upper.objectsInterfaceHandle.update_contents()
        elif(self.upper.mode == "new"):
            self.upper.upper.objectsInterfaceHandle.objects.append(self.input())
            self.upper.upper.objectsInterfaceHandle.append_object(self.input())
            

    def done(self):
        if(self.upper.mode == "edit"):
            inputOriginal = self.upper.upper.objectsInterfaceHandle.objects[self.upper.index]
            inputUser = self.input()
            if(inputOriginal != inputUser):
                if(messagebox.askyesno("Save", "Do you want to save the changes?")):
                    self.save()
            self.upper.close()
        elif(self.upper.mode == "new"):
            self.save()
            self.upper.close()
    
    def format(self, data, format=""):
        if(type(data) == str):
            data = data.replace(" ", "").replace("。", ".")

        if(format == "identifier"):
            return str(data)
        elif(format == "important"):
            if(str(data) == "Yes"):
                return 1
            else:
                return 0
        elif(format == "duration"):
            return int(data)
        elif(format == "weight"):
            data = float(data)
            if(data < 0):
                return 0
            elif(data > 1):
                return 1
            else:
                return data
        elif(format == "wait"):
            return int(data)
        elif(format == "ra"):
            data = float(data)
            if(data < -180):
                while(data < -180):
                    data += 360
                print("Warning: RA is out of range. It is set to " + str(data))
            if(data > 180):
                while(data > 180):
                    data -= 360
                print("Warning: RA is out of range. It is set to " + str(data))
            return float(data)
        elif(format == "dec"):
            data = float(data)
            if(data < -90):
                while(data < -90):
                    data = -90
                print("Warning: dec is below -90, using -90 instead.")
            if(data > 90):
                while(data > 90):
                    data = 90
                print("Warning: dec is above 90, using +90 instead.")
            return float(data)
        else:
            return str(data)

class notice_outdated():
    def __init__(self, upper):
        self.upper = upper
        
        self.load()
    
    def load(self):
        tkinter.Label(self.upper.actionsInterface, text="Information outdated. Please re-open the window to update. ").pack(side="left", fill="x")
        tkinter.Button(self.upper.actionsInterface, text="Done", command=self.upper.close).pack(side="right", fill="x")

class get_info():
    def __init__(self, upper, info, mode="edit", index=0):
        self.upper = upper
        self.info = info
        self.mode = mode
        self.index = index
        self.scheduller = scheduller.scheduller()

        self.load_info()
        self.setup_window()
        self.setup_widgets()

        self.indexes_updated = self.upper.updated.object_indexes("last")
        self.root.after(100, self._plot_update_check)

        self.root.mainloop
    
    def load_info(self):
        self.scheduller = scheduller.scheduller()
        self.scheduller.objects.observation = self.upper.scheduller.objects.observation
        self.scheduller.add.object(
            identifier= self.info["identifier"], 
            ra= self.info["ra"],
            dec= self.info["dec"],
            duration= self.info["duration"],
            weight= self.info["weight"],
            important= self.info["important"],
            wait= self.info["wait"]
        )
        self.scheduller.schedule = self.scheduller.objects
    
    def setup_window(self):
        self.root = tkinter.Toplevel(self.upper.root)
        self.root.title(self.info["identifier"])
        self.root.geometry("500x700")
        self.root.resizable(False, True)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def setup_widgets(self):
        self.previewInterface = tkinter.Frame(self.root)
        self.previewInterface.pack(pady=10, padx=10, fill="both", expand=True)
        self.previewInterfaceHandle = object_preview(self)

        self.infoInterface = tkinter.Frame(self.root,)
        self.infoInterface.pack(pady=10, padx=10, fill="both", expand=True)
        self.infoInterfaceHandle = object_info(self)

        self.actionsInterface = tkinter.Frame(self.root)
        self.actionsInterface.pack(pady=10, padx=10, fill="both", expand=True)
        self.actionsInterfaceHandle = object_actions_edit(self)
    
    def close(self, event=None):
        self.root.destroy()
        self.upper.root.focus_force()
    
    def _plot_update_check(self):
        if(self.upper.updated.object_indexes("check", self.indexes_updated) and self.mode == "edit"):
            for widget in self.actionsInterface.winfo_children():
                widget.destroy()
            self.actionsInterfaceHandle = notice_outdated(self)
        else:
            self.root.after(100, self._plot_update_check)