import time
import traceback
import threading
from queue import Queue, PriorityQueue

from . import _structs

class threading_task_manager():
    def __init__(self, upper):
        self.upper = upper
        self.tasks = PriorityQueue()
        self.history = []
        self.counts = 0

    def new(self, task):
        self.counts += 1
        task.id = self.tasks.qsize()
        self.tasks.put((task.priority, task))
    
    def run(self):
        with task_runner(self.upper, self.tasks) as tr:
            tr.run()
        tr.task.finished = time.time()
        self.history.append(tr.task)
        
        if(tr.task.name == "sys:task_exit"):
            return False
        return True
    
    def empty(self):
        if(self.tasks.empty()):
            if(self.counts == (self.tasks.qsize() + len(self.history))):
                return True
        return False
    
    def quit(self):
        self.new(_structs.task(name="sys:task_exit", method=None, priority=10))

class primary_task_manager():
    def __init__(self, upper):
        self.upper = upper
        self.tasks = Queue()
        self.history = []
        self.counts = 0

    def new(self, task):
        self.counts += 1
        task.id = self.tasks.qsize()
        self.tasks.put((task.priority, task))

        """
        self.counts += 3
        task.id = self.tasks.qsize()

        task_enter = _structs.task(
            id=task.id,
            name="sys:task_enter",
            method=None,
            enter_status=task.enter_status,
            exit_status=None
        )
        task_exit = _structs.task(
            id=task.id,
            name="sys:task_exit",
            method=None,
            enter_status=None,
            exit_status=task.exit_status
        )
        task.enter_status = None
        task.exit_status = None

        self.tasks.put([0, task_enter])
        self.tasks.put([0, task])
        self.tasks.put([0, task_exit])
        """
    
    def run(self):
        with task_runner(self.upper, self.tasks) as tr:
            tr.run()
        self.history.append(tr.task)
    
    def empty(self):
        if(self.tasks.empty()):
            if(self.counts == (self.tasks.qsize() + len(self.history))):
                return True
        return False

class task_runner():
    def __init__(self, upper, tasks) -> None:
        self.upper = upper
        self.tasks = tasks
        self.task = self.tasks.get()[1]
        self.id = self.task.id
        self.enter_status = self.task.enter_status
        self.exit_status = self.task.exit_status

        self.upper.statusInterfaceHandle.status.id = self.id

    def __enter__(self):
        if(self.enter_status is not None):
            self.update_status(self.enter_status.status, self.enter_status.message)
            time.sleep(0.1)
        
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if(self.task.error["code"] == 1):
            self.update_status("error", "" + self.task.name + ": " + self.task.error["error"])
            time.sleep(2)
        else:
            if(self.exit_status is not None):
                if(self.exit_status.status == "idle"):
                    self.update_status("idle", "")
                else:
                    self.update_status(self.exit_status.status, self.exit_status.message)
                    time.sleep(2)
                    self.update_status("idle", "")
    
    def exit_message(self):
        self.update_status(self.exit_status.status, self.exit_status.message)
        time.sleep(1.5)
    
    def update_status(self, status, message="Processing..."):
        self.upper.statusInterfaceHandle.status.status = status
        self.upper.statusInterfaceHandle.status.message = message
        self.upper.statusInterfaceHandle.update_status()
    
    def run(self):
        if(self.task.method is not None):
            try:
                self.task.method()
                self.task.finished = time.time()
            except Exception as e:
                self.task.error = {
                    "code": 1,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
                print("[AshGUI]", self.task.error["traceback"])
                return False
            return True
        
        return False
