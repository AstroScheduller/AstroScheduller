class events():
    def __init__(self, upper):
        self.upper = upper

    def on_quit(self, event=None):
        pass

    def on_objects_list_changed(self, event=None):
        self.upper.actions.update_info()
        self.upper.updated.object_list("update")

    def on_preview_changed(self, event=None):
        self.upper.actions.object_update_indexes()
        self.upper.updated.preview("update")

    def on_info_changed(self, event=None):
        self.upper.updated.info("update")
    
    def on_object_indexes_changed(self, event=None):
        self.upper.updated.object_indexes("update")