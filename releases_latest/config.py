import hashlib
import json
import os

__DIR__ = os.path.dirname(os.path.realpath(__file__))
config = {
    "darwin/amd64": {
        "filename": "_scheduller_darwin_amd64.so",
        "url": "https://raw.githubusercontent.com/xiawenke/AstroScheduller/Dev/releases_latest/_scheduller_darwin_amd64.so", 
        "md5": ""
    }, 
    "linux/amd64": {
        "filename": "_scheduller_linux_amd64.so",
        "url": "https://raw.githubusercontent.com/xiawenke/AstroScheduller/Dev/releases_latest/_scheduller_linux_amd64.so", 
        "md5": ""
    }, 
    "windows/amd64": {
        "filename": "_scheduller_windows_amd64.dll",
        "url": "https://raw.githubusercontent.com/xiawenke/AstroScheduller/Dev/releases_latest/_scheduller_windows_amd64.dll", 
        "md5": ""
    }
}

for platform in config:
    config[platform]["md5"] = hashlib.md5(open(__DIR__ + "/" + config[platform]["filename"], "rb").read()).hexdigest()

config = {"*": config}
json.dump(config, open(__DIR__ + "/" + "_scheduller.config", "w+"), indent=4)