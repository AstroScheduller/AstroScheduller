import datetime
import threading
import multiprocessing
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.pyplot import text, switch_backend

import tkinter
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename


from . import _structs, _funcs, _srcs
from .. import scheduller

class objectsInterface():
    def __init__(self, upper):
        self.upper = upper

        self.scrollbar = ttk.Scrollbar(self.upper.objectsInterface)
        self.view = ttk.Treeview(self.upper.objectsInterface, yscrollcommand=self.scrollbar.set)

        self.objects = []
        self.load_objects()
        self.insert_colomns()
        self.insert_objects()

        self.view.pack(fill="both", expand=True)
        self.view.bind("<Double-1>", self.upper.actions.get_info)

    def load_objects(self):
        self.objects = self.upper.scheduller.objects_scheduled()
    
    def insert_colomns(self):
        self.view["columns"] = ["Identifier", "RA", "Dec", "Duration", "Weight", "Important"]

        self.view.column("#0", width=40, anchor="w")
        self.view.column("Identifier", width=120, anchor="w")
        self.view.column("RA", width=80, anchor="w")
        self.view.column("Dec", width=80, anchor="w")
        self.view.column("Duration", width=100, anchor="w")
        self.view.column("Weight", width=50, anchor="w")
        self.view.column("Important", width=70, anchor="w")
        
        self.view.heading("#0", text="#", anchor="w")
        self.view.heading("Identifier", text="Identifier", anchor="w")
        self.view.heading("RA", text="RA (deg.)", anchor="w")
        self.view.heading("Dec", text="Dec (deg.)", anchor="w")
        self.view.heading("Duration", text="Duration", anchor="w")
        self.view.heading("Weight", text="Weight", anchor="w")
        self.view.heading("Important", text="Important", anchor="w")
    
    def insert_objects(self):
        for i in range(len(self.objects)):
            self.view.insert("", "end", text=i, values=[
                self.format(self.objects[i]["identifier"], "Identifier"), 
                self.format(self.objects[i]["ra"], "RA"),
                self.format(self.objects[i]["dec"], "Dec"),
                self.format(self.objects[i]["duration"], "Duration"),
                self.format(self.objects[i]["weight"], "Weight"),
                self.format(self.objects[i]["important"], "Important")
            ])
    
    def selected(self, multiple=False):
        indexes = []
        contents = []
        selections = self.view.selection()
        
        for selection in selections:
            indexes.append(self.view.index(selection))
            contents.append(self.view.item(selection))

        if(multiple):
            return indexes, contents, selections
        else:
            return indexes[0], contents[0], selections[0]
    
    def move_up(self):

        indexes, _, selections = self.selected(multiple=True)

        if(min(indexes) > 0):
            for i in range(len(indexes)):
                self.view.move(selections[i], "", indexes[i]-1)
        
        _, _, newSelections = self.selected(multiple=True)
        self.view.see(newSelections[0])

        self.upper.events.on_objects_list_changed()
    
    def move_down(self):

        indexes, _, selections = self.selected(multiple=True)

        if(max(indexes) < (len(self.view.get_children())-1)):
            for i in range(len(indexes)):
                self.view.move(selections[i], "", indexes[i]+1)
        
        _, _, newSelections = self.selected(multiple=True)
        self.view.see(newSelections[0])

        self.upper.events.on_objects_list_changed()
    
    def to_top(self):
        indexes, _, selections = self.selected(multiple=True)

        for i in range(len(indexes)):
            self.view.move(selections[i], "", i)
        
        _, _, newSelections = self.selected(multiple=True)
        self.view.see(newSelections[0])

        self.upper.events.on_objects_list_changed()
    
    def to_bottom(self):
        indexes, _, selections = self.selected(multiple=True)

        for i in range(len(indexes)):
            self.view.move(selections[i], "", len(self.view.get_children())-1-i)
        
        _, _, newSelections = self.selected(multiple=True)
        self.view.see(newSelections[0])

        self.upper.events.on_objects_list_changed()
    
    def remove(self):
        indexes, _, selections = self.selected(multiple=True)

        for i in range(len(indexes)):
            self.view.delete(selections[i])
        
        self.upper.events.on_objects_list_changed()
    
    def get_items(self):
        items = self.view.get_children()

        objects = []
        for item in items:
            objects.append(self.view.item(item))

        return objects

    def get_schedule(self, f="all"):
        if(f == "all"):
            self.upper.threading_tasks.new(
                _structs.task(
                    name = "Get schedule",
                    priority = 0,
                    method = self.upper.scheduller.get_schedule,
                    enter_status = _structs.status("busy", "Planning the observation..."),
                    exit_status = _structs.status("success", "Planned.")
                )
            )
            self.upper.primary_tasks.new(
                _structs.task(
                    name = "Reload objects list",
                    priority = 0,
                    method = self.reload,
                    enter_status = None,
                    exit_status = None
                )
            )
        elif(f == "listed"):
            self.ashHandle = scheduller.scheduller()

            for item in self.get_items():
                object = self.objects[item["text"]]
                self.ashHandle.add.object(**object)
            self.ashHandle.objects.observation = self.upper.scheduller.objects.observation
            
            self.upper.threading_tasks.new(
                _structs.task(
                    name = "Get schedule",
                    priority = 0,
                    method = self.ashHandle.get_schedule,
                    enter_status = _structs.status("busy", "Planning the observation..."),
                    exit_status = _structs.status("success", "Planned.")
                )
            )
            self.upper.threading_tasks.new(
                _structs.task(
                    name = "Get schedule",
                    priority = 0,
                    method = self._get_schedule_listed_merging,
                    enter_status = _structs.status("busy", "Planning the observation..."),
                    exit_status = _structs.status("success", "Planned.")
                )
            )
            self.upper.primary_tasks.new(
                _structs.task(
                    name = "Reload objects list",
                    priority = 0,
                    method = self.reload,
                    enter_status = None,
                    exit_status = None
                )
            )
    
    def _get_schedule_listed_merging(self):
        self.upper.scheduller.schedule = self.ashHandle.schedule
    
    def reload(self):
        self.view.delete(*self.view.get_children())
        self.load_objects()
        self.insert_objects()
        self.upper.events.on_objects_list_changed()
        self.upper.events.on_object_indexes_changed()
    
    def update_indexes(self):
        items = self.view.get_children()

        for i in range(len(items)):
            self.view.item(items[i], text=i)
        
        self.upper.events.on_objects_list_changed()
        self.upper.events.on_object_indexes_changed()
    
    def update_contents(self):
        items = self.view.get_children()

        for i in range(len(items)):
            self.view.item(
                items[i],
                values=[
                    self.format(self.objects[self.view.item(items[i])["text"]]["identifier"], "Identifier"),
                    self.format(self.objects[self.view.item(items[i])["text"]]["ra"], "RA"),
                    self.format(self.objects[self.view.item(items[i])["text"]]["dec"], "Dec"),
                    self.format(self.objects[self.view.item(items[i])["text"]]["duration"], "Duration"),
                    self.format(self.objects[self.view.item(items[i])["text"]]["weight"], "Weight"),
                    self.format(self.objects[self.view.item(items[i])["text"]]["important"], "Important")
                ]
            )
        
        self.upper.events.on_objects_list_changed()
    
    def append_object(self, object):
        items = self.view.get_children()

        self.view.insert("", "end", text=len(items), values=[
            self.format(object["identifier"], "Identifier"), 
            self.format(object["ra"], "RA"),
            self.format(object["dec"], "Dec"),
            self.format(object["duration"], "Duration"),
            self.format(object["weight"], "Weight"),
            self.format(object["important"], "Important")
        ])

        self.upper.events.on_objects_list_changed()
    
    def format(self, value, key):
        if(key == "Important"):
            if(value == 1):
                return "Yes"
            else:
                return "No"
        elif(key == "Duration"):
            hh, mm, ss = 0, 0, 0

            if(value >= 3600):
                hh = int(value/3600)
                value = value - hh*3600
            if(value >= 60):
                mm = int(value/60)
                value = value - mm*60
            ss = value

            if(len(str(ss)) == 1):
                ss = "0" + str(ss)
            if(len(str(mm)) == 1):
                mm = "0" + str(mm)
            if(len(str(hh)) == 1):
                hh = "0" + str(hh)

            return str(hh) + "h " + str(mm) + "m " + str(ss) + "s"
        else:
            return value

