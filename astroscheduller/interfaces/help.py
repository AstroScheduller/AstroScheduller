import os
import webbrowser

import tkinter
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename


from . import _srcs

class about():
    def __init__(self, upper):
        self.upper = upper

        self.version = self.upper.scheduller.info.get_version()
        self.copyright = self.upper.scheduller.info.get_copyright()
        self.website = self.upper.scheduller.info.get_website()

        try:
            self.icon = tkinter.PhotoImage(file=os.path.dirname(__file__) + "/../ashrel/AstroSchedullerIcon.png")
        except:
            self.icon = None
    
        self.setup_window()
        self.setup_keys()
        self.setup_menu()
        self.setup_widgets()
        
        self.root.mainloop()
    
    def close(self, event=None):
        self.root.destroy()
        self.upper.root.focus_force()
    
    def setup_window(self):
        self.root = tkinter.Toplevel(self.upper.root)
        self.root.title("About")
        self.root.geometry("320x204")
        self.root.resizable(False, False)
        self.root.configure(background="white")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def setup_keys(self):
        pass

    def setup_menu(self):
        pass

    def setup_widgets(self):
        title = tkinter.Label(self.root, text="", font=("Arial", 1, "bold"), background="white")
        title.pack(pady=2)

        title = tkinter.Label(self.root, image=self.icon, background="white")
        title.pack(pady=2)

        title = tkinter.Label(self.root, text="AstroScheduller", font=("Arial", 15, "bold"), background="white")
        title.pack(pady=2)

        version = tkinter.Label(self.root, text="Version: " + self.version, font=("Arial", 10), background="white")
        version.pack(pady=2)

        copyright = tkinter.Label(self.root,
            text=(self.copyright),
            font=("Arial", 10), background="white")
        copyright.pack(pady=2)

        link = tkinter.Label(self.root, text=self.website, font=("Arial", 10), foreground=_srcs.colors().link, background="white")
        link.bind("<Button-1>", lambda e: webbrowser.open(self.website))
        link.pack(pady=2)

class documentation():
    def __init__(self, upper):
        webbrowser.open("https://astroscheduller.github.io")