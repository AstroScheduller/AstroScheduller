import tkinter
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename


class get_schedule():
    def __init__(self, upper):
        self.upper = upper

        self.setup_window()
        self.setup_widgets()

        self.root.mainloop
    
    def setup_window(self):
        self.root = tkinter.Toplevel(self.upper.root)
        self.root.title("Generate a plan")
        self.root.geometry("500x100")
        self.root.resizable(False, True)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def setup_widgets(self):
        self.mainInterface = tkinter.Frame(self.root)
        self.mainInterface.pack(pady=10, padx=10, fill="both", expand=True)

        self.actionsInterface = tkinter.Frame(self.root)
        self.actionsInterface.pack(pady=10, padx=10, fill="both", expand=True)

        tkinter.Label(self.mainInterface, text="Generate a plan from: ").grid(row=0, column=0, sticky="w")

        self.planFrom = tkinter.StringVar()
        self.planFrom.set("all")

        self.planFromAll = tkinter.Radiobutton(self.mainInterface, text="All Objects", variable=self.planFrom, value="all")
        self.planFromAll.grid(row=0, column=1, sticky="w")
        self.planFromList = tkinter.Radiobutton(self.mainInterface, text="Listed Objects", variable=self.planFrom, value="list")
        self.planFromList.grid(row=0, column=2, sticky="w")


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
        if(self.planFrom.get() == "all"):
            self.upper.actions.get_schedule_from_all()
            self.close()
        elif(self.planFrom.get() == "list"):
            self.upper.actions.get_schedule_from_listed()
            self.close()
        else:
            messagebox.showerror("Error", "Please select a planning option. For more information, click the \"What is this?\" button.")
            return
    
    def cancel(self):
        self.close()
    
    def help(self):
        text = "The AstroScheduller Algorithm is a simple algorithm that tries to find the best possible schedule for your observing schedule.\n\n"
        text += "If \"All Objects\" is selected, the algorithm will try to find the best possible schedule for all objects imported into the AstroScheduller [scheduller.objects_all()].\n\n"
        text += "If \"Listed Objects\" is selected, the algorithm will only try to find the best possible schedule for the objects imported into this editor that are shown as the list in the homepage of this editor [scheduller.objects_scheduled()].\n\n"
        messagebox.showinfo("Help", text)