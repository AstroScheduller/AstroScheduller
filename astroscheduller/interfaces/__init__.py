import os

files = os.listdir(os.path.dirname(__file__))
for file in files:
    if(file.endswith(".py") and file != "__init__.py"):
        exec("from . import " + file.split(".")[0])