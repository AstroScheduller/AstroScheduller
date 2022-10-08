import os
import ctypes
from queue import Queue
from threading import Thread

import tkinter
from tkinter import ttk, messagebox

from . import interfaces
            
class editor():
    def __init__(self, scheduller):
        print("Starting AstroScheduller Editor... ")
        
        self.scheduller = scheduller
        self.root = tkinter.Tk()
        self.settings = interfaces.settings.settings()
        self.actions = interfaces.actions.actions(self)
        self.events = interfaces.events.events(self)
        self.updated = interfaces._funcs.updated(self)

        self.primary_tasks = interfaces.tasks.primary_task_manager(self) # Primary Tasks are used to run tasks in the main thread, such as updating the GUI. This will make the GUI freezing.
        self.threading_tasks = interfaces.tasks.threading_task_manager(self) # Threading Tasks are used to run tasks in a separate thread, such as some data processing and plotting. This will NOT make the GUI freezing.
        # primary tasks will only be run after the threading tasks are finished. This will prevent the GUI updating BEFORE the processing is finished in the seperate thread.

        self.objectsInterfaceHandle = None
        self.previewInterfaceHandle = None
        self.statsInterfaceHandle = None

        self.setup_window()
        self.setup_keys()
        self.setup_menu()
        self.setup_widgets()

        self.root.after(50, self.backgroundloop)
        self.threadloopHandle = Thread(target=self.threadloop)
        self.threadloopHandle.start()

        self.root.mainloop()

    def get_window_geometry(self):
        screen = [self.root.winfo_screenwidth(), self.root.winfo_screenheight()]

        if(screen[0] < self.settings.window_min_width):
            screen[0] = self.settings.window_min_width

        if(screen[1] < self.settings.window_min_height):
            screen[1] = self.settings.window_min_height

        return str(screen[0]) + "x" + str(screen[1])
    
    def setup_window(self):
        self.root.title("AstroScheduller Editor")
        self.root.geometry(self.get_window_geometry())
        self.root.configure(background="white")
        self.root.minsize(self.settings.window_min_width, self.settings.window_min_height)
        self.root.iconphoto(True, tkinter.PhotoImage(file=os.path.dirname(__file__) + "/ashrel/AstroSchedullerIcon.png"))
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def setup_menu(self):
        self.menu = tkinter.Menu(self.root)

        self.setup_file_menu = tkinter.Menu(self.menu)
        self.setup_file_menu.add_command(label="Save [Ctrl/Cmd S]", command=self.save)
        self.setup_file_menu.add_command(label="Export [Ctrl/Cmd E]", command=self.export)
        self.setup_file_menu.add_separator()
        self.setup_file_menu.add_command(label="Close [Ctrl/Cmd Q]", command=self.close)

        self.setup_edit_menu = tkinter.Menu(self.menu)
        #self.setup_edit_menu.add_command(label="Undo", command=self.undo)
        #self.setup_edit_menu.add_command(label="Redo", command=self.redo)
        #self.setup_edit_menu.add_separator()
        self.setup_edit_menu.add_command(label="Add Object", command=self.add_object)
        self.setup_edit_menu.add_command(label="Remove Object", command=self.remove_object)
        self.setup_edit_menu.add_separator()
        self.setup_edit_menu.add_command(label="Object Move Up [W]", command=self.move_up)
        self.setup_edit_menu.add_command(label="Object Move Down [S]", command=self.move_down)
        self.setup_edit_menu.add_separator()
        self.setup_edit_menu.add_command(label="Object To Top", command=self.to_top)
        self.setup_edit_menu.add_command(label="Object To Bottom", command=self.to_bottom)
        self.setup_edit_menu.add_separator()
        self.setup_edit_menu.add_command(label="Generate a Plan [Ctrl/Cmd L]", command=self.get_schedule)
        self.setup_edit_menu.add_command(label="Get Object Information [Ctrl/Cmd I]", command=self.get_info)

        self.setup_plot_menu = tkinter.Menu(self.menu)
        self.setup_plot_menu.add_command(label="Plot [Ctrl/Cmd P]", command=self.actions.plot)
        #self.setup_plot_menu.add_command(label="Save Plot", command=self.plot_save)
        self.setup_edit_menu.add_separator()
        self.setup_plot_menu.add_command(label="Refresh Information", command=self.actions.update_info)
        
        #self.setup_view_menu = tkinter.Menu(self.menu)
        #self.setup_view_menu.add_command(label="Always On Top", command=self.always_on_top)

        self.setup_help_menu = tkinter.Menu(self.menu)
        self.setup_help_menu.add_command(label="Documentations", command=self.documentation)
        self.setup_edit_menu.add_separator()
        self.setup_help_menu.add_command(label="About", command=self.about)

        self.menu.add_cascade(label="File", menu=self.setup_file_menu)
        self.menu.add_cascade(label="Edit", menu=self.setup_edit_menu)
        self.menu.add_cascade(label="View", menu=self.setup_plot_menu)
        #self.menu.add_cascade(label="View", menu=self.setup_view_menu)
        self.menu.add_cascade(label="Help", menu=self.setup_help_menu)

        self.root.config(menu=self.menu)

    def setup_keys(self):
        keys = {
            "<Escape>": self.close,
            "<Control-q>": self.close,
            "<Control-Q>": self.close,
            "<Control-e>": self.export,
            "<Control-E>": self.export,
            "<Control-s>": self.save,
            "<Control-S>": self.export,
            "<Control-p>": self.actions.plot,
            "<Control-P>": self.actions.plot,
            "<Control-l>": self.actions.get_schedule,
            "<Control-L>": self.actions.get_schedule,
            "<Control-i>": self.actions.get_info,
            "<Control-I>": self.actions.get_info,
            "<Control-z>": self.undo,
            "<Control-Z>": self.undo,
            "<Control-y>": self.redo,
            "<Control-Y>": self.redo,
            "<KeyPress-w>": self.move_up,
            "<KeyPress-W>": self.move_up,
            "<KeyPress-s>": self.move_down,
            "<KeyPress-S>": self.move_down,
        }

        for key in keys:
            self.root.bind(key, keys[key])
            self.root.bind(key.replace("Control", "Command"), keys[key])
    
    def setup_widgets(self):
        ##############################
        # Frames                     #
        ##############################

        interface = tkinter.Frame(self.root, background="white")
        interface.pack(side="top", fill="both", expand=True)

        statusFrame = tkinter.Frame(self.root, height=1, background="white")
        statusFrame.pack(side="bottom", fill="x", expand=False)

        toolBarFrame = tkinter.Frame(interface, width=3, background="white")
        toolBarFrame.pack(side="left", fill="y", expand=False)

        editorFrame = tkinter.Frame(interface, background="black")
        editorFrame.pack(side="right", fill="both", expand=True)

        editingFrame = tkinter.Frame(editorFrame, background="white")
        editingFrame.pack(side="left", fill="both", expand=False)

        infoFrame = tkinter.Frame(editorFrame, background="white")
        infoFrame.pack(side="left", fill="both", expand=True)

        ##############################
        # Interfaces                 #
        ##############################

        self.statusInterface = tkinter.Frame(statusFrame, height=1, background="white")
        self.statusInterface.pack(fill="both", expand=True)
        self.statusInterfaceHandle = interfaces.main.statusInterface(self)

        self.toolBarInterface = tkinter.Frame(toolBarFrame, width=3)
        self.toolBarInterface.pack(side="left", fill="both", expand=True)
        self.toolBarInterfaceHandle = interfaces.main.toolBarInterface(self)

        self.toolBarObjectsSeparator = ttk.Separator(toolBarFrame, orient="vertical")
        self.toolBarObjectsSeparator.pack(side="left", fill="y", expand=False)

        self.objectsInterface = tkinter.Frame(editingFrame, background="white")
        self.objectsInterface.pack(fill="both", expand=True)
        self.objectsInterfaceHandle = interfaces.main.objectsInterface(self)

        self.editingInfoSeparator = ttk.Separator(infoFrame, orient="vertical")
        self.editingInfoSeparator.pack(side="left", fill="y", expand=False)

        self.previewInterface = tkinter.Frame(infoFrame)
        self.previewInterface.pack(side="top", fill="both", expand=True)
        self.previewInterfaceHandle = interfaces.main.previewInterface(self)

        self.previewStatsSeparator = ttk.Separator(infoFrame, orient="horizontal")
        self.previewStatsSeparator.pack(side="top", fill="x", expand=False) 

        self.statsInterface = tkinter.Frame(infoFrame)
        self.statsInterface.pack(side="bottom", fill="x", expand=False)
        self.statsInterfaceHandle = interfaces.main.statsInterface(self)
    
    def backgroundloop(self):
        if(self.threading_tasks.empty()):
            if(self.primary_tasks.empty() is not True):
                self.primary_tasks.run()
                self.root.update()
        self.root.after(50, self.backgroundloop)
    
    def threadloop(self):
        while True:
            if(self.threading_tasks.run() is not True):
                break
            self.root.update()

    def close(self, event=None):
        self.actions.quit()

    def move_up(self, event=None):
        self.actions.object_move_up()

    def move_down(self, event=None):
        self.actions.object_move_down()

    def to_top(self, event=None):
        self.actions.object_to_top()

    def to_bottom(self, event=None):
        self.actions.object_to_bottom()

    def get_info(self, event=None):
        self.actions.get_info()

    def add_object(self, event=None):
        self.actions.object_add()

    def remove_object(self, event=None):
        self.actions.object_remove()

    def get_schedule(self, event=None):
        self.actions.get_schedule()

    def undo(self, event=None):
        pass

    def redo(self, event=None):
        pass
    
    def save(self, event=None):
        interfaces.file_actions.save(self)

    def export(self, event=None):
        interfaces.file_actions.export(self)
    
    def plot_save(self, event=None):
        pass
    
    def always_on_top(self, event=None):
        pass
    
    def documentation(self, event=None):
        interfaces.help.documentation(self)

    def about(self, event=None):
        interfaces.help.about(self)
