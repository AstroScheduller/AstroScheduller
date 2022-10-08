from . import _funcs, object_info, get_schedule, add_object

try:
    from tkinter import ttk, messagebox
except ImportError:
    pass

class actions():
    def __init__(self, upper):
        self.upper = upper

    def plot(self, event=None):
        self.upper.previewInterfaceHandle.update()

    def update_info(self, event=None):
        _funcs.sync(self.upper)
        self.upper.statsInterfaceHandle.update()
    
    def object_move_up(self, event=None):
        self.upper.objectsInterfaceHandle.move_up()

    def object_move_down(self, event=None):
        self.upper.objectsInterfaceHandle.move_down()
        
    def object_to_top(self, event=None):
        self.upper.objectsInterfaceHandle.to_top()

    def object_to_bottom(self, event=None):
        self.upper.objectsInterfaceHandle.to_bottom()

    def object_remove(self, event=None):
        self.upper.objectsInterfaceHandle.remove()
    
    def object_update_indexes(self, event=None):
        self.upper.objectsInterfaceHandle.update_indexes()

    def get_schedule(self, event=None):
        get_schedule.get_schedule(self.upper)
    
    def get_schedule_from_all(self, event=None):
        if(messagebox.askokcancel("Overwrite Warning", "This action will overwrite the current schedule.")):
            self.upper.objectsInterfaceHandle.get_schedule(f="all")
            self.plot()
    
    def get_schedule_from_listed(self, event=None):
        if(messagebox.askokcancel("Overwrite Warning", "This action will overwrite the current schedule.")):
            self.upper.objectsInterfaceHandle.get_schedule(f="listed")
            self.plot()
    
    def quit(self, event=None):
        if(self.upper.threading_tasks.empty() == False):
            messagebox.showwarning("Tasks Still Running", "There are still background tasks running. Please wait for them to finish before quitting the editor.")
        else:
            if(messagebox.askokcancel("Quit", "Are you sure you want to quit?")):
                self.upper.threading_tasks.quit()
                self.upper.threadloopHandle.join()
                self.upper.root.destroy()
        
    def get_info(self, event=None):
        _, contents, _ = self.upper.objectsInterfaceHandle.selected(multiple=True)

        if(len(contents) > 0):
            object_info.get_info(
                self.upper, 
                self.upper.objectsInterfaceHandle.objects[contents[0]["text"]], 
                mode= "edit", index= contents[0]["text"]
            )
        else:
            messagebox.showinfo("No Object Selected", "There is no object selected. \n\nTo get information about an object, select it by clicking on it in the list, then click the \"Get Info\" button.")
    
    def add_object(self, event=None):
        add_object.add_object(self.upper)
    
    def object_add(self, event=None):
        self.add_object()