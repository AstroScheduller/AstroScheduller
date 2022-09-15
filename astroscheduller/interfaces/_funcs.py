import time

class status():
    def __init__(self, upper, enter_status = [], exit_status = []) -> None:
        self.upper = upper
        self.enter_status = enter_status
        self.exit_status = exit_status

        self.upper.statusInterfaceHandle.status.id += 1
        self.id = self.upper.statusInterfaceHandle.status.id

    def __enter__(self):
        self.update_status(self.enter_status[0], self.enter_status[1])

    def __exit__(self, exc_type, exc_value, traceback):
        self.update_status(self.exit_status[0], self.exit_status[1])
        time.sleep(2)
        self.update_status("idle", "")
    
    def update_status(self, status, message="Processing..."):
        if(self.upper.statusInterfaceHandle.status.id == self.id or self.upper.statusInterfaceHandle.status.status == "idle"):
            self.upper.statusInterfaceHandle.status.status = status
            self.upper.statusInterfaceHandle.status.message = message
            self.upper.statusInterfaceHandle.update_status()
        else:
            if(self.upper.statusInterfaceHandle.status.id < 0 and status != "idle"):
                self.upper.statusInterfaceHandle.status.id = self.id
                self.upper.statusInterfaceHandle.status.status = status
                self.upper.statusInterfaceHandle.status.message = message
                self.upper.statusInterfaceHandle.update_status()
            
            elif(self.upper.statusInterfaceHandle.status.id < 0 and status == "idle"):
                self.upper.statusInterfaceHandle.status.id = -2

            elif(self.status_to_weight(self.upper.statusInterfaceHandle.status.status) <= self.status_to_weight(status)):
                prevStatus = self.upper.statusInterfaceHandle.status.status
                prevMessage = self.upper.statusInterfaceHandle.status.message
                prevID = self.upper.statusInterfaceHandle.status.id

                self.upper.statusInterfaceHandle.status.id = -1
                self.upper.statusInterfaceHandle.status.status = status
                self.upper.statusInterfaceHandle.status.message = message
                self.upper.statusInterfaceHandle.update_status()

                time.sleep(2)

                if(self.upper.statusInterfaceHandle.status.id == -1):
                    self.upper.statusInterfaceHandle.status.id = prevID
                    self.upper.statusInterfaceHandle.status.status = prevStatus
                    self.upper.statusInterfaceHandle.status.message = prevMessage
                    self.upper.statusInterfaceHandle.update_status()
                elif(self.upper.statusInterfaceHandle.status.id == -2):
                    self.upper.statusInterfaceHandle.status.id = self.id
    
    def status_to_weight(self, status):
        if(status == "idle"):
            return 0
        elif(status == "running"):
            return 1
        elif(status == "busy"):
            return 2
        elif(status == "error"):
            return 3
        elif(status == "success"):
            return 1
        else:
            return -1

class sync():
    def __init__(self, upper):
        self.upper = upper
        self.unsyncOjects = []
        self.treeViewItems = list()

        self.load()
        self.sync()
    
    def sync(self):
        syncObjects = list()

        for item in self.treeViewItems:
            syncObjects.append(self.unsyncOjects[item["text"]])
        
        self.upper.scheduller.schedule.objects = syncObjects

    def load(self):
        self.unsyncOjects = self.upper.objectsInterfaceHandle.objects
        self.treeViewItems = self.upper.objectsInterfaceHandle.get_items()
    
class updated():
    def __init__(self, upper):
        self.updated = {
            "object_list": 0,
            "object_indexes": 0,
            "info": 0,
            "preview": 0, 
        }
    
    def _updated(self, item, action, value):
        if(action == "update"):
            self.updated[item] = time.time()
        elif(action == "last"):
            return self.updated[item]
        elif(action == "check"):
            if(value == self.updated[item]):
                return False
            else:
                return True
        else:
            print("Warning: unknown action")
        
    def object_list(self, action, value=0):
        return self._updated("object_list", action, value)

    def info(self, action, value=0):
        return self._updated("info", action, value)

    def preview(self, action, value=0):
        return self._updated("preview", action, value)
    
    def object_indexes(self, action, value=0):
        return self._updated("object_indexes", action, value)