class previewInterface():
    def __init__(self, upper):
        self.upper = upper
        
        self.load_plot()
        self.load_canvas()
        self.insert_canvas()

        self.view.pack(fill="both", expand=True)
    
    def load_plot(self):
        self.plt = self.upper.scheduller.schedule.plot(guimode=True).plt

    def load_canvas(self):
        self.view = tkinter.Frame(self.upper.previewInterface)
        self.plt_canvas = FigureCanvasTkAgg(self.plt, self.view)
    
    def insert_canvas(self):
        self.plt_canvas.draw()
        self.plt_canvas.get_tk_widget().pack(fill="both", expand=True)

        self.plt_toolbar = NavigationToolbar2Tk(self.plt_canvas, self.view)
        self.plt_toolbar.update()
        self.plt_canvas._tkcanvas.pack(fill="both", expand=True)
    
    def update(self):
        self.upper.threading_tasks.new(
            _structs.task(
                name = "Update preview",
                priority = 0,
                method = self.load_plot,
                enter_status = _structs.status("busy", "Updating preview..."),
                exit_status = _structs.status("success", "Preview updated.")
            )
        )
        self.upper.primary_tasks.new(
            _structs.task(
                name = "Update preview",
                priority = 0,
                method = self.replot,
                enter_status = None,
                exit_status = None
            )
        )
        self.upper.primary_tasks.new(
            _structs.task(
                name = "Update preview",
                priority = 0,
                method = self.upper.events.on_preview_changed,
                enter_status = None,
                exit_status = None
            )
        )

    def replot(self):
        self.view.pack_forget()
        self.load_canvas()
        self.insert_canvas()
        self.view.pack(fill="both", expand=True)

