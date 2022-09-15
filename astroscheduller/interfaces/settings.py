from . import _structs

class settings():
    def __init__(self):
        self.plot_engine = _structs.settings(
            "ashGo", 
            ["ashGo", "astropy"],
        )
        self.plot_quality = _structs.settings(
            "high", 
            ["max", "high", "med", "low", "quick"]
        )
        self.planning_engine = _structs.settings(
            "ashGo", 
            ["ashGo"]
        )
        self.window_min_width = 1280
        self.window_min_height = 720
