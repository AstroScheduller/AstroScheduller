class settings():
    _value = ""
    _allowed_values = {}
    def __init__(self, default_value: str, allowed_values: list) -> None:
        self.__dict__["_value"] = default_value
        self.__dict__["_allowed_values"] = allowed_values
    
    def __setattr__(self, __name: str, __value: any) -> None:
        if(__name == "value"):
            if(__value in self._allowed_values):
                self.__dict__["value"] = str(__value)
            else:
                print("Error: value not allowed.")
                return False
    
    def __getattr__(self, __name: str) -> any:
        if(__name == "value"):
            return self.__dict__["value"]
        elif(__name == "allowed_values" or __name == "allowed"):
            return self.__dict__["_allowed_values"]
        else:
            return None

class status():
    def __init__(self, status="idle", message="") -> None:
        self.__dict__["_status"] = "idle"
        self.__dict__["_message"] = ""
        self.__dict__["_id"] = 0
        self.__dict__["_status_list"] = ["idle", "running", "busy", "error", "success"]

        self.status = status
        self.message = message
    
    def __setattr__(self, __name: str, __value: str) -> None:
        if(__name == "status"):
            if(__value in self._status_list):
                self.__dict__["_status"] = str(__value)
            else:
                print("Error: status not recognized. Status not changed.")
                return False
        elif(__name == "message"):
            self.__dict__["_message"] = str(__value)
        elif(__name == "id"):
            self.__dict__["_id"] = int(__value)
        else:
            print("Error: key not recognized.")
            return False
    
    def __getattr__(self, __name: str) -> any:
        if(__name == "status"):
            return self.__dict__["_status"]
        elif(__name == "message"):
            return self.__dict__["_message"]
        elif(__name == "status_list"):
            return self.__dict__["_status_list"]
        elif(__name == "id"):
            return self.__dict__["_id"]
        else:
            return None

class task():
    def __init__(self, **kwargs) -> None:
        self.__dict__["id"] = 0
        self.__dict__["name"] = ""
        self.__dict__["message"] = ""
        self.__dict__["created"] = 0.0
        self.__dict__["finished"] = 0.0
        self.__dict__["priority"] = 0
        self.__dict__["method"] = None
        self.__dict__["enter_status"] = None
        self.__dict__["exit_status"] = None
        self.__dict__["error"] = {"code": 0, "error": "", "traceback": ""}

        for key in kwargs:
            self.__setattr__(key, kwargs[key])
    
    def __setattr__(self, __name: str, __value: any) -> None:
        if(__name == "method"):
            self.__dict__["method"] = __value
        elif(__name == "name"):
            self.__dict__["name"] = str(__value)
        elif(__name == "message"):
            self.__dict__["message"] = str(__value)
        elif(__name == "enter_status"):
            self.__dict__["enter_status"] = __value
        elif(__name == "exit_status"):
            self.__dict__["exit_status"] = __value
        elif(__name == "id"):
            self.__dict__["id"] = int(__value)
            if(self.__dict__["enter_status"] is not None):
                self.__dict__["enter_status"].id = self.id
            if(self.__dict__["exit_status"] is not None):
                self.__dict__["exit_status"].id = self.id
        elif(__name == "priority"):
            self.__dict__["priority"] = int(__value)
        elif(__name == "created"):
            self.__dict__["created"] = float(__value)
        elif(__name == "finished"):
            self.__dict__["finished"] = float(__value)
        elif(__name == "error"):
            self.__dict__["error"] = __value
        else:
            print("Error: key not recognized.")
            return False
        
    def __lt__(self, other):
        """ Reference: https://blog.csdn.net/babybin/article/details/111624905 """
        return self.priority < other.priority