class statsInterface():
    def __init__(self, upper):
        self.upper = upper
        self.view = tkinter.Frame(self.upper.statsInterface)

        self.widerScreen = False
        if(self.upper.root.winfo_screenwidth() > 2300):
            self.widerScreen = True

        self.viewInfo = tkinter.Frame(self.view, padx=8, pady=8)
        self.viewInfoLeft = tkinter.Frame(self.viewInfo, padx=8)
        self.viewInfoRight = tkinter.Frame(self.viewInfo, padx=8)

        self.separator1 = ttk.Separator(self.view, orient="vertical")

        self.viewObservation = tkinter.Frame(self.view, padx=8, pady=8)
        self.viewObservationLeft = tkinter.Frame(self.viewObservation, padx=8)
        self.viewObservationRight = tkinter.Frame(self.viewObservation, padx=8) 

        self.stats = {}
        self.observation_info = {}
        self.load_stats()
        self.load_observation_info()

        self.insert_stats()
        self.insert_observation_info()  
        self.update_stats()
        self.update_observation_info()

        if(self.widerScreen):
            self.viewObservationLeft.pack(side="left", fill="both", expand=True)
            self.viewObservationRight.pack(side="right", fill="both", expand=True)
            self.viewObservation.grid(row=0, column=2, sticky="nsew")

            self.separator1.grid(row=0, column=1, sticky="nsew")

        self.viewInfoLeft.pack(side="left", fill="both", expand=True)
        self.viewInfoRight.pack(side="right", fill="both", expand=True)
        self.viewInfo.grid(row=0, column=0, sticky="nsew")

        self.view.pack(fill="both", expand=True)

    def load_stats(self):
        self.stats["all_objects"] = len(self.upper.scheduller.objects_all())
        self.stats["scheduled_objects"] = len(self.upper.scheduller.objects_scheduled())
        self.stats["unscheduled_objects"] = len(self.upper.scheduller.objects_unscheduled())
        self.stats["observation_duration"] = self.upper.scheduller.len_observation()
        self.stats["wait_duration"] = self.upper.scheduller.len_wait()
        self.stats["schedule_rate"] = self.format(self.upper.scheduller.rate_schedule())
    
    def load_observation_info(self):
        self.observation_info["telescope_location"] = self.format(self.upper.scheduller.schedule.observation["telescope"]["latitude"]) + " " + self.format(self.upper.scheduller.schedule.observation["telescope"]["longitude"]) + " " + self.format(self.upper.scheduller.schedule.observation["telescope"]["altitude"])
        self.observation_info["observation_begin"] = self.format(self.upper.scheduller.schedule.observation["duration"]["begin"], "timestamps")
        self.observation_info["observation_end"] = self.format(self.upper.scheduller.schedule.observation["duration"]["end"], "timestamps")
        self.observation_info["telescope_velocity"] = self.format(self.upper.scheduller.schedule.observation["telescope"]["velocity"]["ra"]) + " " + self.format(self.upper.scheduller.schedule.observation["telescope"]["velocity"]["dec"])
        self.observation_info["telescope_elevation"] = self.format(self.upper.scheduller.schedule.observation["elevation"]["minimal"]) + " - " + self.format(self.upper.scheduller.schedule.observation["elevation"]["maximal"])
        self.observation_info["telescope_escape_sun"] = self.format(self.upper.scheduller.schedule.observation["escape"]["sun"])
    
    def format(self, value, sp_type=False):
        if(sp_type == "timestamps"):
            return datetime.datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")

        if(type(value) == int or type(value) == float):
            return "{:.{}f}".format(value, 2)
        else:
            return str(value)

    def insert_stats(self):
        # Labels
        self.view.label_all_objects = tkinter.Label(self.viewInfoLeft, text="All Objects:", font=("Arial", 12, "bold"))
        self.view.label_all_objects.grid(row=0, column=0, sticky="w")
        self.view.label_scheduled_objects = tkinter.Label(self.viewInfoLeft, text="Scheduled Objects:", font=("Arial", 12, "bold"))
        self.view.label_scheduled_objects.grid(row=1, column=0, sticky="w")
        self.view.label_unscheduled_objects = tkinter.Label(self.viewInfoLeft, text="Unscheduled Objects:", font=("Arial", 12, "bold"))
        self.view.label_unscheduled_objects.grid(row=2, column=0, sticky="w")
        self.view.label_observation_duration = tkinter.Label(self.viewInfoRight, text="Observation Duration:", font=("Arial", 12, "bold"))
        self.view.label_observation_duration.grid(row=0, column=3, sticky="w")
        self.view.label_wait_duration = tkinter.Label(self.viewInfoRight, text="Wait Duration:", font=("Arial", 12, "bold"))
        self.view.label_wait_duration.grid(row=1, column=3, sticky="w")
        self.view.label_schedule_rate = tkinter.Label(self.viewInfoRight, text="Schedule Rate:", font=("Arial", 12, "bold"))
        self.view.label_schedule_rate.grid(row=2, column=3, sticky="w")

        # Values
        self.view.value_all_objects = tkinter.Entry(self.viewInfoLeft, textvariable=tkinter.StringVar(self.viewInfoLeft, value=self.stats["all_objects"]), state="readonly", font=("Arial", 12), background="white")
        self.view.value_all_objects.grid(row=0, column=1, sticky="w")
        self.view.value_scheduled_objects = tkinter.Entry(self.viewInfoLeft, textvariable=tkinter.StringVar(self.viewInfoLeft, value=self.stats["scheduled_objects"]), state="readonly", font=("Arial", 12), background="white")
        self.view.value_scheduled_objects.grid(row=1, column=1, sticky="w")
        self.view.value_unscheduled_objects = tkinter.Entry(self.viewInfoLeft, textvariable=tkinter.StringVar(self.viewInfoLeft, value=self.stats["unscheduled_objects"]), state="readonly", font=("Arial", 12), background="white")
        self.view.value_unscheduled_objects.grid(row=2, column=1, sticky="w")
        self.view.value_observation_duration = tkinter.Entry(self.viewInfoRight, textvariable=tkinter.StringVar(self.viewInfoRight, value=self.stats["observation_duration"]), state="readonly", font=("Arial", 12), background="white")
        self.view.value_observation_duration.grid(row=0, column=4, sticky="w")
        self.view.value_wait_duration = tkinter.Entry(self.viewInfoRight, textvariable=tkinter.StringVar(self.viewInfoRight, value=self.stats["wait_duration"]), state="readonly", font=("Arial", 12), background="white")
        self.view.value_wait_duration.grid(row=1, column=4, sticky="w")
        self.view.value_schedule_rate = tkinter.Entry(self.viewInfoRight, textvariable=tkinter.StringVar(self.viewInfoRight, value=self.stats["schedule_rate"]), state="readonly", font=("Arial", 12), background="white")
        self.view.value_schedule_rate.grid(row=2, column=4, sticky="w")

        # Units
        self.view.unit_all_objects = tkinter.Label(self.viewInfoLeft, text="(Objects)",  font=("Arial", 10))
        self.view.unit_all_objects.grid(row=0, column=2, sticky="w")
        self.view.unit_scheduled_objects = tkinter.Label(self.viewInfoLeft, text="(Objects)", font=("Arial", 10))
        self.view.unit_scheduled_objects.grid(row=1, column=2, sticky="w")
        self.view.unit_unscheduled_objects = tkinter.Label(self.viewInfoLeft, text="(Objects)", font=("Arial", 10))
        self.view.unit_unscheduled_objects.grid(row=2, column=2, sticky="w")
        self.view.unit_observation_duration = tkinter.Label(self.viewInfoRight, text="(Seconds)", font=("Arial", 10))
        self.view.unit_observation_duration.grid(row=0, column=5, sticky="w")
        self.view.unit_wait_duration = tkinter.Label(self.viewInfoRight, text="(Seconds)", font=("Arial", 10))
        self.view.unit_wait_duration.grid(row=1, column=5, sticky="w")
        self.view.unit_schedule_rate = tkinter.Label(self.viewInfoRight, text="(Objects/Second)", font=("Arial", 10))
        self.view.unit_schedule_rate.grid(row=2, column=5, sticky="w")
    
    def insert_observation_info(self):
        # Labels
        self.view.label_telescope_location = tkinter.Label(self.viewObservationLeft, text="Telescope Location:", font=("Arial", 12, "bold"))
        self.view.label_telescope_location.grid(row=0, column=0, sticky="w")
        self.view.label_observation_begin = tkinter.Label(self.viewObservationLeft, text="Observation Begin:", font=("Arial", 12, "bold"))
        self.view.label_observation_begin.grid(row=1, column=0, sticky="w")
        self.view.label_observation_end = tkinter.Label(self.viewObservationLeft, text="Observation End:", font=("Arial", 12, "bold"))
        self.view.label_observation_end.grid(row=2, column=0, sticky="w")
        self.view.label_telescope_velocity = tkinter.Label(self.viewObservationRight, text="Telescope Rotating Velocity:", font=("Arial", 12, "bold"))
        self.view.label_telescope_velocity.grid(row=1, column=3, sticky="w")
        self.view.label_telescope_elevation = tkinter.Label(self.viewObservationRight, text="Telescope Elevation Range:", font=("Arial", 12, "bold"))
        self.view.label_telescope_elevation.grid(row=2, column=3, sticky="w")
        self.view.label_telescope_escape_sun = tkinter.Label(self.viewObservationRight, text="Escape From the Sun:", font=("Arial", 12, "bold"))
        self.view.label_telescope_escape_sun.grid(row=3, column=3, sticky="w")

        # Values
        self.view.value_telescope_location = tkinter.Entry(self.viewObservationLeft, textvariable=tkinter.StringVar(self.viewObservationLeft, value="--"), state="readonly", font=("Arial", 12), background="white")
        self.view.value_telescope_location.grid(row=0, column=1, sticky="w")
        self.view.value_observation_begin = tkinter.Entry(self.viewObservationLeft, textvariable=tkinter.StringVar(self.viewObservationLeft, value="--"), state="readonly", font=("Arial", 12), background="white")
        self.view.value_observation_begin.grid(row=1, column=1, sticky="w")
        self.view.value_observation_end = tkinter.Entry(self.viewObservationLeft, textvariable=tkinter.StringVar(self.viewObservationLeft, value="--"), state="readonly", font=("Arial", 12), background="white")
        self.view.value_observation_end.grid(row=2, column=1, sticky="w")
        self.view.value_telescope_velocity = tkinter.Entry(self.viewObservationRight, textvariable=tkinter.StringVar(self.viewObservationRight, value="--"), state="readonly", font=("Arial", 12), background="white")
        self.view.value_telescope_velocity.grid(row=1, column=4, sticky="w")
        self.view.value_telescope_elevation = tkinter.Entry(self.viewObservationRight, textvariable=tkinter.StringVar(self.viewObservationRight, value="--"), state="readonly", font=("Arial", 12), background="white")
        self.view.value_telescope_elevation.grid(row=2, column=4, sticky="w")
        self.view.value_telescope_escape_sun = tkinter.Entry(self.viewObservationRight, textvariable=tkinter.StringVar(self.viewObservationRight, value="--"), state="readonly", font=("Arial", 12), background="white")
        self.view.value_telescope_escape_sun.grid(row=3, column=4, sticky="w")

        # Units
        self.view.unit_telescope_location = tkinter.Label(self.viewObservationLeft, text="(Lat. Lon. Hei. in Degrees)", font=("Arial", 10))
        self.view.unit_telescope_location.grid(row=0, column=2, sticky="w")
        self.view.unit_observation_begin = tkinter.Label(self.viewObservationLeft, text="(UTC Timezone)", font=("Arial", 10))
        self.view.unit_observation_begin.grid(row=1, column=2, sticky="w")
        self.view.unit_observation_end = tkinter.Label(self.viewObservationLeft, text="(UTC Timezone)", font=("Arial", 10))
        self.view.unit_observation_end.grid(row=2, column=2, sticky="w")
        self.view.unit_telescope_velocity = tkinter.Label(self.viewObservationRight, text="(R.A. Dec. in Degrees/Second)", font=("Arial", 10))
        self.view.unit_telescope_velocity.grid(row=1, column=5, sticky="w")
        self.view.unit_telescope_elevation = tkinter.Label(self.viewObservationRight, text="(Min. - Max. Degrees)", font=("Arial", 10))
        self.view.unit_telescope_elevation.grid(row=2, column=5, sticky="w")
        self.view.unit_telescope_escape_sun = tkinter.Label(self.viewObservationRight, text="(Degrees)", font=("Arial", 10))
        self.view.unit_telescope_escape_sun.grid(row=3, column=5, sticky="w")

    def update_stats(self):
        #self.load_stats()
        self.view.value_all_objects.config(textvariable=tkinter.StringVar(self.view, value=self.stats["all_objects"]))
        self.view.value_scheduled_objects.config(textvariable=tkinter.StringVar(self.view, value=self.stats["scheduled_objects"]))
        self.view.value_unscheduled_objects.config(textvariable=tkinter.StringVar(self.view, value=self.stats["unscheduled_objects"]))
        self.view.value_observation_duration.config(textvariable=tkinter.StringVar(self.view, value=self.stats["observation_duration"]))
        self.view.value_wait_duration.config(textvariable=tkinter.StringVar(self.view, value=self.stats["wait_duration"]))
        self.view.value_schedule_rate.config(textvariable=tkinter.StringVar(self.view, value=self.stats["schedule_rate"]))
    
    def update_observation_info(self):
        #self.load_observation_info()
        self.view.value_telescope_location.config(textvariable=tkinter.StringVar(self.viewObservationLeft, value=self.observation_info["telescope_location"]))
        self.view.value_observation_begin.config(textvariable=tkinter.StringVar(self.viewObservationLeft, value=self.observation_info["observation_begin"]))
        self.view.value_observation_end.config(textvariable=tkinter.StringVar(self.viewObservationLeft, value=self.observation_info["observation_end"]))
        self.view.value_telescope_velocity.config(textvariable=tkinter.StringVar(self.viewObservationRight, value=self.observation_info["telescope_velocity"]))
        self.view.value_telescope_elevation.config(textvariable=tkinter.StringVar(self.viewObservationRight, value=self.observation_info["telescope_elevation"]))
        self.view.value_telescope_escape_sun.config(textvariable=tkinter.StringVar(self.viewObservationRight, value=self.observation_info["telescope_escape_sun"]))

    def update(self):
        self.upper.threading_tasks.new(
            _structs.task(
                name = "Update telescope info",
                priority = 0,
                method = self.load_observation_info,
                enter_status = _structs.status("running", "Updating telescope information..."),
                exit_status = _structs.status("idle", "Telescope information updated.")
            )
        )
        self.upper.primary_tasks.new(
            _structs.task(
                name = "Update telescope info",
                priority = 0,
                method = self.update_observation_info,
                enter_status = None, 
                exit_status = None
            )
        )
        self.upper.threading_tasks.new(
            _structs.task(
                name = "Update stats",
                priority = 1,
                method = self.load_stats,
                enter_status = _structs.status("running", "Updating statistics..."),
                exit_status = _structs.status("idle", "Statistics updated.")
            )
        )
        self.upper.primary_tasks.new(
            _structs.task(
                name = "Update stats",
                priority = 1,
                method = self.update_stats,
                enter_status = None, 
                exit_status = None
            )
        )
        self.upper.events.on_info_changed()

class statusInterface():
    def __init__(self, upper):
        self.upper = upper
        self.status = _structs.status()

        self.load_icons()

        self.view = tkinter.Frame(self.upper.statusInterface)
        self.viewStatus = tkinter.Frame(self.view, background=self.get_status_color())
        self.viewIcons = tkinter.Frame(self.view, background=self.get_icon_color())

        self.insert_status()
        self.insert_icons()

        self.viewIcons.grid(row=0, column=0, sticky="w", padx=0, pady=0)
        self.viewStatus.grid(row=0, column=2, sticky="w", padx=2, pady=0)
        self.view.pack(fill="both", expand=True)
        
        self.update_status()
        self.update_icons()
    
    def load_icons(self):
        self.iconPlottingEngine = _srcs.icons().PLE
        self.iconPlottingQuality = _srcs.icons().PLQ
        self.iconPlanningEngine = _srcs.icons().PNE
        self.iconIdle = _srcs.icons().idle
        self.iconRunning = _srcs.icons().running
        self.iconBusy = _srcs.icons().busy
        self.iconError = _srcs.icons().error
        self.iconSuccess = _srcs.icons().success
    
    def insert_status(self):
        self.view.statusContainerFrame = tkinter.Frame(self.viewStatus, background=self.get_status_color(), padx=2)
        self.view.statusContainerFrame.pack(side="left", fill="both", expand=True)
        self.view.status_icon = tkinter.Label(self.view.statusContainerFrame, image=self.iconIdle, background=self.get_status_color())
        self.view.status_icon.grid(row=0, column=0, sticky="w", padx=0, pady=0)
        self.view.status_label = tkinter.Label(self.view.statusContainerFrame, text="Initialized", font=("Arial", 12), background=self.get_status_color(), foreground="white")
        self.view.status_label.grid(row=0, column=1, sticky="w", padx=0, pady=0)
    
    def insert_icons(self):
        self.view.iconPlanningEngineFrame = tkinter.Frame(self.viewIcons, background=self.get_icon_color(), padx=3)
        self.view.iconPlanningEngineFrame.grid(row=0, column=0, sticky="w")
        self.view.iconPlanningEngineIcon = tkinter.Label(self.view.iconPlanningEngineFrame, image=self.iconPlanningEngine, background=self.get_icon_color(), padx=1)
        self.view.iconPlanningEngineText = tkinter.Label(self.view.iconPlanningEngineFrame, text="Unknown", font=("Arial", 12), background=self.get_icon_color(), foreground="white", padx=1)
        self.view.iconPlanningEngineIcon.grid(row=0, column=0, sticky="w")
        self.view.iconPlanningEngineText.grid(row=0, column=1, sticky="w")

        self.view.iconPlottingEngineFrame = tkinter.Frame(self.viewIcons, background=self.get_icon_color(), padx=3)
        self.view.iconPlottingEngineFrame.grid(row=0, column=1, sticky="w")
        self.view.iconPlottingEngineIcon = tkinter.Label(self.view.iconPlottingEngineFrame, image=self.iconPlottingEngine, background=self.get_icon_color(), padx=1)
        self.view.iconPlottingEngineText = tkinter.Label(self.view.iconPlottingEngineFrame, text="Unknown", font=("Arial", 12), background=self.get_icon_color(), foreground="white", padx=1)
        self.view.iconPlottingEngineIcon.grid(row=0, column=0, sticky="w")
        self.view.iconPlottingEngineText.grid(row=0, column=1, sticky="w")
        
        self.view.iconPlottingQualityFrame = tkinter.Frame(self.viewIcons, background=self.get_icon_color(), padx=3)
        self.view.iconPlottingQualityFrame.grid(row=0, column=2, sticky="w")
        self.view.iconPlottingQualityIcon = tkinter.Label(self.view.iconPlottingQualityFrame, image=self.iconPlottingQuality, background=self.get_icon_color(), padx=1)
        self.view.iconPlottingQualityText = tkinter.Label(self.view.iconPlottingQualityFrame, text="Unknown", font=("Arial", 12), background=self.get_icon_color(), foreground="white", padx=1)
        self.view.iconPlottingQualityIcon.grid(row=0, column=0, sticky="w")
        self.view.iconPlottingQualityText.grid(row=0, column=1, sticky="w")

    def update_status(self):
        if(self.status.status == "idle"):
            self.status.message = "Idle."
        color, icon = self.get_status_color(True)

        self.view.status_icon.config(image=icon)
        self.view.status_icon.config(background=color)
        self.view.status_label.config(textvariable=tkinter.StringVar(self.view, value=self.status.message))
        self.view.status_label.config(background=color)
        self.view.config(background=color)
        self.viewStatus.config(background=color)
        self.view.statusContainerFrame.config(background=color)
    
    def get_status_color(self, icon=False):
        if self.status.status == "idle":
            if(icon):
                return _srcs.colors().idle, self.iconIdle
            return _srcs.colors().idle
        elif self.status.status == "running":
            if(icon):
                return _srcs.colors().running, self.iconRunning
            return _srcs.colors().running
        elif self.status.status == "busy":
            if(icon):
                return _srcs.colors().busy, self.iconBusy
            return _srcs.colors().busy
        elif self.status.status == "error":
            if(icon):
                return _srcs.colors().error, self.iconError
            return _srcs.colors().error
        elif self.status.status == "success":
            if(icon):
                return _srcs.colors().success, self.iconSuccess
            return _srcs.colors().success
        else:
            if(icon):
                return _srcs.colors().initialized, self.iconIdle
            return _srcs.colors().initialized
    
    def get_icon_color(self):
        return _srcs.colors().icon_bkg

    def update_icons(self):
        self.view.iconPlanningEngineText.config(text="AshGo")
        self.view.iconPlottingEngineText.config(text="AshGo")
        self.view.iconPlottingQualityText.config(text="High")

class toolBarInterface():
    def __init__(self, upper):
        self.upper = upper

        self.load_icons()

        self.view = tkinter.Frame(self.upper.toolBarInterface)
        self.viewTop = tkinter.Frame(self.view)
        self.viewTopMiddleSeparator = ttk.Separator(self.viewTop, orient="horizontal")
        self.viewMiddleUpper = tkinter.Frame(self.view)
        self.viewMiddleMiddleSeparator = ttk.Separator(self.viewMiddleUpper, orient="horizontal")
        self.viewMiddleLower = tkinter.Frame(self.view)
        self.viewMiddleBottomSeparator = ttk.Separator(self.viewMiddleLower, orient="horizontal")
        self.viewBottom = tkinter.Frame(self.view)

        self.insert_icons()

        self.viewTop.pack(side="top", fill="x", expand=True, padx=0, pady=0)
        self.viewTopMiddleSeparator.pack(side="top", fill="x", expand=True, pady=3)
        self.viewMiddleUpper.pack(side="top", fill="x", expand=True, padx=0, pady=0)
        self.viewMiddleMiddleSeparator.pack(side="top", fill="x", expand=True, pady=3)
        self.viewMiddleLower.pack(side="top", fill="x", expand=True, padx=0, pady=0)
        self.viewMiddleBottomSeparator.pack(side="top", fill="x", expand=True, pady=3)
        self.viewBottom.pack(side="top", fill="x", expand=True, padx=0, pady=0)
        self.view.pack(side="top", fill="x", expand=True, padx=3, pady=3)
    
    def load_icons(self):
        self.iconPlot = _srcs.icons().plot
        self.iconSchedule = _srcs.icons().schedule
        self.iconUp = _srcs.icons().up
        self.iconDown = _srcs.icons().down
        self.iconTop = _srcs.icons().top
        self.iconBottom = _srcs.icons().bottom
        self.iconPlus = _srcs.icons().plus
        self.iconMinus = _srcs.icons().minus
        self.iconInfo = _srcs.icons().info

    def insert_icons(self):
        self.viewTop.schedule = tkinter.Button(self.viewTop, image=self.iconSchedule, command=self.upper.actions.get_schedule)
        self.viewTop.schedule.pack(side="top", fill="x", expand=True)
        self.viewTop.plot = tkinter.Button(self.viewTop, image=self.iconPlot, command=self.upper.actions.plot)
        self.viewTop.plot.pack(side="top", fill="x", expand=True)

        self.viewMiddleUpper.top = tkinter.Button(self.viewMiddleUpper, image=self.iconTop, command=self.upper.actions.object_to_top)
        self.viewMiddleUpper.top.pack(side="top", fill="x", expand=True)
        self.viewMiddleUpper.up = tkinter.Button(self.viewMiddleUpper, image=self.iconUp, command=self.upper.actions.object_move_up)
        self.viewMiddleUpper.up.pack(side="top", fill="x", expand=True)
        self.viewMiddleUpper.down = tkinter.Button(self.viewMiddleUpper, image=self.iconDown, command=self.upper.actions.object_move_down)
        self.viewMiddleUpper.down.pack(side="top", fill="x", expand=True)
        self.viewMiddleUpper.bottom = tkinter.Button(self.viewMiddleUpper, image=self.iconBottom, command=self.upper.actions.object_to_bottom)
        self.viewMiddleUpper.bottom.pack(side="top", fill="x", expand=True)

        self.viewMiddleLower.plus = tkinter.Button(self.viewMiddleLower, image=self.iconPlus, command=self.upper.actions.add_object)
        self.viewMiddleLower.plus.pack(side="top", fill="x", expand=True)
        self.viewMiddleLower.minus = tkinter.Button(self.viewMiddleLower, image=self.iconMinus, command=self.upper.actions.object_remove)
        self.viewMiddleLower.minus.pack(side="top", fill="x", expand=True)

        self.viewBottom.info = tkinter.Button(self.viewBottom, image=self.iconInfo, command=self.upper.actions.get_info)
        self.viewBottom.info.pack(side="top", fill="x", expand=True)

    def action(self):
        pass